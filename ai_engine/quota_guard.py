# -*- coding: utf-8 -*-
# ============================================================
# GNI Quota Guard -- quota_guard.py
# Checks daily Groq token usage before any pipeline run
# Reads from groq_daily_usage table in Supabase
# GNI-R-111: Safe ceiling 85,000 tokens/day
# GNI-R-112: Check quota before every run
# GNI-R-124: Token usage tracked in Supabase groq_daily_usage
# ============================================================

import os
import sys
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

TPD_HARD_LIMIT   = 100000
TPD_SAFE_CEILING =  85000
BUFFER           =  15000

PIPELINE_COSTS = {
    'gni_pipeline': 6175,
    'gni_mad':      7433,   # P4: reduced from 12393 after token compression
    'gni_verify':   0,
    'gni_heartbeat':0,
    'gni_adaptive': 7433,   # P4: matches MAD compressed cost
}

# P6: Soft quota reservations per pipeline (C2 portioning)
# Ensures each sacred pipeline always has its budget available.
# Non-sacred pipelines (adaptive) only run if headroom > their reservation.
# Total reserved: 6175 + 7433 + 7433 = 21041 tokens per full day cycle.
# Safe ceiling: 85000 tokens -- headroom after two full cycles: ~42918 tokens.
PIPELINE_RESERVATIONS = {
    'gni_pipeline': 10000,  # sacred -- always runs (GNI-R-121)
    'gni_mad':      10000,  # sacred -- guaranteed window after pipeline
    'gni_adaptive': 15000,  # non-sacred -- only if sufficient headroom
}


def _get_supabase_client():
    from supabase import create_client
    url = os.getenv('SUPABASE_URL', '')
    key = os.getenv('SUPABASE_SERVICE_KEY', '')
    if not url or not key:
        print('  ERROR: Missing SUPABASE_URL or SUPABASE_SERVICE_KEY')
        return None
    return create_client(url, key)


def get_today_usage(client) -> int:
    today = datetime.now(timezone.utc).date().isoformat()
    try:
        result = client.table('groq_daily_usage') \
            .select('tokens_used') \
            .eq('usage_date', today) \
            .execute()
        total = sum(row['tokens_used'] for row in (result.data or []))
        return total
    except Exception as e:
        print('  ERROR reading groq_daily_usage: ' + str(e)[:80])
        return -1


def log_usage(client, pipeline: str, tokens_used: int,
              requests_used: int, run_id: str = None,
              reason: str = '') -> bool:
    today = datetime.now(timezone.utc).date().isoformat()
    try:
        client.table('groq_daily_usage').insert({
            'usage_date':    today,
            'pipeline':      pipeline,
            'tokens_used':   tokens_used,
            'requests_used': requests_used,
            'run_id':        run_id or '',
            'reason':        reason or '',
        }).execute()
        print('  OK Usage logged: ' + pipeline + ' +' +
              str(tokens_used) + ' tokens, +' + str(requests_used) + ' requests')
        return True
    except Exception as e:
        print('  ERROR logging usage: ' + str(e)[:80])
        return False


def _send_telegram_alert(message: str):
    token   = os.getenv('TELEGRAM_BOT_TOKEN', '')
    chat_id = os.getenv('TELEGRAM_ADMIN_ID', os.getenv('TELEGRAM_QSChannel_ID', ''))
    if not token or not chat_id:
        return
    try:
        requests.post(
            'https://api.telegram.org/bot' + token + '/sendMessage',
            json={'chat_id': chat_id, 'text': message},
            timeout=10
        )
    except Exception:
        pass


def check_quota(pipeline: str, sacred: bool = False) -> dict:
    client = _get_supabase_client()
    if not client:
        return {
            'allowed': True,
            'reason': 'WARNING: Cannot connect to Supabase -- quota check skipped',
            'tokens_used': -1,
            'tokens_remaining': -1,
            'headroom': -1,
            'pipeline_cost': PIPELINE_COSTS.get(pipeline, 0),
        }

    tokens_used = get_today_usage(client)
    pipeline_cost = PIPELINE_COSTS.get(pipeline, 0)

    if tokens_used == -1:
        alert = '[GNI QUOTA] WARNING: Cannot read groq_daily_usage table -- quota unknown'
        print('  ' + alert)
        _send_telegram_alert(alert)
        return {
            'allowed': True,
            'reason': 'WARNING: Cannot read quota table -- allowing with caution',
            'tokens_used': -1,
            'tokens_remaining': -1,
            'headroom': -1,
            'pipeline_cost': pipeline_cost,
        }

    tokens_remaining = TPD_HARD_LIMIT - tokens_used
    headroom = TPD_SAFE_CEILING - tokens_used

    result = {
        'tokens_used':      tokens_used,
        'tokens_remaining': tokens_remaining,
        'headroom':         headroom,
        'pipeline_cost':    pipeline_cost,
    }

    if sacred:
        result['allowed'] = True
        result['reason'] = 'SACRED: Sacred run always permitted (GNI-R-121)'
        if tokens_used > TPD_SAFE_CEILING:
            alert = (
                '[GNI QUOTA] WARNING: Sacred run firing but already above safe ceiling!\n'
                'Used: ' + str(tokens_used) + '/' + str(TPD_HARD_LIMIT) + ' tokens\n'
                'Pipeline: ' + pipeline
            )
            print('  ' + alert)
            _send_telegram_alert(alert)
        return result

    if pipeline_cost == 0:
        result['allowed'] = True
        result['reason'] = 'ZERO COST: Pipeline uses no Groq tokens (GNI-R-114)'
        return result

    needed = pipeline_cost + BUFFER
    if headroom < needed:
        reason = (
            'BLOCKED: Insufficient quota headroom.\n'
            'Used today: ' + str(tokens_used) + ' tokens\n'
            'Safe ceiling: ' + str(TPD_SAFE_CEILING) + ' tokens\n'
            'Headroom: ' + str(headroom) + ' tokens\n'
            'Needed (cost + buffer): ' + str(needed) + ' tokens\n'
            'Action: Skip this run. Wait for midnight UTC reset.'
        )
        alert = (
            '[GNI QUOTA] BLOCKED: ' + pipeline + ' skipped -- insufficient headroom\n'
            'Used: ' + str(tokens_used) + '/' + str(TPD_SAFE_CEILING) + ' (safe ceiling)\n'
            'Headroom: ' + str(headroom) + ' | Needed: ' + str(needed)
        )
        print('  ' + reason)
        _send_telegram_alert(alert)
        result['allowed'] = False
        result['reason'] = reason
        return result

    if tokens_used > (TPD_SAFE_CEILING * 0.75):
        alert = (
            '[GNI QUOTA] WARNING: Approaching safe ceiling\n'
            'Used: ' + str(tokens_used) + '/' + str(TPD_SAFE_CEILING) + ' tokens\n'
            'Headroom: ' + str(headroom) + ' tokens\n'
            'Pipeline: ' + pipeline + ' (cost: ~' + str(pipeline_cost) + ')'
        )
        print('  WARNING: Approaching safe ceiling -- ' + str(tokens_used) +
              '/' + str(TPD_SAFE_CEILING))
        _send_telegram_alert(alert)

    result['allowed'] = True
    result['reason'] = (
        'ALLOWED: Sufficient headroom.\n'
        'Used: ' + str(tokens_used) + ' | Headroom: ' + str(headroom) +
        ' | Cost: ~' + str(pipeline_cost)
    )
    return result


def print_status():
    client = _get_supabase_client()
    if not client:
        print('ERROR: Cannot connect to Supabase')
        return

    tokens_used = get_today_usage(client)
    if tokens_used == -1:
        print('ERROR: Cannot read groq_daily_usage table')
        return

    tokens_remaining = TPD_HARD_LIMIT - tokens_used
    headroom = TPD_SAFE_CEILING - tokens_used
    pct_hard = round(tokens_used / TPD_HARD_LIMIT * 100, 1)
    pct_safe = round(tokens_used / TPD_SAFE_CEILING * 100, 1)

    print('=' * 50)
    print('GNI Quota Status -- ' +
          datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'))
    print('=' * 50)
    print('Used today:      ' + str(tokens_used) + ' tokens')
    print('Hard limit:      ' + str(TPD_HARD_LIMIT) + ' (' + str(pct_hard) + '% used)')
    print('Safe ceiling:    ' + str(TPD_SAFE_CEILING) + ' (' + str(pct_safe) + '% used)')
    print('Headroom left:   ' + str(headroom) + ' tokens')
    print('Remaining:       ' + str(tokens_remaining) + ' tokens')
    print('-' * 50)
    for pipeline, cost in PIPELINE_COSTS.items():
        if cost > 0:
            can_run = 'YES' if headroom >= (cost + BUFFER) else 'NO'
            print('  ' + pipeline.ljust(16) + ' ~' + str(cost) +
                  ' tokens  --> ' + can_run)
    print('=' * 50)


if __name__ == '__main__':
    print_status()
