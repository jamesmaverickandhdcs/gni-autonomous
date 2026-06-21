# -*- coding: utf-8 -*-
# ============================================================
# COMMIT 2 dry-run -- rate governor (header-aware 429 wait).
# Offline + hermetic: monkeypatched client, spied sleep, dummy key.
# ZERO Groq calls, ZERO real waits.
#   python ai_engine/tests/dryrun_rate_governor.py
# ============================================================
import os
import sys

os.environ['GITHUB_ACTIONS'] = 'true'
os.environ.setdefault('GROQ_API_KEY', 'test-dummy-key')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))             # ai_engine/
sys.path.insert(0, os.path.join(HERE, '..', 'analysis'))  # ai_engine/analysis/

import mad_rate_governor as gov
import analysis.mad_protocol as mp

# ── spy on sleep (records every wait; never actually sleeps) ────
_SLEEPS = []
mp.time.sleep = lambda s: _SLEEPS.append(round(float(s), 3))
mp._log_safety_event = lambda *a, **k: None

GOOD = ('The strait remains contested and insurers are repricing tanker cover '
        'this week, a concrete near-term fragility worth tracking closely now.')
BODY_429 = 'Error 429: rate limit reached for model on tokens per minute (TPM). Please slow down.'


# ── fakes ───────────────────────────────────────────────────────
class _Msg:
    def __init__(self, c): self.message = type('M', (), {'content': c})()


class FakeResponse:
    def __init__(self, content, total=100):
        self.choices = [_Msg(content)]
        self.usage = type('U', (), {'prompt_tokens': 50, 'completion_tokens': 50,
                                    'total_tokens': total})()


class FakeResp429:
    def __init__(self, headers):
        self.headers = dict(headers)
        self.status_code = 429


class FakeRateLimitError(Exception):
    """Mimics groq.RateLimitError: carries .response.headers."""
    def __init__(self, msg, headers):
        super().__init__(msg)
        self.response = FakeResp429(headers)


class RateLimitNoResponse(Exception):
    """429-classified but NO .response attr -- tests the getattr guard."""


class APIConnectionError(Exception):
    pass


class APITimeoutError(Exception):
    pass


class InternalServerError(Exception):
    pass


class BadRequestError(Exception):
    pass


class _Completions:
    def __init__(self, script):
        self._script = script
        self.calls = 0

    def create(self, **kw):
        action = self._script[self.calls] if self.calls < len(self._script) else self._script[-1]
        self.calls += 1
        if isinstance(action, Exception):
            raise action
        return action


class _Chat:
    def __init__(self, comp): self.completions = comp


class FakeClient:
    def __init__(self, script): self.chat = _Chat(_Completions(script))


def run_call(script, expect_json=False):
    """Install scripted client, clear sleep spy, run _call_agent."""
    _SLEEPS.clear()
    mp.client = FakeClient(script)
    result = mp._call_agent('sys', 'user', 400, expect_json)
    return result, list(_SLEEPS)


# ── assertion plumbing ──────────────────────────────────────────
_results = []


def check(label, cond):
    _results.append(bool(cond))
    print(f'   [{"PASS" if cond else "FAIL"}] {label}')


def approx(x, target, tol=0.011):
    return x is not None and abs(x - target) < tol


def in_range(x, lo, hi):
    return x is not None and lo - 1e-6 <= x <= hi + 1e-6


print('=' * 64)
print('  COMMIT 2 DRY-RUN -- rate governor')
print(f'  _MAX_ATTEMPTS={mp._MAX_ATTEMPTS}  CAP_SECONDS={gov.CAP_SECONDS}  '
      f'TOKEN_RESET_MARGIN={gov.TOKEN_RESET_MARGIN}')
print('=' * 64)

# ── (a) parse_groq_duration ─────────────────────────────────────
print('\n(a) parse_groq_duration')
check('"55.73s" -> 55.73',   approx(gov.parse_groq_duration('55.73s'), 55.73))
check('"11m31.2s" -> 691.2', approx(gov.parse_groq_duration('11m31.2s'), 691.2))
check('"4" -> 4.0',          approx(gov.parse_groq_duration('4'), 4.0))
check('"3.675s" -> 3.675',   approx(gov.parse_groq_duration('3.675s'), 3.675))
check('"garbage" -> None',   gov.parse_groq_duration('garbage') is None)
check('"" -> None',          gov.parse_groq_duration('') is None)
check('None -> None',        gov.parse_groq_duration(None) is None)

# ── (b) compute_wait_from_headers ───────────────────────────────
print('\n(b) compute_wait_from_headers')
w_both = gov.compute_wait_from_headers({'x-ratelimit-reset-tokens': '55.73s', 'retry-after': '4'})
check('reset-tokens preferred over retry-after (=55.73+0.5 margin)', approx(w_both, 56.23))
check('result <= CAP_SECONDS', w_both <= gov.CAP_SECONDS)
w_ra = gov.compute_wait_from_headers({'retry-after': '4'})
check('missing reset-tokens -> retry-after = 4.0', approx(w_ra, 4.0))
check('empty headers -> None', gov.compute_wait_from_headers({}) is None)
check('None headers -> None', gov.compute_wait_from_headers(None) is None)
w_path = gov.compute_wait_from_headers({'x-ratelimit-reset-tokens': '999s'})
check('pathological 999s -> capped at 75.0', approx(w_path, 75.0))

# ── (c) compute_backoff ─────────────────────────────────────────
print('\n(c) compute_backoff (jitter reduces up to 15%)')
check('attempt 0 -> [12.75, 15]', in_range(gov.compute_backoff(0), 12.75, 15.0))
check('attempt 1 -> [25.5, 30]',  in_range(gov.compute_backoff(1), 25.5, 30.0))
check('attempt 2 -> [51, 60]',    in_range(gov.compute_backoff(2), 51.0, 60.0))
check('attempt 3 -> [102, 120]',  in_range(gov.compute_backoff(3), 102.0, 120.0))
check('attempt 5 -> capped [102, 120]', in_range(gov.compute_backoff(5), 102.0, 120.0))

# ── (d) exception-429 WITH headers -> waits ~56s, not 40 ────────
print('\n(d) exception-429 with headers')
res, sl = run_call([FakeRateLimitError('Error 429 rate limit',
                                       {'x-ratelimit-reset-tokens': '55.73s', 'retry-after': '4'}),
                    FakeResponse(GOOD)])
check('waited the header value ~56.23s (NOT 40)', len(sl) == 1 and approx(sl[0], 56.23))
check('no flat-40 anywhere', 40.0 not in sl)
check('returned sanitized text after retry', res == GOOD)

# ── (e) body-429 now RETRIES (gap closed) ───────────────────────
print('\n(e) body-429 (guardian-flagged) now retries via backoff')
res, sl = run_call([FakeResponse(BODY_429), FakeResponse(GOOD)])
check('a backoff sleep fired (previously ZERO)', len(sl) == 1 and in_range(sl[0], 12.75, 15.0))
check('returned good text after retry', res == GOOD)

# ── (f) missing-.response paths do not crash (getattr guard) ────
print('\n(f) getattr guard -- exceptions without .response')
res, sl = run_call([APIConnectionError('Connection error.'), FakeResponse(GOOD)])
check('f1 APIConnectionError: one transient backoff, no crash', len(sl) == 1 and res == GOOD)
res, sl = run_call([RateLimitNoResponse('Error 429 rate limit, no response obj'), FakeResponse(GOOD)])
check('f2 429 w/o .response: getattr guard -> backoff, no crash', len(sl) == 1 and res == GOOD
      and in_range(sl[0], 12.75, 15.0))

# ── (g) CONTROL: clean call -> zero waits, text unchanged ───────
print('\n(g) control -- clean happy path')
res, sl = run_call([FakeResponse(GOOD)])
check('zero sleeps', sl == [])
check('returns sanitized text unchanged', res == GOOD)

# ── (h) transient-vs-non-transient (A1 addition) ────────────────
print('\n(h) transient 500 retries once; non-transient 400 returns immediately')
res, sl = run_call([InternalServerError('Error code: 500 internal server error'), FakeResponse(GOOD)])
check('h1 transient 500 -> one backoff retry then success', len(sl) == 1 and res == GOOD)
res, sl = run_call([BadRequestError('Error code: 400 invalid request body')])
check('h2 non-transient 400 -> NO retry, immediate [Agent error]',
      sl == [] and res.startswith('[Agent error'))

# ── COMMIT-1 invariant: exhausted -> [Agent error] (flag still fires) ──
print('\n(inv) COMMIT-1 invariant -- exhausted 429 still returns [Agent error]')
storm = [FakeRateLimitError('Error 429 rate limit',
                            {'x-ratelimit-reset-tokens': '55.73s'})] * (mp._MAX_ATTEMPTS + 1)
res, sl = run_call(storm)
check('all attempts 429 -> returns [Agent error] (mad_arb_failed will fire)',
      res.startswith('[Agent error') and len(sl) == mp._MAX_ATTEMPTS - 1)

# ── summary ─────────────────────────────────────────────────────
print('\n' + '=' * 64)
total, ok = len(_results), sum(_results)
print(f'  RESULT: {ok}/{total} checks passed -- ' + ('ALL PASS' if ok == total else 'FAILURES PRESENT'))
print('=' * 64)
sys.exit(0 if ok == total else 1)
