# -*- coding: utf-8 -*-
# ============================================================
# GNI Monitoring Pipeline -- monitoring_pipeline.py
# Zero Groq calls -- monitoring is always free (GNI-R-114)
# Runs every 30 min via gni_heartbeat.yml
# Checks escalation delta, NYSE + US Gov hours, triggers adaptive
# GNI-R-114: Heartbeat uses zero Groq -- never add Groq calls here
# GNI-R-116: Trigger adaptive if escalation delta >= 2.0
# GNI-R-118: Adaptive avoids blackout windows
# GNI-R-119: NYSE hours -- minimum 4h adaptive interval
# GNI-R-120: NYSE open + close Telegram alerts always
# GNI-R-122: Protection windows -- suspend non-sacred pipelines
# ============================================================

import os
import sys
import json
import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ============================================================
# Time window constants (all UTC)
# ============================================================
NYSE_OPEN_H,  NYSE_OPEN_M  = 13, 30   # 13:30 UTC
NYSE_CLOSE_H, NYSE_CLOSE_M = 20,  0   # 20:00 UTC

USGOV_OPEN_H,  USGOV_OPEN_M  = 13,  0  # 13:00 UTC (DC 9am ET)
USGOV_CLOSE_H, USGOV_CLOSE_M = 21,  0  # 21:00 UTC (DC 5pm ET)

# Protection windows -- no non-sacred pipelines (GNI-R-122)
# Window 1: 23:00-01:30 UTC (guards 02:00 sacred run)
# Window 2: 09:00-10:45 UTC (guards 10:00 sacred run)
PROTECTION_WINDOWS = [
    (23,  0,  1, 30),   # 23:00 -> 01:30 UTC
    ( 9,  0, 10, 45),   #  09:00 -> 10:45 UTC
]

# Blackout windows for adaptive scheduling (GNI-R-118)
# +-30 min around 02:00 and 10:00 UTC
BLACKOUT_WINDOWS = [
    ( 1, 30,  2, 30),   # 01:30 -> 02:30 UTC
    ( 9, 30, 10, 30),   # 09:30 -> 10:30 UTC
]

# Escalation delta threshold to trigger adaptive (GNI-R-116)
DELTA_THRESHOLD = 2.0


def _get_supabase_client():
    from supabase import create_client
    url = os.getenv('SUPABASE_URL', '')
    key = os.getenv('SUPABASE_SERVICE_KEY', '')
    if not url or not key:
        print('  ERROR: Missing Supabase credentials')
        return None
    return create_client(url, key)


def _send_telegram(message: str):
    token   = os.getenv('TELEGRAM_BOT_TOKEN', '')
    chat_id = os.getenv('TELEGRAM_ADMIN_ID', os.getenv('TELEGRAM_CHAT_ID', ''))
    if not token or not chat_id:
        return
    try:
        requests.post(
            'https://api.telegram.org/bot' + token + '/sendMessage',
            json={'chat_id': chat_id, 'text': message},
            timeout=10
        )
        print('  OK Telegram sent')
    except Exception as e:
        print('  Warning: Telegram failed: ' + str(e)[:60])


def _minutes_since_midnight(h: int, m: int) -> int:
    return h * 60 + m


def _now_in_window(open_h, open_m, close_h, close_m, now_h, now_m) -> bool:
    now_mins   = _minutes_since_midnight(now_h, now_m)
    open_mins  = _minutes_since_midnight(open_h, open_m)
    close_mins = _minutes_since_midnight(close_h, close_m)
    if open_mins <= close_mins:
        return open_mins <= now_mins < close_mins
    else:
        # Wraps midnight (e.g. 23:00 -> 01:30)
        return now_mins >= open_mins or now_mins < close_mins


def is_weekday(now: datetime) -> bool:
    return now.weekday() < 5  # 0=Mon, 4=Fri


def is_nyse_hours(now: datetime) -> bool:
    if not is_weekday(now):
        return False
    return _now_in_window(
        NYSE_OPEN_H, NYSE_OPEN_M,
        NYSE_CLOSE_H, NYSE_CLOSE_M,
        now.hour, now.minute
    )


def is_usgov_hours(now: datetime) -> bool:
    if not is_weekday(now):
        return False
    return _now_in_window(
        USGOV_OPEN_H, USGOV_OPEN_M,
        USGOV_CLOSE_H, USGOV_CLOSE_M,
        now.hour, now.minute
    )


def is_high_alert_hours(now: datetime) -> bool:
    return is_nyse_hours(now) or is_usgov_hours(now)


def is_protection_window(now: datetime) -> bool:
    for (oh, om, ch, cm) in PROTECTION_WINDOWS:
        if _now_in_window(oh, om, ch, cm, now.hour, now.minute):
            return True
    return False


def is_blackout_window(now: datetime) -> bool:
    for (oh, om, ch, cm) in BLACKOUT_WINDOWS:
        if _now_in_window(oh, om, ch, cm, now.hour, now.minute):
            return True
    return False


def get_nyse_transition(now: datetime) -> str:
    """Check if now is NYSE open or close transition (within 5 min)."""
    now_mins = _minutes_since_midnight(now.hour, now.minute)
    open_mins  = _minutes_since_midnight(NYSE_OPEN_H, NYSE_OPEN_M)
    close_mins = _minutes_since_midnight(NYSE_CLOSE_H, NYSE_CLOSE_M)
    if abs(now_mins - open_mins) <= 5 and is_weekday(now):
        return 'OPEN'
    if abs(now_mins - close_mins) <= 5 and is_weekday(now):
        return 'CLOSE'
    return ''


def get_latest_escalation(client) -> dict:
    """Get the two most recent escalation scores from reports table."""
    try:
        result = client.table('reports') \
            .select('id,title,escalation_score,sentiment,mad_verdict,created_at') \
            .not_.is_('escalation_score', 'null') \
            .gt('escalation_score', 0) \
            .order('created_at', desc=True) \
            .limit(2) \
            .execute()
        return result.data or []
    except Exception as e:
        print('  ERROR reading reports: ' + str(e)[:80])
        return []


def trigger_adaptive_pipeline(reason: str):
    """
    Trigger gni_adaptive.yml via GitHub Actions API.
    GNI-R-116: Heartbeat triggers adaptive if delta >= 2.0
    GNI-R-118: Check blackout windows before triggering
    """
    token = os.getenv('GITHUB_TOKEN', '') or os.getenv('GH_PAT', '')
    repo  = os.getenv('GITHUB_REPOSITORY', 'jamesmaverickandhdcs/gni-autonomous')
    if not token:
        print('  WARNING: No GITHUB_TOKEN -- cannot trigger adaptive pipeline')
        return False
    try:
        resp = requests.post(
            'https://api.github.com/repos/' + repo + '/actions/workflows/gni_adaptive.yml/dispatches',
            headers={
                'Authorization': 'Bearer ' + token,
                'Accept': 'application/vnd.github.v3+json',
            },
            json={'ref': 'main', 'inputs': {'reason': reason}},
            timeout=15
        )
        if resp.status_code == 204:
            print('  OK Adaptive pipeline triggered: ' + reason)
            return True
        else:
            print('  WARNING: Adaptive trigger failed: ' + str(resp.status_code))
            return False
    except Exception as e:
        print('  ERROR triggering adaptive: ' + str(e)[:80])
        return False


def _score_to_level(score: float) -> str:
    if score >= 9: return 'CRITICAL'
    if score >= 7: return 'HIGH'
    if score >= 5: return 'ELEVATED'
    if score >= 3: return 'MODERATE'
    return 'LOW'


def check_divergence_alert(client) -> bool:
    """
    I-02: Indirect+Active report -- detect pipeline vs MAD divergence.
    Fires Telegram alert when report sentiment disagrees with MAD verdict.
    """
    try:
        result = client.table('reports') \
            .select('id,title,sentiment,mad_verdict,mad_confidence,escalation_score,created_at') \
            .not_.is_('mad_verdict', 'null') \
            .not_.is_('sentiment', 'null') \
            .order('created_at', desc=True) \
            .limit(1) \
            .execute()

        if not result.data:
            return False

        report = result.data[0]
        sentiment = (report.get('sentiment') or '').lower()
        mad_verdict = (report.get('mad_verdict') or '').lower()
        title = report.get('title', '')[:60]
        esc_score = report.get('escalation_score', 0) or 0
        mad_conf = report.get('mad_confidence', 0) or 0

        # Skip if either is neutral/pending/empty
        if not sentiment or not mad_verdict:
            return False
        if sentiment in ('neutral', 'pending') or mad_verdict in ('neutral', 'pending'):
            return False
        if sentiment == mad_verdict:
            return False

        # Divergence detected!
        msg = (
            '[GNI DIVERGENCE ALERT] Pipeline vs MAD Disagree\n'
            'Report: ' + title + '\n'
            'Report sentiment: ' + sentiment.upper() + '\n'
            'MAD verdict: ' + mad_verdict.upper() +
            ' (confidence: ' + str(round(mad_conf * 100)) + '%)\n'
            'Escalation: ' + str(esc_score) + '/10\n'
            'Action: Investigate divergence -- highest-value signal\n'
            'Time: ' + datetime.now(timezone.utc).strftime('%H:%M UTC')
        )
        print('  DIVERGENCE DETECTED: ' + sentiment.upper() + ' vs ' + mad_verdict.upper())
        _send_telegram(msg)
        return True

    except Exception as e:
        print('  Warning: Divergence check failed: ' + str(e)[:60])
        return False


def run_monitoring_pipeline():
    now = datetime.now(timezone.utc)
    print('=' * 60)
    print('GNI Heartbeat -- Zero Groq Monitoring (GNI-R-114)')
    print('Time: ' + now.strftime('%Y-%m-%d %H:%M UTC'))
    print('=' * 60)

    # -- Check protection window first (GNI-R-122)
    if is_protection_window(now):
        print('PROTECTION WINDOW ACTIVE -- suspending all checks')
        print('Sacred pipeline run imminent -- heartbeat standing down')
        return True

    client = _get_supabase_client()
    if not client:
        print('ERROR: Cannot connect to Supabase')
        return False

    # -- I-02: Divergence alert -- pipeline vs MAD disagree
    print('\nChecking pipeline vs MAD divergence...')
    divergence_found = check_divergence_alert(client)
    if not divergence_found:
        print('  No divergence -- report and MAD aligned')

    # -- NYSE transition alerts (GNI-R-120) -- always fire
    nyse_transition = get_nyse_transition(now)
    if nyse_transition == 'OPEN':
        msg = (
            '[GNI HEARTBEAT] NYSE OPEN\n'
            'Time: ' + now.strftime('%H:%M UTC') + '\n'
            'US markets now open -- monitoring at heightened frequency.\n'
            'Geopolitical events now have direct market impact.'
        )
        print('NYSE OPEN alert firing...')
        _send_telegram(msg)

    elif nyse_transition == 'CLOSE':
        msg = (
            '[GNI HEARTBEAT] NYSE CLOSE\n'
            'Time: ' + now.strftime('%H:%M UTC') + '\n'
            'US markets now closed -- after-hours monitoring continues.\n'
            'Asian markets open in ~3 hours.'
        )
        print('NYSE CLOSE alert firing...')
        _send_telegram(msg)

    # -- Get latest escalation scores
    print('\nChecking escalation scores...')
    reports = get_latest_escalation(client)

    if not reports:
        print('  No reports found -- nothing to compare')
        return True

    latest = reports[0]
    latest_score = float(latest.get('escalation_score', 0))
    latest_level = _score_to_level(latest_score)
    latest_title = latest.get('title', '')[:60]

    print('  Latest:  ' + latest_level + ' (' + str(latest_score) + '/10) -- ' + latest_title)

    # -- Calculate delta if we have two reports
    delta = 0.0
    if len(reports) >= 2:
        prev = reports[1]
        prev_score = float(prev.get('escalation_score', 0))
        delta = abs(latest_score - prev_score)
        direction = 'UP' if latest_score > prev_score else 'DOWN'
        print('  Previous: ' + str(prev_score) + '/10')
        print('  Delta:    ' + str(round(delta, 1)) + ' (' + direction + ')')
    else:
        print('  Only one report -- no delta calculation')

    # -- Current hour context
    nyse_status  = 'OPEN' if is_nyse_hours(now) else 'CLOSED'
    usgov_status = 'OPEN' if is_usgov_hours(now) else 'CLOSED'
    high_alert   = is_high_alert_hours(now)
    blackout     = is_blackout_window(now)

    print('\n  NYSE:    ' + nyse_status)
    print('  US Gov:  ' + usgov_status)
    print('  Blackout window: ' + str(blackout))
    print('  High alert hours: ' + str(high_alert))

    # -- Decide whether to trigger adaptive pipeline (GNI-R-116)
    should_trigger = False
    trigger_reason = ''

    if blackout:
        print('\n  BLACKOUT WINDOW -- adaptive pipeline suspended (GNI-R-118)')
    elif delta >= DELTA_THRESHOLD:
        should_trigger = True
        trigger_reason = (
            'Escalation delta=' + str(round(delta, 1)) +
            ' >= ' + str(DELTA_THRESHOLD) +
            ' | Level: ' + latest_level +
            ' | Score: ' + str(latest_score)
        )
        print('\n  DELTA THRESHOLD MET -- triggering adaptive pipeline')
        print('  Reason: ' + trigger_reason)
    elif latest_level == 'CRITICAL':
        should_trigger = True
        trigger_reason = 'CRITICAL escalation level -- immediate monitoring required'
        print('\n  CRITICAL LEVEL -- triggering adaptive pipeline')
    else:
        print('\n  No trigger needed -- delta=' + str(round(delta, 1)) +
              ' below threshold=' + str(DELTA_THRESHOLD))

    # -- Trigger adaptive if needed
    if should_trigger:
        triggered = trigger_adaptive_pipeline(trigger_reason)
        if triggered:
            alert_msg = (
                '[GNI HEARTBEAT] Adaptive pipeline triggered\n'
                'Reason: ' + trigger_reason + '\n'
                'Time: ' + now.strftime('%H:%M UTC')
            )
            _send_telegram(alert_msg)

    # -- Send periodic status if high alert hours
    if high_alert and not nyse_transition and not should_trigger:
        print('\n  High alert hours -- sending status update')
        status_msg = (
            '[GNI HEARTBEAT] Status Update\n'
            'Time: ' + now.strftime('%H:%M UTC') + '\n'
            'Escalation: ' + latest_level + ' (' + str(latest_score) + '/10)\n'
            'NYSE: ' + nyse_status + ' | US Gov: ' + usgov_status + '\n'
            'Delta: ' + str(round(delta, 1)) + ' (threshold: ' + str(DELTA_THRESHOLD) + ')'
        )
        _send_telegram(status_msg)

    print('\n' + '=' * 60)
    print('  Heartbeat complete -- zero Groq calls used')
    print('  Next check: 30 min')
    print('=' * 60)
    return True


if __name__ == '__main__':
    ok = run_monitoring_pipeline()
    sys.exit(0 if ok else 1)
