# -*- coding: utf-8 -*-
# ============================================================
# S111 dry-run -- three verdicts made to follow their own definitions (R59).
# Offline + hermetic: the database client, price fetches and black-swan check are fakes.
#   python ai_engine/tests/dryrun_verdict_math_s111.py
# (A) GPVS: a Bearish report that names USO is judged on SPY, like its accuracy score.
#     SPY falls while oil rises: the pre-R59 verifier marked the 3d and 7d direction wrong.
# (B) The sentiment "95% CI" uses Student t at df = n-1. With two runs the pre-R59 code
#     used 2.576 (a 99% normal z) instead of 12.706, an interval about 4.9x too narrow.
# (C) health_agent: an escalation score at the 10.0 cap is informational and must not
#     make the overall status CRITICAL (item 9.23).
# Against the pre-R59 engine code 5 of the 10 checks fail; all 10 pass after it.
# ============================================================
import ast
import os
import sys
from datetime import datetime, timezone, timedelta

os.environ.setdefault('SUPABASE_URL', '')
os.environ.setdefault('SUPABASE_SERVICE_KEY', '')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))

import analysis.outcome_verifier as ov
from analysis.nexus_analyzer import _calculate_confidence_intervals

_results = []


def check(label, ok):
    _results.append(bool(ok))
    print(('  PASS  ' if ok else '  FAIL  ') + label)


# ---------- (A) GPVS direction ----------
class _Res:
    def __init__(self, data):
        self.data = data


class _Query:
    def __init__(self, client, table):
        self.client, self.table, self.row = client, table, None

    def insert(self, row):
        self.row = row
        return self

    def execute(self):
        if self.row is not None:
            self.client.inserted.append((self.table, self.row))
            return _Res([self.row])
        if self.table == 'reports':
            return _Res([self.client.report])
        return _Res([])

    def __getattr__(self, name):
        return lambda *a, **k: self


class _Client:
    def __init__(self, report):
        self.report, self.inserted = report, []

    def table(self, name):
        return _Query(self, name)


MOVES = {('SPY', 3): -2.0, ('SPY', 7): -1.0, ('SPY', 30): -0.5, ('SPY', 180): 1.0,
         ('USO', 3): 6.0, ('USO', 7): 4.0, ('USO', 30): 3.0,
         ('GLD', 3): 1.0, ('GLD', 7): 2.0, ('GLD', 30): 2.0, ('GLD', 180): 5.0}
report = {'id': 'r-test', 'title': 'Strait closure lifts crude, equities slide', 'sentiment': 'Bearish',
          'risk_level': 'HIGH', 'tickers_affected': ['SPY', 'GLD', 'XOM', 'USO'], 'sources': '[]',
          'created_at': (datetime.now(timezone.utc) - timedelta(days=10)).isoformat()}
fake = _Client(report)
ov.get_client = lambda: fake
ov.detect_black_swan = lambda: {'detected': False, 'spy_48h_change': 0.0}
ov.fetch_price_change_with_fallback = lambda t, d: MOVES.get((t, d))
ov.update_source_weight = lambda *a, **k: None
print('(A) GPVS judges the market call on SPY')
ov.verify_pending_outcomes()
rows = [r for t, r in fake.inserted if t == 'prediction_outcomes']
check('one outcome row written (got %d)' % len(rows), len(rows) == 1)
if rows:
    r = rows[0]
    check('direction_correct_3d is True (SPY -2.0%%, USO +6.0%%) - got %r' % r['direction_correct_3d'],
          r['direction_correct_3d'] is True)
    check('direction_correct_7d is True (SPY -1.0%%, USO +4.0%%) - got %r' % r['direction_correct_7d'],
          r['direction_correct_7d'] is True)
    check('accuracy_score 1.0 agrees with the direction - got %r' % r['accuracy_score'],
          r['accuracy_score'] == 1.0)
    check('oil and gold moves are still stored (uso 3d %r, gld 3d %r)' % (r['uso_change_3d'], r['gld_change_3d']),
          r['uso_change_3d'] == 6.0 and r['gld_change_3d'] == 1.0)

# ---------- (B) the CI t value ----------
print('(B) the sentiment CI uses t at df = n-1')
ci2 = _calculate_confidence_intervals([0.30, 0.32])
check('n=2: width %.3f == 2 x 12.706 x 0.01 = 0.254 (pre-R59: 0.052)' % ci2['width'],
      abs(ci2['width'] - 0.254) < 0.002)
ci3 = _calculate_confidence_intervals([0.2, 0.3, 0.4])
want3 = round(2 * 4.303 * 0.1 / 3 ** 0.5, 3)
check('n=3: width %.3f == 2 x 4.303 x 0.1 / sqrt 3 = %.3f (unchanged)' % (ci3['width'], want3),
      abs(ci3['width'] - want3) < 0.002)
ci2w = _calculate_confidence_intervals([-0.2, 0.4])
check('n=2, scores 0.6 apart: clipped to [-1, 1] (got %r, %r)' % (ci2w['lower'], ci2w['upper']),
      ci2w['lower'] == -1.0 and ci2w['upper'] == 1.0)

# ---------- (C) health_agent escalation spike ----------
print('(C) a capped escalation score is informational')
src = open(os.path.join(HERE, '..', 'analysis', 'health_agent.py'), 'rb').read().decode('utf-8')
spike = []
for node in ast.walk(ast.parse(src)):
    if isinstance(node, ast.Dict):
        kv = {getattr(k, 'value', None): getattr(v, 'value', None) for k, v in zip(node.keys, node.values)}
        if kv.get('type') == 'ESCALATION_SPIKE':
            spike.append(kv.get('severity'))
check('ESCALATION_SPIKE alert found once (got %d)' % len(spike), len(spike) == 1)
check('its severity is not HIGH, the level that sets status CRITICAL (got %r)' % (spike[:1],),
      spike[:1] != ['HIGH'] and spike[:1] != ['MEDIUM'])

print('\n' + '=' * 64)
total, ok = len(_results), sum(_results)
print('  RESULT: %d/%d checks passed -- %s' % (ok, total, 'ALL PASS' if ok == total else 'FAILURES PRESENT'))
print('=' * 64)
sys.exit(0 if ok == total else 1)
