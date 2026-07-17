# -*- coding: utf-8 -*-
# ============================================================
# GNI MAD Runner -- Standalone MAD Pipeline
# Runs 5 minutes after main pipeline (gni_mad.yml cron)
# Reads latest fresh report from Supabase
# Runs full MAD protocol with clean Groq TPM window
# Updates report with mad_* fields
# GNI-R-110: MAD runs separately to guarantee clean TPM window
# S37 PATCH: _fetch_relevant_articles splits into two queries:
#   scored_arts  (stage3_score > 0)  -> Bull/Bear/Ostrich/Arb
#   weak_arts    (stage3_score = 0)  -> Swan weak signal hunting
# ============================================================

import os
import sys
import time
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

GITHUB_ACTIONS = os.getenv('GITHUB_ACTIONS', 'false').lower() == 'true'

# GNI-R-239: Run preflight check before MAD (local only -- GitHub Actions skips)
if not GITHUB_ACTIONS:
    try:
        from mad_preflight import run_preflight
        if not run_preflight():
            print('Pre-flight FAILED -- MAD pipeline aborted.')
            print('Fix the issues above then re-run mad_preflight.py')
            sys.exit(0)
    except ImportError:
        print('  WARNING: mad_preflight.py not found -- skipping preflight check')
        print('  Copy mad_preflight.py to ai_engine/ folder for safety checks')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from quota_guard import check_quota, log_usage, _send_telegram_alert


def _get_client():
    from supabase import create_client
    url = os.getenv('SUPABASE_URL', '')
    key = os.getenv('SUPABASE_SERVICE_KEY', '')
    if not url or not key:
        print('  ERROR: Missing SUPABASE_URL or SUPABASE_SERVICE_KEY')
        return None
    return create_client(url, key)


def _fetch_fresh_report(client):
    """
    Fetch most recent pending report created in last 90 minutes.
    90 min window covers GNI-R-240 worst case:
    Intelligence runtime (~45 min) + handshake wait (~25 min) = ~70 min.
    Only returns reports with mad_verdict=pending -- prevents duplicate debates.
    """
    cutoff = (datetime.now(timezone.utc) - timedelta(minutes=90)).isoformat()
    try:
        result = client.table('reports') \
            .select('*') \
            .gte('created_at', cutoff) \
            .eq('mad_verdict', 'pending') \
            .order('created_at', desc=True) \
            .limit(1) \
            .execute()

        if not result.data:
            print('  No pending reports found in last 90 minutes -- nothing to do')
            return None

        report = result.data[0]
        print('  Found: ' + report['id'][:8] + '... -- ' + report.get('title', '')[:60])
        print('  Created: ' + report.get('created_at', '')[:19] + ' UTC')
        print('  Current MAD verdict: ' + str(report.get('mad_verdict', 'none')))
        return report

    except Exception as e:
        print('  ERROR fetching report: ' + str(e))
        return None


def _fetch_relevant_articles(client, run_id):
    """
    Fetch articles from this pipeline run for MAD context.
    S37 PATCH: Split into two pools:
      scored_arts -- stage3_score > 0, sorted DESC -- for Bull/Bear/Ostrich/Arb
      weak_arts   -- stage3_score = 0, limit 50    -- for Swan weak signal hunting
    Returns (scored_arts, weak_arts) tuple.
    """
    if not run_id:
        return [], []
    try:
        # Query 1: scored articles for Bull/Bear/Ostrich/Arbitrator
        scored_result = client.table('pipeline_articles') \
            .select('*') \
            .eq('run_id', run_id) \
            .eq('stage1b_passed', True) \
            .gt('stage3_score', 0) \
            .order('stage3_score', desc=True) \
            .execute()

        # Query 2: weak signal articles for Swan
        weak_result = client.table('pipeline_articles') \
            .select('*') \
            .eq('run_id', run_id) \
            .eq('stage1b_passed', True) \
            .lte('stage3_score', 0) \
            .limit(50) \
            .execute()

        scored_arts = scored_result.data or []
        weak_arts = weak_result.data or []
        print(f'  Fetched {len(scored_arts)} scored articles + {len(weak_arts)} weak signals for MAD context')
        return scored_arts, weak_arts

    except Exception as e:
        print('  Warning: Could not fetch articles: ' + str(e)[:60])
        return [], []


def _fetch_run_id_for_report(client, report_id):
    """Find the pipeline run associated with this report."""
    try:
        result = client.table('pipeline_runs') \
            .select('id') \
            .eq('report_id', report_id) \
            .order('created_at', desc=True) \
            .limit(1) \
            .execute()
        if result.data:
            return result.data[0]['id']
    except Exception as e:
        print('  Warning: Could not fetch run_id: ' + str(e)[:60])
    return None


# ============================================================
# GT-5 E-1a (S73) -- save-time grounding scoring.
# The fabrication loop is: save -> history -> prior authority -> repeat.
# _get_debate_history reads reports.mad_*_case, so an ungrounded case saved
# today comes back tomorrow as prior authority and the Arbitrator repeats it.
# Scoring HERE -- at the real write site, on the exact strings being written
# (post-_validate_mad_output) -- is what lets COMMIT 2 skip a poisoned snippet
# at read time. Detect-only: no text altered, no other field touched.
# ============================================================
_MAD_CASE_FIELDS = ('mad_bull_case', 'mad_bear_case',
                    'mad_black_swan_case', 'mad_ostrich_case')


def _score_mad_grounding(report: dict, mad_result: dict,
                         scored_arts: list, weak_arts: list):
    """Score each mad_*_case against the basket the debate was grounded in.

    Returns {field: {'hit_count': n, 'hits': [...]}}, or None on ANY failure.

    FAIL-OPEN BY CONTRACT: None means the caller writes no column value at all,
    leaving mad_grounding_hits NULL. NULL reads downstream as 'unscored / honest
    unknown', never as 'scored clean' -- so a scoring failure can never silently
    certify a fabricated case as grounded.
    """
    try:
        from analysis.mad_grounding_gate import check_grounding
        from analysis.mad_protocol import build_grounding_whitelist
        # Same basket AND same whitelist the debate's own shadow seams used.
        # Basket: scored pool + Swan's weak-signal pool. Whitelist: the shared
        # build_grounding_whitelist() contract -- NOT a hand-copy, so a change to
        # the Swan FALLOUT template can never leave save-time scoring behind
        # flagging every compliant Swan case as fabrication.
        basket = list(scored_arts or []) + list(weak_arts or [])
        whitelist = build_grounding_whitelist(report)
        hits = {}
        for field in _MAD_CASE_FIELDS:
            text = mad_result.get(field, '') or ''
            agent = field[len('mad_'):-len('_case')]
            _g = check_grounding(text, basket, whitelist, location='save_' + agent)
            hits[field] = {'hit_count': _g['hit_count'], 'hits': _g['hits']}
        _total = sum(v['hit_count'] for v in hits.values())
        print('  GT-5 save-time grounding: '
              + ', '.join(f.replace('mad_', '').replace('_case', '')
                          + '=' + str(hits[f]['hit_count']) for f in _MAD_CASE_FIELDS)
              + ' (total ' + str(_total) + ' hit(s))')
        return hits
    except Exception as e:
        print('  Warning: save-time grounding scoring failed -- fail-open, '
              'mad_grounding_hits left unscored: ' + str(e)[:80])
        return None


def _update_report_with_mad(client, report_id, mad_result):
    """Update the existing report row with MAD fields."""
    update_fields = {
        'mad_bull_case':             mad_result.get('mad_bull_case', ''),
        'mad_bear_case':             mad_result.get('mad_bear_case', ''),
        'mad_black_swan_case':       mad_result.get('mad_black_swan_case', ''),
        'mad_ostrich_case':          mad_result.get('mad_ostrich_case', ''),
        'mad_verdict':               mad_result.get('mad_verdict', 'neutral'),
        'mad_confidence':            mad_result.get('mad_confidence', 0.5),
        'mad_arb_failed':            mad_result.get('mad_arb_failed', False),
        'mad_reasoning':             mad_result.get('mad_reasoning', ''),
        'mad_blind_spot':            mad_result.get('mad_blind_spot', ''),
        'mad_action_recommendation': mad_result.get('mad_action_recommendation', ''),
        'short_focus_threats':       mad_result.get('short_focus_threats', ''),
        'long_shoot_threats':        mad_result.get('long_shoot_threats', ''),
        'short_verify_days':         mad_result.get('short_verify_days', 14),
        'long_verify_days':          mad_result.get('long_verify_days', 180),
        'mad_round1_positions':      mad_result.get('mad_round1_positions', {}),
        'mad_round2_positions':      mad_result.get('mad_round2_positions', {}),
        'mad_round3_positions':      mad_result.get('mad_round3_positions', {}),
        'mad_arb_feedbacks':         mad_result.get('mad_arb_feedbacks', {}),
        'mad_historian_case':        mad_result.get('mad_historian_case', ''),
        'debate_summary':            mad_result.get('debate_summary', ''),
        'agent_positions':           mad_result.get('agent_positions', {}),
        'key_disagreements':         mad_result.get('key_disagreements', ''),
        'consensus_path':            mad_result.get('consensus_path', ''),
        'mad_risk_case':             mad_result.get('mad_risk_case', ''),
    }
    # GT-5 E-1a: additive jsonb. Key ABSENT when scoring failed or did not run --
    # an omitted key leaves the column NULL (= unscored), whereas writing an
    # explicit null would look identical to a real 'no hits' result. Never claim
    # 'scored clean' on a scoring failure.
    _grounding = mad_result.get('mad_grounding_hits')
    if _grounding is not None:
        update_fields['mad_grounding_hits'] = _grounding
    try:
        client.table('reports').update(update_fields).eq('id', report_id).execute()
        print('  OK Report updated: verdict=' + update_fields['mad_verdict'] +
              ' confidence=' + str(update_fields['mad_confidence']))
        return True
    except Exception as e:
        print('  ERROR updating report: ' + str(e))
        return False


def _save_mad_predictions(client, report_id, mad_result):
    """Save MAD predictions to debate_predictions table."""
    try:
        from analysis.mad_protocol import _save_predictions
        _save_predictions(
            report_id=report_id,
            short=mad_result.get('short_focus_threats', ''),
            long_s=mad_result.get('long_shoot_threats', ''),
            short_days=mad_result.get('short_verify_days', 14),
            long_days=mad_result.get('long_verify_days', 180),
            round3=mad_result.get('mad_round3_positions', {}),
        )
    except Exception as e:
        print('  Warning: Could not save predictions: ' + str(e)[:60])


def _log_safety_event_runner(event_type: str, detail: str) -> None:
    """
    COMMIT 1: mirror of mad_protocol._log_safety_event -- IDENTICAL 6-field
    runtime_logs shape, silent try/except, independent of mad_protocol so the
    runner does not import the Groq client just to log.
    """
    try:
        from supabase import create_client
        sb = create_client(
            os.getenv('SUPABASE_URL', ''),
            os.getenv('SUPABASE_SERVICE_KEY', '')
        )
        sb.table('runtime_logs').insert({
            'status':                event_type,
            'error_message':         detail,
            'articles_collected':    0,
            'articles_after_funnel': 0,
            'reports_saved':         0,
            'step_timings':          '{}',
        }).execute()
    except Exception:
        pass


def _compute_mad_succeeded(mad_result: dict) -> bool:
    """
    COMMIT 1: single decision point for whether a MAD run counts as a real
    success for scoring/prediction purposes.

    mad_arb_failed is an ABSOLUTE VETO: a run without a genuine Arbitrator
    verdict has NOT succeeded, regardless of how healthy the agent cases are.
    (Closes the old leak where bool(mad_bull_case) flipped success True on an
    Arbitrator-only failure.)
    """
    if mad_result.get('mad_arb_failed', False):
        return False
    verdict = mad_result.get('mad_verdict', 'neutral')
    confidence = mad_result.get('mad_confidence', 0.5)
    return (
        verdict in ('bullish', 'bearish') or
        (verdict == 'neutral' and confidence != 0.5) or
        bool(mad_result.get('mad_bull_case', ''))
    )


def _assert_mad_integrity(mad_succeeded: bool, mad_arb_failed: bool) -> None:
    """
    COMMIT 1 canary. After _compute_mad_succeeded vetoes on mad_arb_failed,
    the combination (mad_succeeded AND mad_arb_failed) is structurally
    impossible. If it ever fires, a regression has reopened the false-neutral
    hole -- shout loudly and log it instead of silently polluting data.
    """
    if mad_succeeded and mad_arb_failed:
        print('  ALERT INTEGRITY VIOLATION: mad_succeeded=True while mad_arb_failed=True '
              '-- false-neutral guard regressed; scoring/predictions must NOT proceed')
        _log_safety_event_runner(
            'integrity_violation',
            'mad_succeeded && mad_arb_failed -- COMMIT-1 false-neutral guard breached'
        )


def _mad_telegram_text(report, mad_result) -> str:
    """
    COMMIT 1: build the Telegram body. On Arbitrator failure, send an HONEST
    'incomplete' notice instead of a fake NEUTRAL verdict card.
    """
    if mad_result.get('mad_arb_failed', False):
        msg = '[GNI MAD] WARNING -- INCOMPLETE\n'
        msg += 'Report: ' + report.get('title', '')[:60] + '\n'
        msg += 'Arbitrator rate-limited/failed -- no verdict this run.\n'
        return msg

    verdict = mad_result.get('mad_verdict', 'neutral').upper()
    confidence = int(mad_result.get('mad_confidence', 0.5) * 100)
    blind_spot = mad_result.get('mad_blind_spot', '')[:100]
    action = mad_result.get('mad_action_recommendation', '')[:150]
    short_focus = mad_result.get('short_focus_threats', '')[:150]

    emoji = {'BULLISH': 'BULL', 'BEARISH': 'BEAR', 'NEUTRAL': 'NEUTRAL'}.get(verdict, 'NEUTRAL')

    msg = '[GNI MAD VERDICT] ' + emoji + '\n'
    msg += 'Report: ' + report.get('title', '')[:60] + '\n'
    msg += 'Verdict: ' + verdict + ' (' + str(confidence) + '% confidence)\n'
    if blind_spot:
        msg += 'Blind Spot: ' + blind_spot + '\n'
    if short_focus:
        msg += 'Short Focus: ' + short_focus + '\n'
    if action:
        msg += 'Action: ' + action + '\n'
    return msg


def _send_mad_telegram(report, mad_result):
    """Send Telegram with MAD verdict (or honest 'incomplete' notice on failure)."""
    import requests
    token = os.getenv('TELEGRAM_BOT_TOKEN', '')
    chat_id = os.getenv('TELEGRAM_ADMIN_ID', os.getenv('TELEGRAM_QSChannel_ID', ''))
    if not token or not chat_id:
        return

    msg = _mad_telegram_text(report, mad_result)

    try:
        requests.post(
            'https://api.telegram.org/bot' + token + '/sendMessage',
            json={'chat_id': chat_id, 'text': msg},
            timeout=10
        )
        print('  OK MAD Telegram sent')
    except Exception as e:
        print('  Warning: Telegram failed: ' + str(e)[:60])


def _build_debate_summary(mad_result: dict) -> dict:
    """
    F4: Build 4 derived debate summary fields from mad_result.
    Zero Groq calls -- pure Python transformation of existing data.
    """
    verdict = mad_result.get('mad_verdict', 'neutral').upper()
    confidence = int(mad_result.get('mad_confidence', 0.5) * 100)
    reasoning = mad_result.get('mad_reasoning', '')[:200]
    action = mad_result.get('mad_action_recommendation', '')[:150]
    blind_spot = mad_result.get('mad_blind_spot', '')[:100]

    if verdict in ('BULLISH', 'BEARISH'):
        debate_summary = (
            f'The 4-agent MAD debate reached a {verdict} verdict '
            f'with {confidence}% confidence after 3 coached rounds. '
        )
    else:
        debate_summary = (
            f'The 4-agent MAD debate concluded NEUTRAL ({confidence}% confidence) '
            f'after 3 coached rounds, indicating balanced risk signals. '
        )
    if action:
        debate_summary += f'Recommended action: {action[:100]}.'
    elif reasoning:
        debate_summary += reasoning[:100] + '.'

    round3 = mad_result.get('mad_round3_positions', {})
    agent_positions = {}
    for agent in ['bull', 'bear', 'black_swan', 'ostrich']:
        pos = round3.get(agent, '')
        if pos and not pos.startswith('[Agent error'):
            first = pos.split('.')[0].strip()
            agent_positions[agent] = first[:200] if first else pos[:200]
        else:
            agent_positions[agent] = ''

    round1 = mad_result.get('mad_round1_positions', {})
    disagreements = []
    for agent in ['bull', 'bear', 'black_swan', 'ostrich']:
        r1 = round1.get(agent, '')
        r3 = round3.get(agent, '')
        if r1 and r3 and not r3.startswith('[Agent error'):
            disagreements.append(agent.replace('_', ' ').title())
    if len(disagreements) >= 3:
        key_disagreements = (
            f'Significant debate across all agents: '
            f'{", ".join(disagreements)}. '
            f'Blind spot flagged: {blind_spot[:80]}.' if blind_spot else
            f'Significant debate across all agents: {", ".join(disagreements)}.'
        )
    elif len(disagreements) >= 1:
        key_disagreements = (
            f'Primary tension between {" and ".join(disagreements)} perspectives.'
        )
    else:
        key_disagreements = 'Debate inconclusive -- agents returned fallback positions.'

    r1_valid = sum(1 for a in ['bull', 'bear', 'black_swan', 'ostrich']
                   if round1.get(a) and not round1.get(a, '').startswith('['))
    r3_valid = sum(1 for a in ['bull', 'bear', 'black_swan', 'ostrich']
                   if round3.get(a) and not round3.get(a, '').startswith('['))

    if r1_valid >= 4 and r3_valid >= 4:
        consensus_path = (
            f'Round 1: {r1_valid}/4 agents positioned '
            f'-> Round 2: Consultant coaching applied '
            f'-> Round 3: {r3_valid}/4 agents refined '
            f'-> Verdict: {verdict} ({confidence}%)'
        )
    elif r3_valid >= 2:
        consensus_path = (
            f'Partial debate: {r3_valid}/4 agents reached final position '
            f'-> Verdict: {verdict} ({confidence}%)'
        )
    else:
        consensus_path = f'Debate incomplete -> Fallback verdict: {verdict}'

    return {
        'debate_summary':    debate_summary.strip(),
        'agent_positions':   agent_positions,
        'key_disagreements': key_disagreements.strip(),
        'consensus_path':    consensus_path.strip(),
    }


def _wait_for_pipeline_complete(client, report_id, max_attempts=25, poll_interval=60):
    """
    GNI-R-240: Handshake gate -- verify Intelligence completed before MAD runs.
    Polls every 60s for up to 25 minutes (25 attempts).
    """
    db_errors = 0
    for attempt in range(max_attempts):
        try:
            ok = client.table('pipeline_runs').select('status').eq('report_id', report_id).eq('status', 'success').limit(1).execute()
            if ok.data:
                print(f'  OK Handshake confirmed (attempt {attempt+1}/{max_attempts})')
                return True, 'confirmed'
            fail = client.table('pipeline_runs').select('status').eq('report_id', report_id).eq('status', 'failed').limit(1).execute()
            if fail.data:
                print('  Intelligence pipeline FAILED -- skipping MAD cleanly')
                return False, 'failed'
            remaining = max_attempts - attempt - 1
            print(f'  Handshake: Intelligence still running ({attempt+1}/{max_attempts}) -- {remaining} min remaining')
            if attempt < max_attempts - 1:
                time.sleep(poll_interval)
        except Exception as e:
            db_errors += 1
            print(f'  Warning: handshake DB error ({attempt+1}): {str(e)[:60]}')
            if attempt < max_attempts - 1:
                time.sleep(poll_interval)
    if db_errors >= max_attempts:
        print('  Supabase unavailable on all attempts -- skipping MAD')
        return False, 'db_error'
    if db_errors > 0:
        print('  Partial DB errors -- skipping MAD (safe default)')
        return False, 'db_error'
    try:
        rc = client.table('reports').select('created_at').eq('id', report_id).limit(1).execute()
        if rc.data:
            from datetime import datetime as _dt, timezone as _tz
            created = _dt.fromisoformat(rc.data[0]['created_at'].replace('Z', '+00:00'))
            age_min = (_dt.now(_tz.utc) - created).total_seconds() / 60
            if age_min > 15:
                print(f'  Report is {age_min:.0f}min old, no pipeline_runs row -- proceeding')
                return True, 'no_record'
    except Exception:
        pass
    print('  Intelligence still running after 25 min -- exiting cleanly')
    print('  Next MAD cycle (10:30 UTC) will pick this up')
    return False, 'timeout'


def run_mad_pipeline():
    start = datetime.now(timezone.utc)
    print('=' * 60)
    print('?? GNI MAD Pipeline -- Standalone Run')
    print('   Start: ' + start.isoformat())
    print('   GNI-R-110: Separate pipeline = clean Groq TPM window')
    print('=' * 60)

    client = _get_client()
    if not client:
        print('ABORT: Cannot connect to Supabase')
        return False

    mad_account = os.getenv('GNI_MAD_ACCOUNT', 'morning')
    print('  MAD account: ' + mad_account)

    print('\n?? Step 1: Fetching fresh report...')
    report = _fetch_fresh_report(client)
    if not report:
        print('Nothing to do. Exiting cleanly.')
        print('Total time: ' + str(round((datetime.now(timezone.utc) - start).total_seconds(), 2)) + 's')
        return True

    report_id = report['id']

    print('\n  Handshake: Verifying Intelligence pipeline complete...')
    should_proceed, reason = _wait_for_pipeline_complete(client, report_id)
    if not should_proceed:
        print(f'  Handshake exit: {reason} -- MAD skipped cleanly')
        print('  Total time: ' + str(round((datetime.now(timezone.utc) - start).total_seconds(), 2)) + 's')
        return True

    print('\n\U0001f6e1  Quota check (GNI-R-112)...')
    _quota = check_quota('gni_mad', sacred=True, account=mad_account)
    print('  ' + _quota['reason'].split('\n')[0])
    if not _quota['allowed']:
        print('  BLOCKED: Insufficient quota -- exiting cleanly')
        print('  Used today: ' + str(_quota['tokens_used']) + ' tokens')
        print('  Headroom: ' + str(_quota['headroom']) + ' tokens')
        return True
    print('  Used today: ' + str(_quota['tokens_used']) + ' tokens | Headroom: ' + str(_quota['headroom']) + ' tokens')

    # S37 PATCH: fetch returns (scored_arts, weak_arts) tuple
    print('\n?? Step 2: Fetching article context...')
    run_id = _fetch_run_id_for_report(client, report_id)
    scored_arts, weak_arts = _fetch_relevant_articles(client, run_id)

    print('\n???? Step 3: Running Quadratic MAD Protocol...')
    print('   TPM window status: CLEAN (5+ minutes since main pipeline)')
    from analysis.mad_protocol import run_mad_protocol, reset_token_usage, get_token_usage
    reset_token_usage()
    # S37 PATCH: pass both pools to run_mad_protocol
    mad_result = run_mad_protocol(
        report,
        all_articles=scored_arts,
        weak_articles=weak_arts,
        report_id=None
    )

    verdict = mad_result.get('mad_verdict', 'neutral')
    confidence = mad_result.get('mad_confidence', 0.5)
    print('   Final verdict: ' + verdict + ' (' + str(round(confidence, 2)) + ')')

    mad_arb_failed = mad_result.get('mad_arb_failed', False)
    mad_succeeded = _compute_mad_succeeded(mad_result)
    _assert_mad_integrity(mad_succeeded, mad_arb_failed)

    if mad_arb_failed:
        print('  WARNING: Arbitrator failed (mad_arb_failed=True) -- run flagged, '
              'excluded from scoring/predictions/counts')

    if not mad_succeeded:
        print('  WARNING: MAD returned fallback defaults -- arbitrator likely failed')
        print('  Report will be updated but debate content may be empty')

    debate_fields = _build_debate_summary(mad_result)
    mad_result.update(debate_fields)

    # GT-5 E-1a: score the exact case strings about to be written, with the
    # debate's own basket still in hand. Runs regardless of mad_succeeded -- a
    # failed-Arbitrator run still writes agent cases that history will read back.
    _grounding_hits = _score_mad_grounding(report, mad_result, scored_arts, weak_arts)
    if _grounding_hits is not None:
        mad_result['mad_grounding_hits'] = _grounding_hits

    print('\n?? Step 4: Updating report with MAD fields...')
    success = _update_report_with_mad(client, report_id, mad_result)

    # Save MAD quality record (Option A -- S37)
    if success and mad_succeeded:
        try:
            from analysis.mad_quality import calculate_mad_quality, save_mad_quality
            quality_record = calculate_mad_quality(mad_result)
            save_mad_quality(client, report_id, quality_record)
        except Exception as _qe:
            print(f'  Warning: MAD quality logging failed: {str(_qe)[:60]}')

    if success and mad_succeeded:
        print('\n?? Step 5: Saving predictions...')
        _save_mad_predictions(client, report_id, mad_result)

    if success:
        print('\n?? Step 6: Sending MAD Telegram...')
        _send_mad_telegram(report, mad_result)

    if success and os.getenv('GITHUB_ACTIONS', 'false').lower() == 'true':
        try:
            import requests as _req
            pat = os.getenv('MYANMAR_DISPATCH_PAT', '')
            if pat:
                resp = _req.post(
                    'https://api.github.com/repos/johnwickiscodingforyou/gni-myanmar/dispatches',
                    headers={
                        'Authorization': f'token {pat}',
                        'Accept': 'application/vnd.github.v3+json',
                        'Content-Type': 'application/json',
                    },
                    json={'event_type': 'mad-pipeline-complete'},
                    timeout=15
                )
                if resp.status_code == 204:
                    print('  OK: Myanmar pipeline dispatch triggered')
                else:
                    print(f'  WARNING: Dispatch returned {resp.status_code}')
            else:
                print('  WARNING: MYANMAR_DISPATCH_PAT not set -- skipping dispatch')
        except Exception as _e:
            print(f'  WARNING: Dispatch failed: {str(_e)[:60]}')

    if os.getenv('GITHUB_ACTIONS', 'false').lower() == 'true':
        try:
            from supabase import create_client as _create_client
            _sb = _create_client(
                os.getenv('SUPABASE_URL', ''),
                os.getenv('SUPABASE_SERVICE_KEY', '')
            )
            _usage = get_token_usage()
            _real_tokens = _usage['total'] or (_usage['prompt'] + _usage['completion'])
            log_usage(_sb, 'gni_mad', _real_tokens, _usage['calls'], report_id or '',
                      account=mad_account)
            print(f'  Metered MAD usage: {_real_tokens} tokens over {_usage["calls"]} calls')
            # S48 cost-divergence assertion -- observability ONLY, never blocks (sacred run already committed).
            _est = mad_result.get('mad_depth_est') or _quota.get('pipeline_cost', 0)
            if _est and (_real_tokens > _est * 1.25 or _real_tokens < _est * 0.75):
                _ratio = round(_real_tokens / _est, 2)
                _msg = ('[GNI MAD] Cost divergence: est=' + str(_est) +
                        ' real=' + str(_real_tokens) + ' ratio=' + str(_ratio) +
                        ' account=' + str(mad_account))
                print('  WARNING: ' + _msg)
                _send_telegram_alert(_msg)
        except Exception as _e:
            print('  WARNING: Could not log usage: ' + str(_e)[:60])

    total = round((datetime.now(timezone.utc) - start).total_seconds(), 2)
    print('\n' + '=' * 60)
    print('  Status:  ' + ('SUCCESS' if success else 'PARTIAL'))
    print('  Verdict: ' + verdict + ' (' + str(round(confidence * 100)) + '% confidence)')
    print('  Time:    ' + str(total) + 's')
    print('=' * 60)
    return success


if __name__ == '__main__':
    ok = run_mad_pipeline()
    sys.exit(0 if ok else 1)
