# -*- coding: utf-8 -*-
# ============================================================
# S111 dry-run -- a sent source alert marks that run's source_health rows.
# Offline + hermetic: a fake Supabase client records calls; Telegram is stubbed.
#   python ai_engine/tests/dryrun_source_alert_sent.py
# Before S111 nothing wrote source_health.alert_sent, so /source-health's red bar
# and History badge could never show. This checks the write path end to end.
# ============================================================
import os
import sys

os.environ.setdefault('SUPABASE_URL', '')
os.environ.setdefault('SUPABASE_SERVICE_KEY', '')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))

import analysis.source_health_monitor as shm

_results = []


def check(label, ok):
    _results.append(bool(ok))
    print(('  PASS  ' if ok else '  FAIL  ') + label)


class _Q:
    """A query builder that records every call and returns itself."""
    def __init__(self, log, table):
        self.log, self.table = log, table

    def __getattr__(self, name):
        def call(*a, **k):
            self.log.append((self.table, name, a))
            return self
        return call

    def execute(self):
        class R:
            data = []
        return R()


class FakeClient:
    def __init__(self):
        self.log = []

    def table(self, name):
        return _Q(self.log, name)


fake = FakeClient()
shm._get_client = lambda: fake
shm._send_admin_message = lambda msg: True
shm._get_active_reserve_name = lambda client, name: ''
shm._should_send_alert = lambda client, name: (True, 5.0)
shm.HEALTH_ALERT_DRY_RUN = False

sources = [{'name': 'Feed A', 'pillar': 'geo', 'url': 'https://a.example/rss'},
           {'name': 'Feed B', 'pillar': 'fin', 'url': 'https://b.example/rss'}]
saved = shm.save_source_counts([], sources, {'Feed A': {'fetch_ok': False, 'raw': 0}})
run_at = getattr(shm, '_LAST_SAVED_RUN_AT', None)
check('save_source_counts stores the run_at it stamped', bool(saved and run_at))

alerted = shm.alert_and_log_failures([{'name': 'Feed A', 'pillar': 'geo', 'avg': 9.0,
                                       'url': 'https://a.example/rss', 'reason': 'fetch failed'}])
check('alert_and_log_failures returns the alerted names (%r)' % (alerted,), alerted == ['Feed A'])

mark = getattr(shm, 'mark_alert_sent', None)
marked = bool(mark and mark(fake, run_at, alerted))
calls = [(op, a) for t, op, a in fake.log if t == 'source_health']
check('an update sets alert_sent True on source_health', marked and ('update', ({'alert_sent': True},)) in calls)
check('it is scoped to this run_at', ('eq', ('run_at', run_at)) in calls)
check('and to the alerted sources only', ('in_', ('source_name', ['Feed A'])) in calls)
check('nothing alerted -> nothing marked', bool(mark) and mark(fake, run_at, []) is False)

print('\n' + '=' * 64)
total, ok = len(_results), sum(_results)
print('  RESULT: %d/%d checks passed -- %s' % (ok, total, 'ALL PASS' if ok == total else 'FAILURES PRESENT'))
print('=' * 64)
sys.exit(0 if ok == total else 1)
