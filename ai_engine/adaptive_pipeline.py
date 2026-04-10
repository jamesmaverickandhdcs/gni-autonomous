# -*- coding: utf-8 -*-
# ============================================================
# GNI Adaptive Pipeline -- adaptive_pipeline.py
# Triggered by heartbeat when escalation delta >= 2.0
# Adjusts Groq calls by escalation level (GNI-R-115)
# CRITICAL=0 Groq+lightweight, HIGH=4calls, ELEVATED=4calls
# MODERATE=4calls, LOW=19calls (full run)
# GNI-R-112: Check quota before every run
# GNI-R-115: Adaptive interval by escalation level
# GNI-R-118: Avoid blackout windows
# GNI-R-119: NYSE hours -- minimum 4h interval
# GNI-R-122: Protection windows -- suspend
# ============================================================

import os
import sys
import time
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from quota_guard import check_quota, log_usage
from monitoring_pipeline import (
    is_protection_window,
    is_blackout_window,
    is_nyse_hours,
    is_usgov_hours,
    is_high_alert_hours,
    _send_telegram,
    _score_to_level,
)
from analysis.supabase_saver import save_pipeline_run

GITHUB_ACTIONS = os.getenv('GITHUB_ACTIONS', 'false').lower() == 'true'

# ============================================================
# Escalation level --> pipeline mode (GNI-R-115)
# ============================================================
ESCALATION_MODES = {
    'CRITICAL':  {'groq_calls': 0,  'mode': 'lightweight', 'interval_h': 0.5},
    'HIGH':      {'groq_calls': 4,  'mode': 'standard',    'interval_h': 2.0},
    'ELEVATED':  {'groq_calls': 4,  'mode': 'standard',    'interval_h': 4.0},
    'MODERATE':  {'groq_calls': 4,  'mode': 'standard',    'interval_h': 6.0},
    'LOW':       {'groq_calls': 19, 'mode': 'full',         'interval_h': 12.0},
}


def _get_supabase_client():
    from supabase import create_client
    url = os.getenv('SUPABASE_URL', '')
    key = os.getenv('SUPABASE_SERVICE_KEY', '')
    if not url or not key:
        print('  ERROR: Missing Supabase credentials')
        return None
    return create_client(url, key)


def get_latest_escalation_score(client) -> tuple:
    """Returns (score, level) from latest report."""
    try:
        result = client.table('reports') \
            .select('escalation_score,created_at') \
            .not_.is_('escalation_score', 'null') \
            .order('created_at', desc=True) \
            .limit(1) \
            .execute()
        if result.data:
            score = float(result.data[0].get('escalation_score', 5.0))
            level = _score_to_level(score)
            return score, level
    except Exception as e:
        print('  WARNING: Cannot read escalation score: ' + str(e)[:60])
    return 5.0, 'ELEVATED'


def get_last_adaptive_run(client) -> datetime:
    """Get timestamp of last adaptive pipeline run."""
    try:
        result = client.table('pipeline_runs') \
            .select('run_at') \
            .eq('pipeline_type', 'adaptive') \
            .order('run_at', desc=True) \
            .limit(1) \
            .execute()
        if result.data:
            raw = result.data[0].get('run_at', '')
            if raw:
                return datetime.fromisoformat(raw.replace('Z', '+00:00'))
    except Exception as e:
        print('  WARNING: Cannot read last adaptive run: ' + str(e)[:60])
    return datetime.min.replace(tzinfo=timezone.utc)


def run_lightweight_mode(report: dict) -> dict:
    """
    CRITICAL escalation -- zero Groq calls.
    Just reads latest report and sends Telegram alert.
    GNI-R-115: CRITICAL = 0 Groq + 30min heartbeat only.
    """
    print('  Running LIGHTWEIGHT mode -- zero Groq calls')
    score    = report.get('escalation_score', 0)
    title    = report.get('title', '')[:60]
    level    = _score_to_level(float(score))
    msg = (
        '[GNI ADAPTIVE] CRITICAL ESCALATION\n'
        'Score: ' + str(score) + '/10 [' + level + ']\n'
        'Report: ' + title + '\n'
        'Action: System in maximum monitoring mode.\n'
        'Sacred pipeline runs protected. No extra Groq calls.'
    )
    _send_telegram(msg)
    print('  OK Lightweight alert sent -- zero Groq used')
    return {'mode': 'lightweight', 'groq_calls': 0}


def run_standard_mode(client, report: dict, reason: str) -> dict:
    """
    HIGH/ELEVATED/MODERATE -- 4 Groq calls.
    Runs a focused analysis on latest articles.
    """
    print('  Running STANDARD mode -- ~4 Groq calls')
    try:
        from collectors.rss_collector import collect_articles
        from funnel.intelligence_funnel import run_funnel
        from analysis.nexus_analyzer import analyze
        from analysis.escalation_scorer import score_escalation

        # Collect fresh articles
        print('  Collecting fresh articles...')
        articles = collect_articles(max_per_source=10)
        if len(articles) < 5:
            print('  WARNING: Too few articles -- aborting standard mode')
            return {'mode': 'standard', 'groq_calls': 0}

        # Run funnel -- top 5 only (saves tokens)
        top_articles, _ = run_funnel(articles, top_n=5, max_per_source=2)
        if not top_articles:
            print('  WARNING: No articles after funnel')
            return {'mode': 'standard', 'groq_calls': 0}

        # Run analysis -- 1 Groq call
        print('  Running focused analysis (~1 Groq call)...')
        adaptive_report = analyze(top_articles, provider="cerebras")
        if not adaptive_report:
            print('  WARNING: Analysis returned no report')
            return {'mode': 'standard', 'groq_calls': 1}

        # Score escalation -- 0 Groq calls
        escalation = score_escalation(top_articles)
        new_score = escalation['escalation_score']
        new_level = escalation['escalation_level']

        print('  New escalation: ' + new_level + ' (' + str(new_score) + '/10)')

        # Send Telegram
        msg = (
            '[GNI ADAPTIVE] Standard Run Complete\n'
            'Reason: ' + reason[:100] + '\n'
            'New escalation: ' + new_level + ' (' + str(new_score) + '/10)\n'
            'Report: ' + adaptive_report.get('title', '')[:60] + '\n'
            'Sentiment: ' + adaptive_report.get('sentiment', '') + '\n'
            'Risk: ' + adaptive_report.get('risk_level', '')
        )
        _send_telegram(msg)
        print('  OK Standard mode complete')
        return {'mode': 'standard', 'groq_calls': 1}

    except Exception as e:
        print('  ERROR in standard mode: ' + str(e)[:80])
        return {'mode': 'standard', 'groq_calls': 0}



def check_mission_control_flag(client) -> str:
    """
    GNI-R-158: Read latest mission_control_log row.
    If overall_status is CRITICAL or WARNING and row is < 35 min old,
    return a trigger reason string. Otherwise return empty string.
    Mission Control never triggers directly -- adaptive reads and decides.
    GNI-R-157: Mission Control is monitor-only. This is the DB flag pattern.
    """
    try:
        result = client.table('mission_control_log') \
            .select('overall_status,checked_at,issues_found') \
            .order('checked_at', desc=True) \
            .limit(1) \
            .execute()
        if not result.data:
            print('  Mission Control flag: no log rows found')
            return ''
        row = result.data[0]
        status = row.get('overall_status', '')
        checked_at_raw = row.get('checked_at', '')
        issues = row.get('issues_found', 0) or 0
        if status not in ('CRITICAL', 'WARNING'):
            print('  Mission Control flag: status=' + status + ' -- no trigger')
            return ''
        # Parse checked_at
        checked_at = datetime.fromisoformat(checked_at_raw.replace('Z', '+00:00'))
        age_min = (datetime.now(timezone.utc) - checked_at).total_seconds() / 60
        if age_min > 35:
            print('  Mission Control flag: status=' + status + ' but ' + str(round(age_min, 1)) + 'min old -- stale, no trigger')
            return ''
        reason = (
            'Mission Control flag: ' + status +
            ' (' + str(issues) + ' issues) -- ' +
            str(round(age_min, 1)) + 'min ago (GNI-R-158)'
        )
        print('  Mission Control flag: ' + reason)
        return reason
    except Exception as e:
        print('  WARNING: Cannot read mission_control_flag: ' + str(e)[:60])
        return ''

def run_adaptive_pipeline(reason: str = 'scheduled'):
    now = datetime.now(timezone.utc)
    print('=' * 60)
    print('GNI Adaptive Pipeline')
    print('Time:   ' + now.strftime('%Y-%m-%d %H:%M UTC'))
    print('Reason: ' + reason)
    print('=' * 60)

    # -- Protection window check (GNI-R-122)
    if is_protection_window(now):
        print('PROTECTION WINDOW -- adaptive pipeline suspended (GNI-R-122)')
        return True

    # -- Blackout window check (GNI-R-118)
    if is_blackout_window(now):
        print('BLACKOUT WINDOW -- adaptive pipeline suspended (GNI-R-118)')
        return True

    client = _get_supabase_client()
    if not client:
        print('ERROR: Cannot connect to Supabase')
        return False

    # -- Mission Control DB flag check (GNI-R-158)
    print('\nChecking Mission Control flag (GNI-R-158)...')
    mc_reason = check_mission_control_flag(client)
    if mc_reason and not reason.startswith('Mission Control'):
        reason = mc_reason

    # -- Get current escalation level
    score, level = get_latest_escalation_score(client)
    mode_config  = ESCALATION_MODES.get(level, ESCALATION_MODES['ELEVATED'])
    mode         = mode_config['mode']
    interval_h   = mode_config['interval_h']

    print('\nEscalation: ' + level + ' (' + str(score) + '/10)')
    print('Mode:       ' + mode)
    print('Interval:   ' + str(interval_h) + 'h')

    # -- NYSE hours minimum interval check (GNI-R-119)
    if is_high_alert_hours(now) and interval_h < 4.0:
        interval_h = 4.0
        print('NYSE/USGov hours -- minimum interval raised to 4h (GNI-R-119)')

    # -- Check if enough time has passed since last adaptive run
    last_run = get_last_adaptive_run(client)
    hours_since = (now - last_run).total_seconds() / 3600
    print('Last adaptive run: ' + str(round(hours_since, 1)) + 'h ago')

    if hours_since < interval_h and last_run != datetime.min.replace(tzinfo=timezone.utc):
        print('Too soon -- need ' + str(interval_h) + 'h gap, only ' +
              str(round(hours_since, 1)) + 'h since last run')
        print('Exiting cleanly -- next run in ' +
              str(round(interval_h - hours_since, 1)) + 'h')
        return True

    # -- Quota check (GNI-R-112)
    print('\nChecking quota (GNI-R-112)...')
    _quota = check_quota('gni_adaptive', sacred=False)
    print('  ' + _quota['reason'].split('\n')[0])
    if not _quota['allowed']:
        print('  BLOCKED: Insufficient quota -- exiting cleanly')
        return True

    # -- CRITICAL mode -- zero Groq (GNI-R-115)
    if level == 'CRITICAL':
        print('\nCRITICAL escalation -- lightweight mode (GNI-R-115)')
        try:
            report_result = client.table('reports') \
                .select('title,escalation_score') \
                .order('created_at', desc=True) \
                .limit(1) \
                .execute()
            latest_report = report_result.data[0] if report_result.data else {}
        except Exception:
            latest_report = {}
        result = run_lightweight_mode(latest_report)

    # -- STANDARD/FULL mode -- uses Groq
    else:
        print('\nRunning ' + mode.upper() + ' analysis...')
        result = run_standard_mode(client, {}, reason)

    # -- Log this adaptive run so get_last_adaptive_run() finds it
    total = round((datetime.now(timezone.utc) - now).total_seconds(), 2)
    try:
        save_pipeline_run(
            run_at=now.isoformat(),
            report_id=None,
            total_collected=0,
            total_after_relevance=0,
            total_after_dedup=0,
            total_after_funnel=0,
            llm_source='adaptive',
            status='success',
            duration_seconds=total,
            pipeline_type='adaptive',
        )
        print('  OK Adaptive run logged to pipeline_runs')
    except Exception as _e:
        print('  WARNING: Could not log adaptive run: ' + str(_e)[:60])

    # -- Log Groq usage so quota_guard can see adaptive token consumption (GNI-R-131)
    groq_calls = result.get('groq_calls', 0)
    if groq_calls > 0:
        try:
            tokens_estimate = groq_calls * 6175
            log_usage(
                client,
                pipeline='gni_adaptive',
                tokens_used=tokens_estimate,
                requests_used=groq_calls,
                run_id=None,
                reason=reason,
            )
            print('  OK Usage logged: gni_adaptive +' + str(tokens_estimate) + ' tokens, +' + str(groq_calls) + ' requests')
        except Exception as _e2:
            print('  WARNING: Could not log usage: ' + str(_e2)[:60])

    # -- Done
    print('\n' + '=' * 60)
    print('  Status:     SUCCESS')
    print('  Mode:       ' + result.get('mode', mode))
    print('  Groq calls: ~' + str(result.get('groq_calls', 0)))
    print('  Time:       ' + str(total) + 's')
    print('=' * 60)
    return True


if __name__ == '__main__':
    import sys
    reason = sys.argv[1] if len(sys.argv) > 1 else 'manual'
    ok = run_adaptive_pipeline(reason)
    sys.exit(0 if ok else 1)
