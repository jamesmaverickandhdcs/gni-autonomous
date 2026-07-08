# ============================================================
# GNI Grounding Watch -- S61 (Tier-A A1: fabrication rate)
# ------------------------------------------------------------
# Daily 7-day digest over mad_quality_log.grounding_hits (the SHADOW output
# of mad_grounding_gate). Counts runs checked, consultant-level hits, arb-level
# hits, and the top fabricated spans. Telegram digest is INFO by default and
# RED only when an ARBITRATOR-LEVEL hit landed in the window (alarm philosophy
# from W12-b: fabrication that reached the published verdict is the alarm class).
#
# ZERO LLM calls -- no Groq account is touched. "not_mad cron slot" means
# schedule placement only (11:13 UTC), never token spend. Pure Supabase read +
# one Telegram POST, fail-closed throughout.
# ============================================================

import os
import sys
from collections import Counter
from datetime import datetime, timezone, timedelta

import requests
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_ADMIN_ID  = os.getenv('TELEGRAM_ADMIN_ID', '') or os.getenv('TELEGRAM_QSChannel_ID', '')

WINDOW_DAYS = 7
TOP_SPANS   = 10


def _safe_print(text: str) -> None:
    """Console echo that survives non-UTF8 terminals (Windows cp1252)."""
    try:
        print(text)
    except UnicodeEncodeError:
        enc = sys.stdout.encoding or 'ascii'
        print(text.encode(enc, 'replace').decode(enc))


def _get_client():
    from supabase import create_client
    url = os.getenv('SUPABASE_URL', '')
    key = os.getenv('SUPABASE_SERVICE_KEY', '')
    if not url or not key:
        return None
    try:
        return create_client(url, key)
    except Exception:
        return None


def _send_admin_message(message: str) -> bool:
    """Fail-closed Telegram send (mirror of source_health_monitor pattern)."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_ADMIN_ID:
        print('  Grounding watch: Telegram creds absent -- digest not sent')
        return False
    try:
        resp = requests.post(
            'https://api.telegram.org/bot' + TELEGRAM_BOT_TOKEN + '/sendMessage',
            json={'chat_id': TELEGRAM_ADMIN_ID, 'text': message, 'parse_mode': 'HTML'},
            timeout=10,
        )
        if resp.status_code != 200:
            print('  Warning: Telegram send HTTP ' + str(resp.status_code)
                  + ': ' + resp.text[:100])
            return False
        return True
    except Exception as e:
        print('  Warning: Telegram send failed: ' + str(e)[:60])
        return False


def _fetch_rows(client):
    """Fetch mad_quality_log rows in the 7-day window. Never raises."""
    if client is None:
        return []
    cutoff = (datetime.now(timezone.utc) - timedelta(days=WINDOW_DAYS)).isoformat()
    try:
        res = (client.table('mad_quality_log')
               .select('created_at, report_id, account, grounding_hits')
               .gte('created_at', cutoff)
               .order('created_at', desc=True)
               .execute())
        return res.data or []
    except Exception as e:
        print('  Warning: grounding_hits query failed: ' + str(e)[:80])
        return []


def _aggregate(rows: list) -> dict:
    """Roll rows up into digest stats. Robust to nulls / legacy rows."""
    stats = {
        'runs_total':      len(rows),
        'runs_checked':    0,      # rows that actually carry a grounding_hits payload
        'consultant_hits': 0,
        'arb_hits':        0,
        'arb_flagged':     [],     # (report_id, spans) with arbitrator-level hits
        'top_spans':       [],
    }
    span_counter = Counter()
    for row in rows:
        gh = row.get('grounding_hits')
        if not isinstance(gh, dict):
            continue
        stats['runs_checked'] += 1
        cons = gh.get('consultant_hits') or []
        arb  = gh.get('arb_hits') or []
        stats['consultant_hits'] += len(cons)
        stats['arb_hits'] += len(arb)
        for hit in cons + arb:
            span = (hit or {}).get('span', '') if isinstance(hit, dict) else ''
            if span:
                span_counter[span.strip().lower()] += 1
        if arb:
            arb_spans = [(h or {}).get('span', '') for h in arb if isinstance(h, dict)]
            stats['arb_flagged'].append(
                (row.get('report_id', '?'), [s for s in arb_spans if s]))
    stats['top_spans'] = span_counter.most_common(TOP_SPANS)
    return stats


def _build_digest(stats: dict) -> tuple:
    """Return (message, is_red)."""
    is_red = stats['arb_hits'] > 0
    head = ('\U0001f534 <b>[GNI Grounding Watch] ARBITRATOR-LEVEL FABRICATION</b>'
            if is_red else 'ℹ️ <b>[GNI Grounding Watch]</b>')
    lines = [
        head,
        f'Window: last {WINDOW_DAYS}d | runs checked: {stats["runs_checked"]}'
        f'/{stats["runs_total"]}',
        f'Consultant-level hits: {stats["consultant_hits"]} | '
        f'Arbitrator-level hits: {stats["arb_hits"]}',
    ]
    if stats['top_spans']:
        top = ', '.join(f'{span} x{n}' for span, n in stats['top_spans'])
        lines.append('Top fabricated spans: ' + top)
    if is_red:
        lines.append('')
        lines.append('ARB HITS (fabrication reached the verdict):')
        for report_id, spans in stats['arb_flagged'][:10]:
            lines.append(f'  - {report_id}: {", ".join(spans)[:200]}')
    return '\n'.join(lines), is_red


def run_grounding_watch() -> bool:
    print('GNI Grounding Watch -- 7d digest')
    client = _get_client()
    if client is None:
        print('  No Supabase client (creds absent) -- running empty-data dry-run')
    rows = _fetch_rows(client)
    stats = _aggregate(rows)
    message, is_red = _build_digest(stats)
    _safe_print('  ' + message.replace('\n', '\n  '))
    # Skip Telegram only when there is genuinely nothing to report AND no client
    # (pure local dry-run). A live 0-hit window still sends an INFO heartbeat.
    if client is None and stats['runs_total'] == 0:
        print('  Dry-run complete -- no send.')
        return True
    _send_admin_message(message)
    return True


if __name__ == '__main__':
    run_grounding_watch()
