# -*- coding: utf-8 -*-
# ============================================================
# GNI S53 Stats Half B -- per-run Groq token accumulator.
# Drives nexus_analyzer's module-level counter via the testable
# _record_usage() helper (no live Groq needed). Proves summation,
# call-count, and the defensive 0-default for a missing usage block.
#
# State is process-global (mirrors a real GHA run), so cases run in
# order and assert CUMULATIVE totals.
#
# Run: python ai_engine/tests/test_token_accumulator.py
# ============================================================

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from analysis import nexus_analyzer as nx

_fails = []


def check(name, cond):
    status = 'PASS' if cond else 'FAIL'
    print(f'  [{status}] {name}')
    if not cond:
        _fails.append(name)


print('S53 Half B -- token accumulator harness\n')

# (i) fresh import -> (0, 0) before any record.
check('(i) fresh getter == (0, 0)', nx.get_run_usage() == (0, 0))

# (ii) three Groq-shaped responses with usage.total_tokens -> (3700, 3).
nx._record_usage({'choices': [{'message': {'content': 'a'}}], 'usage': {'total_tokens': 1000}})
nx._record_usage({'choices': [{'message': {'content': 'b'}}], 'usage': {'total_tokens': 1500}})
nx._record_usage({'choices': [{'message': {'content': 'c'}}], 'usage': {'total_tokens': 1200}})
check('(ii) after 3 records == (3700, 3)  [summation + count]', nx.get_run_usage() == (3700, 3))

# (iii) a response MISSING usage -> count +1, tokens += 0, no crash.
nx._record_usage({'choices': [{'message': {'content': 'd'}}]})  # no 'usage' key
check('(iii) missing-usage: tokens unchanged, count +1 == (3700, 4)', nx.get_run_usage() == (3700, 4))

# (iii-b) usage present but total_tokens missing -> still defensive 0.
nx._record_usage({'usage': {}})
check('(iii-b) usage-without-total: == (3700, 5)', nx.get_run_usage() == (3700, 5))

print()
if _fails:
    print(f'RESULT: {len(_fails)} FAILED -> {_fails}')
    sys.exit(1)
print('RESULT: ALL GREEN')
