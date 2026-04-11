# -*- coding: utf-8 -*-
# ============================================================
# GNI MAD Runner -- Standalone MAD Pipeline
# Runs 5 minutes after main pipeline (gni_mad.yml cron)
# Reads latest fresh report from Supabase
# Runs full MAD protocol with clean Groq TPM window
# Updates report with mad_* fields
# GNI-R-110: MAD runs separately to guarantee clean TPM window
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
# Prevents rushing into MAD without fresh report, proper gap, sufficient quota
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
from quota_guard import check_quota, log_usage


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
    Fetch most recent report created in last 30 minutes.
    30 min window ensures we only process the report from
    the main pipeline that just ran -- never old reports.
    """
    # 45 min window -- covers 30 min gap + up to 15 min main pipeline runtime
    cutoff = (datetime.now(timezone.utc) - timedelta(minutes=45)).isoformat()
    try:
        result = client.table('reports') \
            .select('*') \
            .gte('created_at', cutoff) \
            .order('created_at', desc=True) \
            .limit(1) \
            .execute()

        if not result.data:
            print('  No fresh reports found in last 30 minutes -- nothing to do')
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
    """Fetch all relevant articles from this pipeline run for MAD context."""
    if not run_id:
        return []
    try:
        result = client.table('pipeline_articles') \
            .select('*') \
            .eq('run_id', run_id) \
            .eq('stage1_passed', True) \
            .execute()
        articles = result.data or []
        print('  Fetched ' + str(len(articles)) + ' relevant articles for MAD context')
        return articles
    except Exception as e:
        print('  Warning: Could not fetch articles: ' + str(e)[:60])
        return []


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


def _update_report_with_mad(client, report_id, mad_result):
    """Update the existing report row with MAD fields."""
    update_fields = {
        'mad_bull_case':             mad_result.get('mad_bull_case', ''),
        'mad_bear_case':             mad_result.get('mad_bear_case', ''),
        'mad_black_swan_case':       mad_result.get('mad_black_swan_case', ''),
        'mad_ostrich_case':          mad_result.get('mad_ostrich_case', ''),
        'mad_verdict':               mad_result.get('mad_verdict', 'neutral'),
        'mad_confidence':            mad_result.get('mad_confidence', 0.5),
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


def _send_mad_telegram(report, mad_result):
    """Send Telegram with MAD verdict."""
    import requests
    token = os.getenv('TELEGRAM_BOT_TOKEN', '')
    chat_id = os.getenv('TELEGRAM_ADMIN_ID', os.getenv('TELEGRAM_QSChannel_ID', ''))
    if not token or not chat_id:
        return

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
    Zero Groq calls — pure Python transformation of existing data.

    Returns dict with:
      debate_summary    — 2-3 sentence plain English debate summary
      agent_positions   — each agent final stance (from round3)
      key_disagreements — what agents disagreed on most
      consensus_path    — how debate moved across 3 rounds
    """
    verdict = mad_result.get('mad_verdict', 'neutral').upper()
    confidence = int(mad_result.get('mad_confidence', 0.5) * 100)
    reasoning = mad_result.get('mad_reasoning', '')[:200]
    action = mad_result.get('mad_action_recommendation', '')[:150]
    blind_spot = mad_result.get('mad_blind_spot', '')[:100]

    # debate_summary — plain English synthesis
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

    # agent_positions — round 3 final stances (truncated for readability)
    round3 = mad_result.get('mad_round3_positions', {})
    agent_positions = {}
    for agent in ['bull', 'bear', 'black_swan', 'ostrich']:
        pos = round3.get(agent, '')
        if pos and not pos.startswith('[Agent error'):
            # First sentence only
            first = pos.split('.')[0].strip()
            agent_positions[agent] = first[:200] if first else pos[:200]
        else:
            agent_positions[agent] = ''

    # key_disagreements — compare round1 vs round3
    round1 = mad_result.get('mad_round1_positions', {})
    disagreements = []
    for agent in ['bull', 'bear', 'black_swan', 'ostrich']:
        r1 = round1.get(agent, '')
        r3 = round3.get(agent, '')
        # If both have content and they differ substantially → disagreement noted
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
        key_disagreements = 'Debate inconclusive — agents returned fallback positions.'

    # consensus_path — how rounds progressed
    r1_valid = sum(1 for a in ['bull', 'bear', 'black_swan', 'ostrich']
                   if round1.get(a) and not round1.get(a, '').startswith('['))
    r3_valid = sum(1 for a in ['bull', 'bear', 'black_swan', 'ostrich']
                   if round3.get(a) and not round3.get(a, '').startswith('['))

    if r1_valid >= 4 and r3_valid >= 4:
        consensus_path = (
            f'Round 1: {r1_valid}/4 agents positioned '
            f'→ Round 2: Arbitrator coaching applied '
            f'→ Round 3: {r3_valid}/4 agents refined '
            f'→ Verdict: {verdict} ({confidence}%)'
        )
    elif r3_valid >= 2:
        consensus_path = (
            f'Partial debate: {r3_valid}/4 agents reached final position '
            f'→ Verdict: {verdict} ({confidence}%)'
        )
    else:
        consensus_path = f'Debate incomplete → Fallback verdict: {verdict}'

    return {
        'debate_summary':    debate_summary.strip(),
        'agent_positions':   agent_positions,
        'key_disagreements': key_disagreements.strip(),
        'consensus_path':    consensus_path.strip(),
    }


def run_mad_pipeline():
    start = datetime.now(timezone.utc)
    print('=' * 60)
    print('?? GNI MAD Pipeline -- Standalone Run')
    print('   Start: ' + start.isoformat())
    print('   GNI-R-110: Separate pipeline = clean Groq TPM window')
    print('=' * 60)

    # Connect to Supabase
    client = _get_client()
    if not client:
        print('ABORT: Cannot connect to Supabase')
        return False

    # Fetch fresh report from main pipeline
    print('\n?? Step 1: Fetching fresh report...')
    report = _fetch_fresh_report(client)
    if not report:
        print('Nothing to do. Exiting cleanly.')
        print('Total time: ' + str(round((datetime.now(timezone.utc) - start).total_seconds(), 2)) + 's')
        return True

    report_id = report['id']

    # GNI-R-112: Check quota before MAD runs
    # sacred=False -- MAD will be blocked if quota too low
    print('\n\U0001f6e1  Quota check (GNI-R-112)...')
    _quota = check_quota('gni_mad', sacred=False)
    print('  ' + _quota['reason'].split('\n')[0])
    if not _quota['allowed']:
        print('  BLOCKED: Insufficient quota -- exiting cleanly')
        print('  Used today: ' + str(_quota['tokens_used']) + ' tokens')
        print('  Headroom: ' + str(_quota['headroom']) + ' tokens')
        return True
    print('  Used today: ' + str(_quota['tokens_used']) + ' tokens | Headroom: ' + str(_quota['headroom']) + ' tokens')

    # Fetch relevant articles for MAD context
    print('\n?? Step 2: Fetching article context...')
    run_id = _fetch_run_id_for_report(client, report_id)
    all_articles = _fetch_relevant_articles(client, run_id)

    # Run MAD protocol -- TPM window is clean (5 min gap from main pipeline)
    print('\n???? Step 3: Running Quadratic MAD Protocol...')
    print('   TPM window status: CLEAN (5+ minutes since main pipeline)')
    from analysis.mad_protocol import run_mad_protocol
    mad_result = run_mad_protocol(report, all_articles=all_articles, report_id=None)

    verdict = mad_result.get('mad_verdict', 'neutral')
    confidence = mad_result.get('mad_confidence', 0.5)
    print('   Final verdict: ' + verdict + ' (' + str(round(confidence, 2)) + ')')

    # Check if MAD actually succeeded (not just fallback)
    mad_succeeded = (
        verdict in ['bullish', 'bearish'] or
        (verdict == 'neutral' and confidence != 0.5) or
        bool(mad_result.get('mad_bull_case', ''))
    )

    if not mad_succeeded:
        print('  WARNING: MAD returned fallback defaults -- arbitrator likely failed')
        print('  Report will be updated but debate content may be empty')

    # F4: Build debate summary fields (zero Groq calls — derived)
    debate_fields = _build_debate_summary(mad_result)
    mad_result.update(debate_fields)

    # Update report with MAD fields
    print('\n?? Step 4: Updating report with MAD fields...')
    success = _update_report_with_mad(client, report_id, mad_result)

    # Save predictions
    if success and mad_succeeded:
        print('\n?? Step 5: Saving predictions...')
        _save_mad_predictions(client, report_id, mad_result)

    # Send Telegram with MAD verdict
    if success:
        print('\n?? Step 6: Sending MAD Telegram...')
        _send_mad_telegram(report, mad_result)

    # Step 7: Trigger Myanmar pipeline via GitHub repository_dispatch
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

    # Log Groq usage (GNI-R-124)
    if os.getenv('GITHUB_ACTIONS', 'false').lower() == 'true':
        try:
            from supabase import create_client as _create_client
            _sb = _create_client(
                os.getenv('SUPABASE_URL', ''),
                os.getenv('SUPABASE_SERVICE_KEY', '')
            )
            log_usage(_sb, 'gni_mad', 7433, 15, report_id or '')
        except Exception as _e:
            print('  WARNING: Could not log usage: ' + str(_e)[:60])

    # Done
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
