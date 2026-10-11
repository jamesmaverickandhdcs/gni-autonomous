# -*- coding: utf-8 -*-
# ============================================================
# S111 dry-run -- the report check's black-swan window is 48 wall-clock hours.
# Offline + hermetic: urllib's urlopen is replaced by a fake SPY chart; no network.
#   python ai_engine/tests/dryrun_black_swan_window.py
# Case A: SPY climbs 6% over five trading days but is flat for the last 48 h -
#         NOT a black swan (the pre-S111 bar slice kept all five days and said yes).
# Case B: SPY falls 6% inside the last 24 h - a black swan.
# Case C: no bars - not detected, no crash.
# ============================================================
import io
import json
import os
import sys
import urllib.request

os.environ.setdefault('SUPABASE_URL', '')
os.environ.setdefault('SUPABASE_SERVICE_KEY', '')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))

import analysis.outcome_verifier as ov

_results = []


def check(label, ok):
    _results.append(bool(ok))
    print(('  PASS  ' if ok else '  FAIL  ') + label)


def trading_hours(days):
    """Hourly bar stamps for `days` trading days, 7 bars each, one day apart."""
    t0 = 1_760_000_000
    return [t0 + d * 86400 + h * 3600 for d in range(days) for h in range(7)]


def fake_chart(stamps, closes):
    body = json.dumps({'chart': {'result': [{'timestamp': stamps,
                                             'indicators': {'quote': [{'close': closes}]}}]}}).encode()

    class _Resp(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    return lambda req, timeout=10: _Resp(body)


stamps = trading_hours(5)                      # 35 bars - fewer than 48
n = len(stamps)
climb = [100.0 + 6.0 * min(i, n - 15) / (n - 15) for i in range(n)]   # +6% then flat
urllib.request.urlopen = fake_chart(stamps, climb)
a = ov.detect_black_swan()
check('A: +6%% over five days, flat in the last 48 h -> not detected (got %s, change %s)'
      % (a['detected'], a['spy_48h_change']), a['detected'] is False)

drop = [100.0] * (n - 5) + [97.0, 96.0, 95.0, 94.5, 94.0]
urllib.request.urlopen = fake_chart(stamps, drop)
b = ov.detect_black_swan()
check('B: -6%% inside the last day -> detected (got %s, change %s)'
      % (b['detected'], b['spy_48h_change']), b['detected'] is True)

urllib.request.urlopen = fake_chart([], [])
c = ov.detect_black_swan()
check('C: no bars -> not detected', c['detected'] is False)

print('\n' + '=' * 64)
total, ok = len(_results), sum(_results)
print('  RESULT: %d/%d checks passed -- %s' % (ok, total, 'ALL PASS' if ok == total else 'FAILURES PRESENT'))
print('=' * 64)
sys.exit(0 if ok == total else 1)
