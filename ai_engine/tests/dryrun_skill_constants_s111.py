# -*- coding: utf-8 -*-
# ============================================================
# S111 dry-run -- the skill check's critical value matches its significance level (R60).
# Offline + hermetic: reads src/lib/skill.ts as text; standard library only.
#   python ai_engine/tests/dryrun_skill_constants_s111.py
# The pages print PT_CRITICAL and PT_ALPHA from src/lib/skill.ts. A one-sided test at PT_ALPHA
# needs the standard-normal quantile at 1 - PT_ALPHA; this fails if either constant is edited
# without the other. (The PT formula itself was cross-checked against
# statsmodels.stats.diagnostic.pesaran_timmermann at S111: 1.6391 on the 3-day outcomes.)
# ============================================================
import os
import re
import sys
from statistics import NormalDist

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, '..', '..', 'src', 'lib', 'skill.ts'), 'rb').read().decode('utf-8')
_results = []


def check(label, ok):
    _results.append(bool(ok))
    print(('  PASS  ' if ok else '  FAIL  ') + label)


a = re.findall(r'export const PT_ALPHA = ([\d.]+)', src)
c = re.findall(r'export const PT_CRITICAL = ([\d.]+)', src)
check('one PT_ALPHA (found %d) and one PT_CRITICAL (found %d)' % (len(a), len(c)), len(a) == 1 and len(c) == 1)
if a and c:
    want = NormalDist().inv_cdf(1 - float(a[0]))
    check('PT_CRITICAL %s == N^-1(1 - %s) = %.4f to 3 decimals' % (c[0], a[0], want),
          abs(float(c[0]) - want) < 0.0005)

print('\n' + '=' * 64)
total, ok = len(_results), sum(_results)
print('  RESULT: %d/%d checks passed -- %s' % (ok, total, 'ALL PASS' if ok == total else 'FAILURES PRESENT'))
print('=' * 64)
sys.exit(0 if ok == total else 1)
