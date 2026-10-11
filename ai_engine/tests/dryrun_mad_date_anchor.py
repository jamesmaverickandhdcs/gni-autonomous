# -*- coding: utf-8 -*-
# ============================================================
# S111 dry-run -- the MAD agents' date anchor follows the run's clock.
# Offline + hermetic: imports the prompts, makes ZERO Groq calls.
#   python ai_engine/tests/dryrun_mad_date_anchor.py
# Red both ways: (a) a prompt whose 'Current date:' is not this run's month,
# (b) a prompt with no 'Current date:' anchor at all, (c) a fixed year in
# 'all timelines relative to <year>' that is not this run's year.
# ============================================================
import os
import re
import sys
from datetime import datetime, timezone

os.environ['GITHUB_ACTIONS'] = 'true'
os.environ.setdefault('GROQ_API_KEY', 'test-dummy-key')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'analysis'))

import analysis.mad_protocol as mp

_results = []


def check(label, ok):
    _results.append(bool(ok))
    print(('  PASS  ' if ok else '  FAIL  ') + label)


now = datetime.now(timezone.utc)
want_date, want_year = now.strftime('%B %Y'), now.strftime('%Y')
print('run clock (UTC): %s -> want "%s"' % (now.isoformat(timespec='seconds'), want_date))
check('module CURRENT_DATE == run month', mp.CURRENT_DATE == want_date)
check('module CURRENT_YEAR == run year', mp.CURRENT_YEAR == want_year)

for name, txt in (('BULL', mp.BULL), ('BEAR', mp.BEAR), ('SWAN', mp.SWAN), ('OSTRICH', mp.OSTRICH)):
    dates = re.findall(r'Current date: ([A-Z][a-z]+ \d{4})', txt)
    check('%s: exactly one Current date anchor' % name, len(dates) == 1)
    check('%s: anchor == %s' % (name, want_date), dates == [want_date])
    years = re.findall(r'all timelines relative to (\d{4})', txt)
    check('%s: timelines year, if stated, == %s' % (name, want_year), all(y == want_year for y in years))

src = open(os.path.join(HERE, '..', 'analysis', 'mad_protocol.py'), 'rb').read().decode('utf-8-sig')
frozen = re.findall(r"Current date: [A-Z][a-z]+ \d{4}", src)
check('source carries no frozen "Current date: <Month> <Year>" literal (found %d)' % len(frozen), not frozen)

print('\n' + '=' * 64)
total, ok = len(_results), sum(_results)
print('  RESULT: %d/%d checks passed -- %s' % (ok, total, 'ALL PASS' if ok == total else 'FAILURES PRESENT'))
print('=' * 64)
sys.exit(0 if ok == total else 1)
