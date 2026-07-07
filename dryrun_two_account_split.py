# -*- coding: utf-8 -*-
# ============================================================
# S47 dry-run: two-account MAD split -- quota_guard account isolation
# Offline / hermetic. No real Supabase, no real Groq.
# Proves:
#   1. log_usage stamps the account it was given
#   2. get_today_usage filters by account (morning sees only morning,
#      evening sees only evening)
#   3. check_quota(account=...) reads the RIGHT account's bucket, so a
#      heavy morning does NOT block a fresh evening
# Run:  python dryrun_two_account_split.py
# Exit 0 = all asserts pass; nonzero = a failure (do NOT push)
# ============================================================
import os
import sys

os.environ.setdefault('GROQ_API_KEY', 'test-dummy-key')
os.environ.setdefault('GITHUB_ACTIONS', 'true')
os.environ.setdefault('SUPABASE_URL', 'http://dummy')
os.environ.setdefault('SUPABASE_SERVICE_KEY', 'dummy')

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ai_engine'))

import quota_guard


# ---- Fake Supabase client: an in-memory groq_daily_usage table ----
class _FakeResult:
    def __init__(self, data):
        self.data = data


class _FakeQuery:
    def __init__(self, rows):
        self._rows = rows
        self._filters = {}

    def select(self, *_a, **_k):
        return self

    def eq(self, col, val):
        self._filters[col] = val
        return self

    def execute(self):
        out = []
        for r in self._rows:
            if all(r.get(k) == v for k, v in self._filters.items()):
                out.append(r)
        return _FakeResult(out)

    def insert(self, row):
        self._pending = dict(row)
        return self

    def _do_insert(self):
        self._rows.append(self._pending)
        return _FakeResult([self._pending])


class _FakeTable:
    def __init__(self, rows):
        self._rows = rows

    def table(self, _name):
        return _FakeTableQuery(self._rows)


class _FakeTableQuery:
    def __init__(self, rows):
        self._rows = rows
        self._q = _FakeQuery(rows)

    def select(self, *a, **k):
        return self._q.select(*a, **k)

    def insert(self, row):
        q = _FakeQuery(self._rows)
        q.insert(row)
        # execute() on an insert query commits

        class _Ins:
            def __init__(self, outer, payload):
                self._outer = outer
                self._payload = payload

            def execute(self):
                self._outer._rows.append(self._payload)
                return _FakeResult([self._payload])
        return _Ins(self, dict(row))


# Shared in-memory table across the whole test
_ROWS = []
_CLIENT = _FakeTable(_ROWS)

# Force quota_guard to use our fake client everywhere
quota_guard._get_supabase_client = lambda: _CLIENT


def reset():
    _ROWS.clear()


def main():
    failures = []

    # --- Scenario: heavy morning, fresh evening ---
    reset()
    # morning logs a real ~63K MAD + ~6K pipeline
    quota_guard.log_usage(_CLIENT, 'gni_mad', 63005, 21, 'r1', account='morning')
    quota_guard.log_usage(_CLIENT, 'gni_pipeline', 6175, 6, 'r2', account='morning')

    morning_used = quota_guard.get_today_usage(_CLIENT, 'morning')
    evening_used = quota_guard.get_today_usage(_CLIENT, 'evening')

    print('morning_used =', morning_used, '(expect 69180)')
    print('evening_used =', evening_used, '(expect 0)')

    if morning_used != 69180:
        failures.append('morning bucket wrong: ' + str(morning_used))
    if evening_used != 0:
        failures.append('evening bucket not isolated: ' + str(evening_used))

    # --- check_quota: evening must be ALLOWED despite heavy morning ---
    ev = quota_guard.check_quota('gni_mad', sacred=False, account='evening')
    mo = quota_guard.check_quota('gni_mad', sacred=False, account='morning')

    print('evening allowed =', ev['allowed'], '(expect True)  used=', ev['tokens_used'])
    print('morning allowed =', mo['allowed'], '(expect False) used=', mo['tokens_used'])

    # Evening pool is fresh -> with stale 7433 estimate, needed=22433, headroom=85000 -> allowed
    if not ev['allowed']:
        failures.append('evening BLOCKED despite fresh pool -- split broken')
    if ev['tokens_used'] != 0:
        failures.append('evening check read wrong bucket: ' + str(ev['tokens_used']))
    # Morning is at 69180; headroom=85000-69180=15820 < 22433 -> blocked (matches live 15:37 behavior)
    if mo['allowed']:
        failures.append('morning should be blocked at 69180 used (headroom<needed)')
    if mo['tokens_used'] != 69180:
        failures.append('morning check read wrong bucket: ' + str(mo['tokens_used']))

    # --- evening logs its own run; must not leak into morning ---
    quota_guard.log_usage(_CLIENT, 'gni_mad', 63005, 21, 'r3', account='evening')
    morning_after = quota_guard.get_today_usage(_CLIENT, 'morning')
    evening_after = quota_guard.get_today_usage(_CLIENT, 'evening')
    print('after evening run: morning =', morning_after, '(expect 69180), evening =', evening_after, '(expect 63005)')
    if morning_after != 69180:
        failures.append('evening run leaked into morning: ' + str(morning_after))
    if evening_after != 63005:
        failures.append('evening run not recorded: ' + str(evening_after))

    print('-' * 50)
    if failures:
        print('DRY-RUN FAILED:')
        for f in failures:
            print('  - ' + f)
        sys.exit(1)
    print('DRY-RUN PASSED: morning/evening buckets fully isolated.')
    sys.exit(0)


if __name__ == '__main__':
    main()
