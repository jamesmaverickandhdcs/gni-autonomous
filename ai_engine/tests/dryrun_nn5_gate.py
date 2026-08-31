# -*- coding: utf-8 -*-
# ============================================================
# NN-5 GATE DRY-RUN -- item 8.5 (S91)
#
# Proves the gate at mad_protocol.py:989 DISCRIMINATES: that the arbitrator
# prompt is materially different when _high_escalation is False.
#
# WHY TWO ARMS: at CRITICAL/High the True and False paths cannot be told apart
# by looking at one run. A cert that cannot fail is not a cert (R-S90-1).
#
# PROVENANCE OF THE TREATMENT VALUES -- NOT INVENTED:
#   SELECT escalation_level, risk_level, count(*) FROM reports GROUP BY 1,2
#   over the whole 199-row corpus returns exactly one row for which the gate
#   evaluates False: escalation_level='ELEVATED', risk_level='Medium',
#   escalation_score=5.0, created_at=2026-06-22 15:34:56Z. That single stored
#   row is TREATMENT. Every other row in five months is CRITICAL at 10.0.
#   The existing harnesses (dryrun_false_neutral / _mad_redefinition /
#   _rate_governor) all hardcode 'High'/'CRITICAL', so the False arm of this
#   gate has never once been executed by a test.
#
# ZERO Groq calls, ZERO sleeps, ZERO DB writes (all stubbed) -- and the agent
# call count is PRINTED, so "no network" is measured, not asserted.
#
#   python ai_engine/tests/dryrun_nn5_gate.py
# ============================================================
import os
import sys
import io
import contextlib

# Skip import-time preflight that would hit Supabase.
os.environ['GITHUB_ACTIONS'] = 'true'

# Hermetic: satisfy mad_protocol's module-load Groq() client guard without .env.
# setdefault never clobbers a real key. The dummy is NEVER used -- _call_agent
# and _call_arbitrator are monkeypatched below, so no Groq call is ever made.
os.environ.setdefault('GROQ_API_KEY', 'test-dummy-key')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))              # ai_engine/
sys.path.insert(0, os.path.join(HERE, '..', 'analysis'))  # ai_engine/analysis/

import analysis.mad_protocol as mp

# -- Neutralise all I/O / latency in mad_protocol ------------------
mp.time.sleep = lambda *_a, **_k: None
mp._log_safety_event = lambda *_a, **_k: None
mp._get_debate_history = lambda: {'bull': [], 'bear': [], 'black_swan': [],
                                  'ostrich': [], 'verdict_trend': ''}

AGENT_REPLY = ('The strait remains contested; insurers are repricing tanker '
               'cover and two refiners flagged supply exposure this week, a '
               'concrete near-term fragility worth tracking closely now.')

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

# -- Instrumented stubs --------------------------------------------
AGENT_CALLS = []
ARB_CALLS = []


def _spy_agent(*a, **k):
    AGENT_CALLS.append((a, k))
    return AGENT_REPLY


def _spy_arb(*a, **k):
    # Record every argument so the prompt can be inspected without assuming
    # which position it sits in. Signature at L155:
    #   _call_arbitrator(system_prompt, user_prompt, max_tokens, expect_json)
    ARB_CALLS.append((a, k))
    return VALID_ARB_JSON


mp._call_agent = _spy_agent
mp._call_arbitrator = _spy_arb

# -- Article pool ---------------------------------------------------
# NOT optional. run_mad_protocol:714 computes _eff_n from all_articles and
# calls compute_depth(_eff_n); mad_budget_solver.py:70 divides by n_articles,
# so an EMPTY pool raises ZeroDivisionError before the gate is ever reached.
# The three June harnesses all pass all_articles=[] and are therefore DEAD --
# they predate the S51 wiring (c3ce662, 2026-06-27) by six days. Item 5.14.
#
# IDENTICAL in both arms, so the only difference between them is the gate.
# 8 articles, 2 per pillar -> _eff_n=8 -> depth solver returns D=400/OK.
ARTICLES = [
    {'id': 'a%d' % i,
     'title': 'Article %d on shipping and supply exposure' % i,
     'summary': ('Regional carriers report rerouting and higher premiums; '
                 'two refiners flagged near-term supply exposure. ' * 3),
     'content': 'Body text for article %d.' % i,
     'pillar': pillar,
     'stage3_score': 9 - i,
     'source_name': 'TestWire',
     'url': 'https://example.invalid/%d' % i,
     'published_at': '2026-06-22T12:00:00+00:00'}
    for i, pillar in enumerate(['geo', 'geo', 'fin', 'fin',
                                'tech', 'tech', 'other', 'other'])
]

# The one stored row for which the gate is False, and its CRITICAL control.
CONTROL = {'title': 'Iran Threatens Hormuz', 'summary': 'forces moved',
           'risk_level': 'High', 'escalation_level': 'CRITICAL',
           'location_name': 'Iran'}
TREATMENT = {'title': 'Iran Threatens Hormuz', 'summary': 'forces moved',
             'risk_level': 'Medium', 'escalation_level': 'ELEVATED',
             'location_name': 'Iran'}

PASS, FAIL = 'PASS', 'FAIL'
_results = []


def check(label, cond):
    _results.append(bool(cond))
    print('   [%s] %s' % (PASS if cond else FAIL, label))


def _all_text(calls):
    """Flatten every arbitrator argument to one searchable string per call."""
    out = []
    for a, k in calls:
        parts = [str(x) for x in a] + [str(v) for v in k.values()]
        out.append('\n'.join(parts))
    return out


def _final_prompt(calls):
    """The last arbitrator call is the final synthesis (L1151)."""
    if not calls:
        return ''
    return _all_text(calls)[-1]


def run_arm(name, report):
    AGENT_CALLS.clear()
    ARB_CALLS.clear()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        res = mp.run_mad_protocol(report, all_articles=ARTICLES,
                                  weak_articles=ARTICLES[-2:],
                                  report_id=None)
    out = buf.getvalue()
    print('\n' + '=' * 60)
    print('  ARM: %s  (risk_level=%s, escalation_level=%s)'
          % (name, report['risk_level'], report['escalation_level']))
    print('=' * 60)
    print('   agent calls=%d  arbitrator calls=%d  (stubs -- zero network)'
          % (len(AGENT_CALLS), len(ARB_CALLS)))
    for _l in out.splitlines():
        if 'depth solver' in _l:
            print('   %s' % _l.strip())
    return res, out, _all_text(ARB_CALLS), _final_prompt(ARB_CALLS)


# ============================================================
c_res, c_out, c_all, c_final = run_arm('CONTROL', CONTROL)
print('\n  -- assertions --')
check('A1 CONTROL stdout contains the NN-5 print', 'NN-5:' in c_out)
check('A1b CONTROL names 2 hard constraints', '2 hard constraint' in c_out)
check('A2 CONTROL arbitrator prompt contains HARD CONSTRAINTS',
      any('HARD CONSTRAINTS' in t for t in c_all))
if 'NN-5:' in c_out:
    for line in c_out.splitlines():
        if 'NN-5:' in line:
            print('   evidence: %s' % line.strip())

t_res, t_out, t_all, t_final = run_arm('TREATMENT', TREATMENT)
print('\n  -- assertions --')
check('A3 TREATMENT stdout does NOT contain the NN-5 print', 'NN-5:' not in t_out)
check('A4 TREATMENT arbitrator prompt has NO HARD CONSTRAINTS',
      not any('HARD CONSTRAINTS' in t for t in t_all))
check('A5 TREATMENT still returns a verdict (gate closing breaks nothing)',
      isinstance(t_res, dict) and bool(t_res.get('mad_verdict')))
print('   evidence: mad_verdict=%r  mad_arb_failed=%r'
      % (t_res.get('mad_verdict'), t_res.get('mad_arb_failed')))

# ============================================================
# A6 -- item 8.1c's cost, MEASURED. Reported, never asserted.
print('\n' + '=' * 60)
print('  A6: ARBITRATOR PROMPT COST OF THE ALWAYS-ON BRANCH')
print('=' * 60)
print('   CONTROL   final arb prompt: %6d chars' % len(c_final))
print('   TREATMENT final arb prompt: %6d chars' % len(t_final))
print('   MEASURED CHARS SAVED      : %6d' % (len(c_final) - len(t_final)))
print('   (order item 8.1c cites constraint=1092 of ctx_room=4762 in production;')
print('    this harness uses a short stubbed agent reply, so a SMALLER number')
print('    here is expected and is not a contradiction.)')

print('\n' + '=' * 60)
total, ok = len(_results), sum(_results)
print('  RESULT: %d/%d checks passed -- %s'
      % (ok, total, 'ALL PASS' if ok == total else 'FAILURES PRESENT'))
print('=' * 60)
sys.exit(0 if ok == total else 1)
