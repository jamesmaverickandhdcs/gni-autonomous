# ============================================================
# debate_prediction_verifier.py -- I2 ARC B (S56)
# Purpose: the missing prediction-level GPVS verifier. MAD writes rows to
#          debate_predictions with verify_by dates and verified_by='pending';
#          until now NOTHING read them back (write-only table, 358 pending).
# Method:  market_proxy_v1 -- deterministic, $0 tokens, honestly coarse.
#          A threat prediction over [created_at -> verify_by] is judged by
#          SPY's actual move across that window (Yahoo chart API, the same
#          endpoint detect_black_swan already uses):
#            change <= -2.0%          -> materialized      (risk-off move)
#            change >= -1.0%          -> not_materialized  (market shrugged)
#            -2.0% < change < -1.0%   -> inconclusive      (gray band)
#          Thresholds mirror check_escalation_accuracy (GPVS v1.1) bands.
#          This is a PROXY: prose threats are not purely directional; the
#          method name is stored so the UI can say what kind of verdict it is.
# Safety:  DRY-RUN by default (LR-105 pattern) -- prints every verdict,
#          writes NOTHING until --apply. Schema-adaptive updates: reads one
#          live row first and only writes columns that actually exist.
# Run:     python ai_engine/analysis/debate_prediction_verifier.py --inspect
#          python ai_engine/analysis/debate_prediction_verifier.py            # dry-run
#          python ai_engine/analysis/debate_prediction_verifier.py --apply
#          python ai_engine/analysis/debate_prediction_verifier.py --apply --limit 100
# ============================================================
import argparse
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone

from dotenv import load_dotenv
load_dotenv()

METHOD = 'market_proxy_v1'
TICKER = 'SPY'
MATERIALIZED_AT = -2.0     # pct move at/under which a threat 'materialized'
NOT_MATERIALIZED_AT = -1.0  # pct move at/over which the market 'shrugged'
FETCH_GAP_SECONDS = 1.5


def get_client():
    from supabase import create_client
    url = os.getenv('SUPABASE_URL', '')
    key = os.getenv('SUPABASE_SERVICE_KEY', '')
    if not url or not key:
        print('FATAL: SUPABASE_URL / SUPABASE_SERVICE_KEY not set')
        return None
    return create_client(url, key)


_range_cache = {}


def fetch_change_over_range(ticker: str, start_date: str, end_date: str):
    """Pct change of daily closes across [start_date, end_date] (ISO dates).
    Uses Yahoo v8 chart with period1/period2 -- same endpoint family the
    verifier's detect_black_swan already trusts. Cached per window."""
    key = (ticker, start_date, end_date)
    if key in _range_cache:
        return _range_cache[key]
    try:
        p1 = int(datetime.fromisoformat(start_date + 'T00:00:00+00:00').timestamp())
        p2 = int(datetime.fromisoformat(end_date + 'T23:59:59+00:00').timestamp())
        url = ('https://query1.finance.yahoo.com/v8/finance/chart/' + ticker
               + '?interval=1d&period1=' + str(p1) + '&period2=' + str(p2))
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode('utf-8'))
        closes = (data['chart']['result'][0]['indicators']['quote'][0]['close'])
        closes = [c for c in closes if c is not None]
        if len(closes) < 2:
            _range_cache[key] = None
            return None
        change = (closes[-1] - closes[0]) / closes[0] * 100.0
        _range_cache[key] = round(change, 2)
        time.sleep(FETCH_GAP_SECONDS)
        return _range_cache[key]
    except Exception as e:
        print('  WARNING: range fetch failed ' + ticker + ' '
              + start_date + '->' + end_date + ': ' + str(e)[:80])
        _range_cache[key] = None
        return None


def judge(change) -> str:
    if change is None:
        return 'no_data'
    if change <= MATERIALIZED_AT:
        return 'materialized'
    if change >= NOT_MATERIALIZED_AT:
        return 'not_materialized'
    return 'inconclusive'


def inspect(client) -> list:
    """Read one live row; print and return its column names (schema BEV)."""
    res = client.table('debate_predictions').select('*').limit(1).execute()
    if not res.data:
        print('  Table empty -- no schema sample available')
        return []
    cols = sorted(res.data[0].keys())
    print('  debate_predictions columns: ' + ', '.join(cols))
    return cols


def run(apply: bool, limit: int):
    client = get_client()
    if not client:
        return

    print('\n=== GPVS Prediction-Level Verifier (' + METHOD + ') ===')
    mode = 'APPLY (writes verdicts)' if apply else 'DRY-RUN (writes nothing)'
    print('mode: ' + mode + ' | limit: ' + str(limit))

    cols = inspect(client)
    if not cols:
        return
    for needed in ('verify_by', 'verified_by', 'report_id'):
        if needed not in cols:
            print('FATAL: expected column missing: ' + needed)
            return

    today = datetime.now(timezone.utc).date().isoformat()
    res = client.table('debate_predictions') \
        .select('*') \
        .eq('verified_by', 'pending') \
        .lte('verify_by', today) \
        .order('verify_by', desc=False) \
        .limit(limit) \
        .execute()
    rows = res.data or []
    if not rows:
        print('  No due pending predictions. Done.')
        return
    print('  Due pending predictions: ' + str(len(rows)))

    # window start: row's own created_at if the column exists, else the
    # parent report's created_at (one lookup per report_id, cached)
    report_created = {}

    def window_start(row):
        if 'created_at' in row and row.get('created_at'):
            return str(row['created_at'])[:10]
        rid = row['report_id']
        if rid not in report_created:
            rres = client.table('reports').select('created_at') \
                .eq('id', rid).limit(1).execute()
            report_created[rid] = (str(rres.data[0]['created_at'])[:10]
                                   if rres.data else None)
        return report_created[rid]

    counts = {'materialized': 0, 'not_materialized': 0,
              'inconclusive': 0, 'no_data': 0, 'skipped': 0,
              'fossil': 0}
    optional_fields = [f for f in ('outcome', 'market_change_pct',
                                   'verified_at', 'verification_method')
                       if f in cols]
    print('  writable verdict fields present: verified_by'
          + ((', ' + ', '.join(optional_fields)) if optional_fields else ' (only)'))

    for row in rows:
        # S57 I2-b fossil guard: agent-error text is not a prediction.
        # 429 storms write '[Agent error: ...]' into round3 texts and
        # they land here as rows; judging them by SPY poisons accuracy.
        pred_text = str(row.get('prediction', '') or '')
        if (not pred_text.strip()) or \
                pred_text.lstrip().startswith('[Agent error'):
            counts['fossil'] += 1
            print('  FOSSIL          id=' + str(row.get('id', '?'))
                  + ' error/empty prediction -- not judged')
            if apply:
                update = {'verified_by': 'fossil_error_row'}
                if 'outcome' in cols:
                    update['outcome'] = 'error_row'
                if 'verified_at' in cols:
                    update['verified_at'] = \
                        datetime.now(timezone.utc).isoformat()
                try:
                    client.table('debate_predictions').update(update) \
                        .eq('id', row['id']).execute()
                except Exception as e:
                    print('  WARNING: fossil mark failed id='
                          + str(row.get('id')) + ': ' + str(e)[:80])
            continue
        start = window_start(row)
        end = str(row['verify_by'])[:10]
        if not start or start >= end:
            counts['skipped'] += 1
            print('  SKIP id=' + str(row.get('id', '?')) + ' bad window '
                  + str(start) + '->' + end)
            continue
        change = fetch_change_over_range(TICKER, start, end)
        verdict = judge(change)
        counts[verdict] += 1
        print('  ' + verdict.upper().ljust(16)
              + ' ' + str(row.get('agent', '?')).ljust(10)
              + ' ' + str(row.get('horizon', '?')).ljust(5)
              + ' ' + start + '->' + end
              + ' SPY ' + (str(change) + '%' if change is not None else 'n/a')
              + ' | ' + str(row.get('prediction', ''))[:60])
        if apply and verdict != 'no_data':
            update = {'verified_by': METHOD}
            if 'outcome' in cols:
                update['outcome'] = verdict
            else:
                update['verified_by'] = METHOD + '/' + verdict
            if 'accurate' in cols and verdict in ('materialized', 'not_materialized'):
                update['accurate'] = (verdict == 'materialized')
            if 'market_change_pct' in cols:
                update['market_change_pct'] = change
            if 'verified_at' in cols:
                update['verified_at'] = datetime.now(timezone.utc).isoformat()
            try:
                client.table('debate_predictions').update(update) \
                    .eq('id', row['id']).execute()
            except Exception as e:
                print('  WARNING: update failed id=' + str(row.get('id'))
                      + ': ' + str(e)[:80])

    print('\n=== SUMMARY ===')
    for k, v in counts.items():
        print('  ' + k.ljust(18) + str(v))
    print('  yahoo fetches (uncached windows): ' + str(len(_range_cache)))
    if not apply:
        print('  DRY-RUN: nothing written. Re-run with --apply to persist.')
    print('=== DONE GPVS-PRED-VERIFY ===')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true',
                    help='write verdicts (default: dry-run)')
    ap.add_argument('--limit', type=int, default=40,
                    help='max rows per run (backfill throttle)')
    ap.add_argument('--inspect', action='store_true',
                    help='print table columns and exit')
    args = ap.parse_args()
    if args.inspect:
        c = get_client()
        if c:
            inspect(c)
    else:
        run(args.apply, args.limit)
