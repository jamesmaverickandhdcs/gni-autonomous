# -*- coding: utf-8 -*-
# ============================================================
# GNI Groq Guardian — GNI-R-234
# Validates ALL Groq API responses before pipeline processing.
# A response that fails validation is NEVER processed.
#
# Functions:
#   is_rate_limit_error(raw)   — detect 429 / rate limit strings
#   is_refusal(raw)            — detect model refusals
#   is_injection_attempt(raw)  — detect prompt injection in output
#   is_quality_response(raw)   — check length + JSON indicators
#   sanitize_response(raw)     — strip known noise from response
#   validate_response(raw)     — run all checks, return result dict
# ============================================================

import re

# ── Constants ────────────────────────────────────────────────

RATE_LIMIT_SIGNALS = [
    '429',
    'rate_limit',
    'rate limit',
    'too many requests',
    'quota exceeded',
    'tokens per minute',
    'requests per minute',
    'please slow down',
]

REFUSAL_SIGNALS = [
    'i cannot',
    "i can't",
    'i am unable',
    "i'm unable",
    'i will not',
    "i won't",
    'as an ai',
    'as a language model',
    'i apologize',
    'i\'m sorry, but i cannot',
    'this request cannot',
]

INJECTION_SIGNALS = [
    'ignore previous instructions',
    'ignore all previous',
    'disregard previous',
    'override instructions',
    'new instructions:',
    'system prompt:',
    'act as',
    'you are now',
    'jailbreak',
    'do anything now',
    'dan mode',
    '\x00',
    'prompt injection',
]

AGENT_ERROR_PREFIX = '[agent error'

MIN_RESPONSE_LENGTH = 50    # chars — anything shorter is suspicious
MAX_RESPONSE_LENGTH = 8000  # chars — anything longer is likely noise
JSON_OPEN_CHAR = '{'
JSON_CLOSE_CHAR = '}'


# ── Core Validation Functions ────────────────────────────────


def _tg_guardian_alert(reason: str) -> None:
    """Send Telegram alert when groq_guardian rejects. GNI S28 FIX."""
    try:
        import requests as _rq, os as _os
        tok = _os.environ.get('TELEGRAM_BOT_TOKEN', '')
        cid = _os.environ.get('TELEGRAM_ADMIN_CHAT_ID', '')
        if tok and cid and reason not in ('rate limit error (429)', 'empty response'):
            _rq.post(
                f'https://api.telegram.org/bot{tok}/sendMessage',
                json={'chat_id': cid, 'text': f'[GNI GUARDIAN] Silent rejection: {reason}'},
                timeout=5
            )
    except Exception:
        pass  # Never let Telegram break the guardian

def is_rate_limit_error(raw: str) -> bool:
    """
    Return True if the raw response indicates a Groq rate limit (429).
    Checks for known rate limit signal strings, case-insensitive.
    """
    if not raw:
        return False
    lower = raw.lower()
    return any(signal in lower for signal in RATE_LIMIT_SIGNALS)


def is_refusal(raw: str) -> bool:
    """
    Return True if the model refused to answer.
    Checks for known refusal phrases, case-insensitive.
    Only flags if refusal phrase appears in the FIRST 200 chars
    (to avoid false positives from quoted text in reports).
    """
    if not raw:
        return False
    lower = raw[:200].lower()
    return any(signal in lower for signal in REFUSAL_SIGNALS)


def is_injection_attempt(raw: str) -> bool:
    """
    Return True if the response contains prompt injection signals.
    These indicate an article may have injected instructions into
    the LLM response, bypassing the analysis intent.
    """
    if not raw:
        return False
    lower = raw.lower()
    return any(signal in lower for signal in INJECTION_SIGNALS)


def is_quality_response(raw: str) -> bool:
    """
    Return True if the response meets minimum quality standards:
    - Not empty
    - Not an agent error string
    - Length within acceptable range
    - Contains JSON structure indicators (for JSON-expected responses)
    """
    if not raw:
        return False
    stripped = raw.strip()
    if not stripped:
        return False
    if stripped.lower().startswith(AGENT_ERROR_PREFIX):
        return False
    if len(stripped) < MIN_RESPONSE_LENGTH:
        return False
    if len(stripped) > MAX_RESPONSE_LENGTH:
        return False
    return True


def has_json_structure(raw: str) -> bool:
    """
    Return True if the response contains a JSON object.
    Does not validate the JSON — just checks for { } presence.
    """
    if not raw:
        return False
    return JSON_OPEN_CHAR in raw and JSON_CLOSE_CHAR in raw


def sanitize_response(raw: str) -> str:
    """
    Strip known noise from LLM response:
    - Leading/trailing whitespace
    - Null bytes
    - Excessive newlines (more than 3 consecutive)
    Returns cleaned string. Does not modify JSON content.
    """
    if not raw:
        return ''
    cleaned = raw.strip()
    cleaned = cleaned.replace('\x00', '')
    cleaned = re.sub(r'\n{4,}', '\n\n\n', cleaned)
    return cleaned


def validate_response(raw: str, expect_json: bool = True) -> dict:
    """
    Run all validation checks on a raw Groq API response.

    Returns a dict:
    {
        'valid': bool,          — True if response is safe to process
        'sanitized': str,       — cleaned response text
        'rejection_reason': str — why it was rejected (empty if valid)
        'checks': dict          — individual check results
    }

    GNI-R-234: A response that fails validation is NEVER processed.
    """
    checks = {
        'is_rate_limit':    False,
        'is_refusal':       False,
        'is_injection':     False,
        'is_quality':       False,
        'has_json':         False,
    }

    if not raw:
        _tg_guardian_alert('empty response')
        return {
            'valid': False,
            'sanitized': '',
            'rejection_reason': 'empty response',
            'checks': checks,
        }

    sanitized = sanitize_response(raw)

    checks['is_rate_limit'] = is_rate_limit_error(sanitized)
    checks['is_refusal']    = is_refusal(sanitized)
    checks['is_injection']  = is_injection_attempt(sanitized)
    checks['is_quality']    = is_quality_response(sanitized)
    checks['has_json']      = has_json_structure(sanitized)

    # Determine rejection reason
    if checks['is_rate_limit']:
        _tg_guardian_alert('rate limit error (429)')
        return {
            'valid': False,
            'sanitized': sanitized,
            'rejection_reason': 'rate limit error (429)',
            'checks': checks,
        }

    if not checks['is_quality']:
        if sanitized.strip().lower().startswith(AGENT_ERROR_PREFIX):
            reason = 'agent error string'
        elif len(sanitized.strip()) < MIN_RESPONSE_LENGTH:
            reason = f'response too short ({len(sanitized.strip())} chars)'
        elif len(sanitized.strip()) > MAX_RESPONSE_LENGTH:
            reason = f'response too long ({len(sanitized.strip())} chars)'
        else:
            reason = 'quality check failed'
        _tg_guardian_alert(reason)
        return {
            'valid': False,
            'sanitized': sanitized,
            'rejection_reason': reason,
            'checks': checks,
        }

    if checks['is_refusal']:
        _tg_guardian_alert('model refusal detected')
        return {
            'valid': False,
            'sanitized': sanitized,
            'rejection_reason': 'model refusal detected',
            'checks': checks,
        }

    if checks['is_injection']:
        _tg_guardian_alert('injection attempt detected in response')
        return {
            'valid': False,
            'sanitized': sanitized,
            'rejection_reason': 'injection attempt detected in response',
            'checks': checks,
        }

    if expect_json and not checks['has_json']:
        return {
            'valid': False,
            'sanitized': sanitized,
            'rejection_reason': 'expected JSON but no { } found',
            'checks': checks,
        }

    return {
        'valid': True,
        'sanitized': sanitized,
        'rejection_reason': '',
        'checks': checks,
    }
