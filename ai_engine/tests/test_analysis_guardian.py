# -*- coding: utf-8 -*-
# ============================================================
# GNI S53 L6 -- guardian on the nexus_analyzer response path.
# Proves the analysis path can disable ONLY the upper-bound ceiling
# (max_tokens=3000 ~ 12k chars > guardian's 8000) WITHOUT loosening
# the floor or any other check -- and that MAD's default 8000 ceiling
# stays enforced (shared-constant blast-radius guard).
#
# Run: python ai_engine/tests/test_analysis_guardian.py
# ============================================================

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from groq_guardian import validate_response

_fails = []


def check(name, cond):
    status = 'PASS' if cond else 'FAIL'
    print(f'  [{status}] {name}')
    if not cond:
        _fails.append(name)


# Benign filler sentence -- contains NO rate-limit / refusal / injection
# signal strings (no 'rate limit', 'i cannot', 'as an ai', 'ignore previous',
# 'act as', 'you are now', etc.). ~104 chars/repeat.
_FILLER = ("Markets responded to the policy shift as analysts weighed the "
           "regional supply outlook and currency moves. ")

# (i) CLEAN long report ~10,000 chars -- the 3000-token analysis path.
_LONG_VALID = '{"title": "Regional supply outlook", "market_impact": "' + (_FILLER * 96) + '"}'

# (iv) NORMAL report ~2,000 chars -- ordinary case.
_NORMAL = '{"title": "Regional supply outlook", "market_impact": "' + (_FILLER * 18) + '"}'

# (ii) REFUSAL.
_REFUSAL = 'I cannot assist with that request. As an AI language model, I will not provide this analysis.'

# (iii) SHORT garbage (<50 chars).
_SHORT = 'nope'

# (v) MAD-default blast-radius guard: ~9,000-char benign string.
_MAD_OVERSIZE = _FILLER * 87  # ~9,048 chars, no signal strings


print('S53 L6 -- analysis-path guardian harness\n')

print(f'  (sizes: long={len(_LONG_VALID)}, normal={len(_NORMAL)}, '
      f'mad_oversize={len(_MAD_OVERSIZE)})')

# --- Analysis path: expect_json=False, max_length=None (ceiling disabled) ---
print('\n-- analysis path (expect_json=False, max_length=None) --')

_r_i = validate_response(_LONG_VALID, expect_json=False, max_length=None)
check('(i) clean ~10k report -> valid (ceiling no longer false-rejects)', _r_i['valid'] is True)

_r_ii = validate_response(_REFUSAL, expect_json=False, max_length=None)
check('(ii) refusal -> rejected (new protection)', _r_ii['valid'] is False)
check('(ii) refusal reason == model refusal detected',
      _r_ii['rejection_reason'] == 'model refusal detected')

_r_iii = validate_response(_SHORT, expect_json=False, max_length=None)
check('(iii) <50 garbage -> rejected (floor still enforced)', _r_iii['valid'] is False)
check('(iii) floor reason mentions too short', 'too short' in _r_iii['rejection_reason'])

_r_iv = validate_response(_NORMAL, expect_json=False, max_length=None)
check('(iv) normal ~2k report -> valid (regression: ordinary case unaffected)', _r_iv['valid'] is True)

# --- MAD path: DEFAULT args -- 8000 ceiling MUST still bite ---
print('\n-- MAD path (default args) -- shared-constant blast-radius guard --')

_r_v = validate_response(_MAD_OVERSIZE)  # default expect_json=True, max_length=8000
check('(v) ~9k string under DEFAULT args -> rejected (MAD ceiling intact)', _r_v['valid'] is False)
check('(v) rejection is the length ceiling, not something else',
      'too long' in _r_v['rejection_reason'])

print()
if _fails:
    print(f'RESULT: {len(_fails)} FAILED -> {_fails}')
    sys.exit(1)
print('RESULT: ALL GREEN')
