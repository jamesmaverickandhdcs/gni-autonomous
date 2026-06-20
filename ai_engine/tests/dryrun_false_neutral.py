# -*- coding: utf-8 -*-
# ============================================================
# COMMIT 1 dry-run -- false-neutral integrity fix
# Proves (a-e) on forced Arbitrator failure + control (genuine bearish).
# ZERO Groq calls, ZERO sleeps, ZERO DB writes (all stubbed/monkeypatched).
#   python ai_engine/tests/dryrun_false_neutral.py
# ============================================================
import os
import sys
import io
import contextlib

# Skip mad_runner's import-time preflight (which would hit Supabase).
os.environ['GITHUB_ACTIONS'] = 'true'

# Hermetic: satisfy mad_protocol's module-load Groq() client guard without .env.
# setdefault never clobbers a real key. The dummy is NEVER used -- _call_agent and
# _call_arbitrator are monkeypatched below, so no Groq call is ever made.
os.environ.setdefault('GROQ_API_KEY', 'test-dummy-key')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))            # ai_engine/
sys.path.insert(0, os.path.join(HERE, '..', 'analysis'))  # ai_engine/analysis/

import analysis.mad_protocol as mp
import mad_runner as mr

# ── Neutralise all I/O / latency in mad_protocol ────────────────
mp.time.sleep = lambda *_a, **_k: None          # kill ~5 min of inter-round sleeps
mp._log_safety_event = lambda *_a, **_k: None    # no Supabase
mp._get_debate_history = lambda: {'bull': [], 'bear': [], 'black_swan': [],
                                  'ostrich': [], 'verdict_trend': ''}

AGENT_REPLY = ('The strait remains contested; insurers are repricing tanker '
               'cover and two refiners flagged supply exposure this week, a '
               'concrete near-term fragility worth tracking closely now.')

# Every agent/consultant call returns a healthy paragraph -> agent cases NON-EMPTY.
# This is the exact condition that used to leak success=True on arb-only failure.
mp._call_agent = lambda *a, **k: AGENT_REPLY

# Spy on the runner safety-logger so the canary test never touches Supabase.
_LOG_CALLS = []
mr._log_safety_event_runner = lambda et, detail: _LOG_CALLS.append((et, detail))

TEST_REPORT = {'title': 'Iran Threatens Hormuz', 'summary': 'forces moved',
               'risk_level': 'High', 'escalation_level': 'CRITICAL',
               'location_name': 'Iran'}

VALID_ARB_JSON = (
    '{"verdict": "bearish", "confidence": 0.72, '
    '"reasoning": "Agents converge on cited shipping-insurance repricing; '
    'calibrated moderate-high on hard evidence.", '
    '"blind_spot_quadrant": "ostrich", "blind_spot_explanation": "regulator silence", '
    '"action_recommendation": "Diversify tanker routing and pre-position reserves.", '
    '"short_focus_threats": "escalation and shipping disruption in 7-30 days", '
    '"short_verify_days": 14, "long_shoot_threats": "structural energy realignment", '
    '"long_verify_days": 180, "short_focus_opportunities": "de-escalation talks", '
    '"preparedness_path": "stockpile + bilateral channels"}'
)

PASS, FAIL = 'PASS', 'FAIL'
_results = []


def check(label, cond):
    tag = PASS if cond else FAIL
    _results.append(cond)
    print(f'   [{tag}] {label}')


# ============================================================
# CASE 1 -- FORCED ARBITRATOR FAILURE  (proves a-e)
# ============================================================
print('=' * 60)
print('  CASE 1: FORCED ARBITRATOR 429 FAILURE')
print('=' * 60)

mp._call_arbitrator = lambda *a, **k: '[Agent error: rate limit error (429)]'
res_fail = mp.run_mad_protocol(TEST_REPORT, all_articles=[], weak_articles=[], report_id=None)

print('\n  -- assertions --')
# (a) flag set, verdict still neutral default
check('(a) mad_arb_failed is True', res_fail.get('mad_arb_failed') is True)
check("(a) mad_verdict == 'neutral'", res_fail.get('mad_verdict') == 'neutral')
check('(a) agent cases are NON-EMPTY (leak precondition present)',
      bool(res_fail.get('mad_bull_case')) and not res_fail['mad_bull_case'].startswith('[Agent error'))

# (b) gate vetoes despite healthy agents
succeeded_fail = mr._compute_mad_succeeded(res_fail)
check('(b) _compute_mad_succeeded is False (veto beats non-empty bull_case)',
      succeeded_fail is False)

# (c) quality/predictions gate is `if success and mad_succeeded` -> False -> SKIP
quality_pred_gate = (True and succeeded_fail)   # success(DB)=True best-case; gate still False
check('(c) quality/predictions gate (success and mad_succeeded) == False -> SKIPPED',
      quality_pred_gate is False)

# (d) honest telegram -- no fake neutral card
tg_fail = mr._mad_telegram_text(TEST_REPORT, res_fail)
check('(d) telegram says INCOMPLETE', 'INCOMPLETE' in tg_fail)
check('(d) telegram has NO verdict card', ('Verdict:' not in tg_fail) and ('NEUTRAL' not in tg_fail))

# (e) canary trips when forced into the impossible state
_LOG_CALLS.clear()
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    mr._assert_mad_integrity(True, True)   # forced contradiction
canary_out = buf.getvalue()
check('(e) canary printed INTEGRITY VIOLATION', 'INTEGRITY VIOLATION' in canary_out)
check("(e) canary logged status='integrity_violation' (runtime_logs)",
      len(_LOG_CALLS) == 1 and _LOG_CALLS[0][0] == 'integrity_violation')

print('\n  telegram body (failure):')
print('   | ' + tg_fail.replace('\n', '\n   | ').rstrip())


# ============================================================
# CASE 2 -- CONTROL: genuine bearish verdict (must be untouched)
# ============================================================
print('\n' + '=' * 60)
print('  CASE 2: CONTROL -- genuine bearish JSON')
print('=' * 60)

mp._call_arbitrator = lambda *a, **k: VALID_ARB_JSON
res_ok = mp.run_mad_protocol(TEST_REPORT, all_articles=[], weak_articles=[], report_id=None)

print('\n  -- assertions --')
check('mad_arb_failed is False', res_ok.get('mad_arb_failed') is False)
check("mad_verdict == 'bearish'", res_ok.get('mad_verdict') == 'bearish')
check('mad_confidence == 0.72', abs(float(res_ok.get('mad_confidence')) - 0.72) < 1e-9)
succeeded_ok = mr._compute_mad_succeeded(res_ok)
check('_compute_mad_succeeded is True', succeeded_ok is True)

tg_ok = mr._mad_telegram_text(TEST_REPORT, res_ok)
check('telegram shows BEARISH verdict card', ('BEARISH' in tg_ok) and ('Verdict:' in tg_ok))
check('telegram is NOT marked INCOMPLETE', 'INCOMPLETE' not in tg_ok)

# canary silent on the only state that actually occurs (succeeded=True, failed=False)
_LOG_CALLS.clear()
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    mr._assert_mad_integrity(succeeded_ok, res_ok.get('mad_arb_failed'))
check('canary SILENT on genuine run (no print, no log)',
      buf.getvalue() == '' and len(_LOG_CALLS) == 0)

print('\n  telegram body (control):')
print('   | ' + tg_ok.replace('\n', '\n   | ').rstrip())


# ============================================================
print('\n' + '=' * 60)
total, ok = len(_results), sum(_results)
print(f'  RESULT: {ok}/{total} checks passed -- ' + ('ALL PASS' if ok == total else 'FAILURES PRESENT'))
print('=' * 60)
sys.exit(0 if ok == total else 1)
