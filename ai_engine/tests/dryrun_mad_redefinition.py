# -*- coding: utf-8 -*-
# ============================================================
# PHASE 2 dry-run -- MAD redefinition wiring verification.
# Offline + hermetic (same pattern as Commit 1/2 harnesses).
# ZERO Groq calls, ZERO real waits.
#   python ai_engine/tests/dryrun_mad_redefinition.py
# ============================================================
import os
import sys

os.environ['GITHUB_ACTIONS'] = 'true'
os.environ.setdefault('GROQ_API_KEY', 'test-dummy-key')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))             # ai_engine/
sys.path.insert(0, os.path.join(HERE, '..', 'analysis'))  # ai_engine/analysis/

import analysis.mad_protocol as mp

mp.time.sleep = lambda *a, **k: None      # kill inter-round sleeps
mp._log_safety_event = lambda *a, **k: None
mp._get_debate_history = lambda: {'bull': [], 'bear': [], 'black_swan': [],
                                  'ostrich': [], 'verdict_trend': ''}
mp._save_predictions = lambda *a, **k: None

AGENTS = {'BULL': mp.BULL, 'BEAR': mp.BEAR, 'SWAN': mp.SWAN, 'OSTRICH': mp.OSTRICH}
CONS = {'BULL_CONS': mp.BULL_CONS, 'BEAR_CONS': mp.BEAR_CONS,
        'SWAN_CONS': mp.SWAN_CONS, 'OSTRICH_CONS': mp.OSTRICH_CONS}
ALL_AGENT_CONS = {**AGENTS, **CONS}
NINE = {**AGENTS, **CONS, 'ARB_FINAL': mp.ARB_FINAL}
ALL_ELEVEN = NINE  # 4 agents + 4 consultants + arbitrator = 9 distinct system prompts

_results = []


def check(label, cond):
    _results.append(bool(cond))
    print(f'   [{"PASS" if cond else "FAIL"}] {label}')


# Pre-change Arbitrator JSON schema (verbatim from the prior ARB_FINAL) for byte-identity test.
_JSON_ANCHOR = 'Respond ONLY with valid JSON: '
EXPECTED_SCHEMA = (
    'Respond ONLY with valid JSON: '
    '{"verdict": "bullish or bearish or neutral", '
    '"confidence": 0.40-1.00, '
    '"reasoning": "2-3 sentences incl. confidence calibration basis", '
    '"blind_spot_quadrant": "bull or bear or black_swan or ostrich", '
    '"blind_spot_explanation": "why neglected", '
    '"action_recommendation": "one specific action now", '
    '"short_focus_threats": "threats in 7-30 days", '
    '"short_verify_days": 14, '
    '"long_shoot_threats": "structural threats 3-24 months", '
    '"long_verify_days": 180, '
    '"short_focus_opportunities": "stabilising developments in 7-30 days", '
    '"preparedness_path": "what actors can do to prepare or capture"}'
)

BUG_CLAUSES = ['FOUNDATION CHECK', 'GROUNDING CHECK', 'JURISDICTION CHECK',
               'correct it FIRST', 'redirect it FIRST', 'redirect to the correct one FIRST',
               'fix it before pushing']
PURITY = {'BULL': 'never hedge toward the threat cases',
          'BEAR': 'never soften it toward optimism',
          'SWAN': 'never retreat\nto the obvious known one'.replace('\n', ' '),
          'OSTRICH': 'never drift to the exotic unknown'}

print('=' * 64)
print('  PHASE 2 DRY-RUN -- MAD redefinition wiring')
print('=' * 64)

# ── (a) bug clause GONE from every consultant ──────────────────
print('\n(a) consultant bug clause removed')
for name, txt in CONS.items():
    hits = [c for c in BUG_CLAUSES if c in txt]
    check(f'{name}: no corrector/redirect clause {hits if hits else ""}', not hits)

# ── (b) lens-purity lock in each agent ─────────────────────────
print('\n(b) lens-purity lock present in each agent')
for name, phrase in PURITY.items():
    check(f'{name}: "{phrase}"', phrase in AGENTS[name])

# ── (c) GROUNDING_RULE in all 4 agents + 4 consultants + arbitrator (9) ──
print('\n(c) GROUNDING_RULE present in all 9 prompts')
for name, txt in NINE.items():
    check(f'{name}: grounding rule present', mp.GROUNDING_RULE.strip() in txt)

# ── (d) Arbitrator JSON schema byte-identical ──────────────────
print('\n(d) Arbitrator JSON schema unchanged')
new_schema = mp.ARB_FINAL[mp.ARB_FINAL.index(_JSON_ANCHOR):]
check('schema slice byte-identical to pre-change', new_schema == EXPECTED_SCHEMA)

# ── (e) SENIOR_FOUNDATION in all 9 prompts ─────────────────────
print('\n(e) SENIOR_FOUNDATION present in all 9 prompts')
for name, txt in NINE.items():
    check(f'{name}: foundation present', mp.SENIOR_FOUNDATION.strip() in txt)

# ── (f) per-run system-prompt char/token load (report only) ────
print('\n(f) per-run system-prompt load (report only, NOT a gate)')
# One full run: agents x3 rounds (R1/R2/R3) + consultants x2 (after R1, R2) + 1 arbitrator.
agent_calls = sum(len(t) for t in AGENTS.values()) * 3      # each agent system prompt used 3 rounds
cons_calls = sum(len(t) for t in CONS.values()) * 2         # each consultant used 2 rounds
arb_calls = len(mp.ARB_FINAL) * 1
total_chars = agent_calls + cons_calls + arb_calls
approx_tokens = total_chars // 4
print(f'   agents (4 x 3 rounds):      {agent_calls:>7} chars')
print(f'   consultants (4 x 2 rounds): {cons_calls:>7} chars')
print(f'   arbitrator (1):             {arb_calls:>7} chars')
print(f'   TOTAL system-prompt chars:  {total_chars:>7}')
print(f'   APPROX tokens (chars/4):    {approx_tokens:>7}  (per-call max, NOT per-minute; 12K TPM window)')
print(f'   per-call system-prompt approx: agent~{len(mp.BULL)//4} tok, cons~{len(mp.BULL_CONS)//4} tok, arb~{len(mp.ARB_FINAL)//4} tok')

# ── (g) CONTROL: full mock debate end-to-end -> parseable verdict ──
print('\n(g) control -- full mock debate produces a parseable verdict')
VALID_ARB = (
    '{"verdict": "bearish", "confidence": 0.68, "reasoning": "Agents converge on cited '
    'shipping-insurance repricing; moderate-high on hard evidence.", "blind_spot_quadrant": '
    '"ostrich", "blind_spot_explanation": "regulator silence", "action_recommendation": '
    '"Diversify tanker routing.", "short_focus_threats": "shipping disruption in 7-30 days", '
    '"short_verify_days": 14, "long_shoot_threats": "structural energy realignment", '
    '"long_verify_days": 180, "short_focus_opportunities": "de-escalation talks", '
    '"preparedness_path": "stockpile + bilateral channels"}'
)
AGENT_REPLY = ('The strait remains contested; insurers are repricing tanker cover and two '
               'refiners flagged supply exposure this week, a concrete near-term fragility.')


def fake_create(**kw):
    is_arb = any('ARBITRATOR' in m.get('content', '') for m in kw.get('messages', []))
    content = VALID_ARB if is_arb else AGENT_REPLY
    return type('R', (), {
        'choices': [type('C', (), {'message': type('M', (), {'content': content})()})()],
        'usage': type('U', (), {'prompt_tokens': 100, 'completion_tokens': 50, 'total_tokens': 150})(),
    })()


mp.client = type('FC', (), {'chat': type('CH', (), {
    'completions': type('CP', (), {'create': staticmethod(fake_create)})()})()})()

report = {'title': 'Iran Threatens Hormuz', 'summary': 'forces moved', 'risk_level': 'High',
          'escalation_level': 'CRITICAL', 'location_name': 'Iran'}
res = mp.run_mad_protocol(report, all_articles=[], weak_articles=[], report_id=None)
check('verdict parsed == bearish', res.get('mad_verdict') == 'bearish')
check('confidence parsed == 0.68', abs(float(res.get('mad_confidence')) - 0.68) < 1e-9)
check('mad_arb_failed is False (pipeline intact)', res.get('mad_arb_failed') is False)
check('all 4 agent R3 cases populated',
      all(res.get(f'mad_{a}_case') for a in ['bull', 'bear', 'black_swan', 'ostrich']))

print('\n' + '=' * 64)
total, ok = len(_results), sum(_results)
print(f'  RESULT: {ok}/{total} checks passed -- ' + ('ALL PASS' if ok == total else 'FAILURES PRESENT'))
print('=' * 64)
sys.exit(0 if ok == total else 1)
