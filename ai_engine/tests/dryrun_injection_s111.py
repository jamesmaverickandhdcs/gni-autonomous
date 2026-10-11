# -*- coding: utf-8 -*-
# ============================================================
# S111 dry-run -- Stage 1b (intelligence_funnel._check_injection) both ways.
# Offline + hermetic: no network, no database, no LLM.
#   python ai_engine/tests/dryrun_injection_s111.py
# (A) every attack listed under the security page's Pentest Results must REMOVE
#     (read from src/app/security/page.tsx, so the page and this check share one list);
# (B) news sentences built on the phrases that made Stage 1b delete real reporting
#     before S111 (S111_C_INJECT.sql: ~400 articles since 2026-06-16, none an injection)
#     must NOT be removed - PASS, or FLAG where they carry PHI-003 rhetoric.
# Against the pre-S111 patterns, (A) fails 7 of 9 and (B) fails every line.
# ============================================================
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))

from funnel.intelligence_funnel import _check_injection

_results = []


def check(label, ok):
    _results.append(bool(ok))
    print(('  PASS  ' if ok else '  FAIL  ') + label)


page = open(os.path.join(HERE, '..', '..', 'src', 'app', 'security', 'page.tsx'), 'rb').read().decode('utf-8')
blk = page[page.index('Pentest Results'):]
blk = blk[blk.index('{['):blk.index('].map')]
attacks = re.findall(r"'((?:[^'\\]|\\.)*)'", blk)
check('security page lists 9 attacks (found %d)' % len(attacks), len(attacks) == 9)
print('(A) listed attacks must REMOVE')
for a in attacks:
    action = _check_injection({'title': a, 'summary': ''})[0]
    check('%-7s %s' % (action, a), action == 'REMOVE')

NEWS = [
    'Turkey offered to act as a mediator between Kyiv and Moscow at the talks.',
    'The jailbreak freed more than 40 prisoners held by the junta in Chin State.',
    'Analysts warn the strikes could spark a regional war across the Gulf.',
    'Officials fear a domino effect as fighting spreads across the Horn of Africa.',
    'Critics say the new law lets police bypass safety rules during protests.',
    'Some governments pretend to be neutral while arming one side.',
    'The audit at https://example.org/report found password reuse in most ministries.',
    'Obviously the ceasefire depends on what Tehran does next, the envoy said.',
    'You are now a step closer to understanding the sanctions regime, the explainer begins.',
]
print('(B) real-news phrasing must not REMOVE')
for n in NEWS:
    action = _check_injection({'title': n, 'summary': ''})[0]
    check('%-7s %s' % (action, n), action != 'REMOVE')

print('\n' + '=' * 64)
total, ok = len(_results), sum(_results)
print('  RESULT: %d/%d checks passed -- %s' % (ok, total, 'ALL PASS' if ok == total else 'FAILURES PRESENT'))
print('=' * 64)
sys.exit(0 if ok == total else 1)
