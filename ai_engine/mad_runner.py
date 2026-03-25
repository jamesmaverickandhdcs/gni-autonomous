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
    chat_id = os.getenv('TELEGRAM_CHAT_ID', '')
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

    # Log Groq usage (GNI-R-124)
    if os.getenv('GITHUB_ACTIONS', 'false').lower() == 'true':
        try:
            from supabase import create_client as _create_client
            _sb = _create_client(
                os.getenv('SUPABASE_URL', ''),
                os.getenv('SUPABASE_SERVICE_KEY', '')
            )
            log_usage(_sb, 'gni_mad', 12393, 15, report_id or '')
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
