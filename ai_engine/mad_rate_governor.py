# -*- coding: utf-8 -*-
# ============================================================
# GNI MAD Rate Governor -- COMMIT 2
# Pure helper functions for header-aware Groq 429 handling.
# NO Groq client, NO Supabase, NO mad_protocol import (one-way only:
# mad_protocol -> mad_rate_governor). stdlib only. Caller does the sleeping.
#
# Grounded on a live 429 probe (llama-3.3-70b-versatile, on_demand tier):
#   retry-after: 4                      (coarse, whole seconds)
#   x-ratelimit-reset-tokens: 55.73s    (the BINDING token-bucket refill)
#   retry-after-ms: absent
#   12K TPM confirmed live
# The token-bucket reset is preferred over retry-after: honoring only 4s
# retries into a near-empty bucket (probe: 854 tok left) -> instant re-429.
# ============================================================

import re
from random import random

# Ceiling so a pathological reset value can never hang a run.
CAP_SECONDS = 75.0
# Small margin so we clear the token-bucket boundary instead of racing it.
TOKEN_RESET_MARGIN = 0.5

# Groq duration grammar seen in headers: "4", "3.675s", "55.73s", "11m31.2s", "2h1m3s".
_DUR_RE = re.compile(
    r'^\s*(?:(\d+(?:\.\d+)?)h)?(?:(\d+(?:\.\d+)?)m)?(?:(\d+(?:\.\d+)?)s?)?\s*$'
)

# Transient (retry-once) vs non-transient (give up immediately) classification.
# Used to recover the non-429 resilience that Groq(max_retries=0) removes.
_TRANSIENT_TYPE_NAMES = {
    'APIConnectionError', 'APITimeoutError', 'InternalServerError',
}
_NONTRANSIENT_TYPE_NAMES = {
    'BadRequestError', 'AuthenticationError', 'PermissionDeniedError',
    'NotFoundError', 'UnprocessableEntityError',
}
_TRANSIENT_SIGNALS = (
    'timeout', 'timed out', 'connection error', 'connection aborted',
    'temporarily unavailable', 'internal server error',
    'error code: 500', 'error code: 502', 'error code: 503', 'error code: 504',
    '502 bad gateway', '503 service', '504 gateway',
)


def parse_groq_duration(s) -> float | None:
    """Parse Groq's header duration grammar into seconds.

    "4" -> 4.0 | "3.675s" -> 3.675 | "55.73s" -> 55.73 | "11m31.2s" -> 691.2
    Unparseable / empty / None -> None. The SDK does NOT parse the
    'Nm M.SSs' form -- this is ours.
    """
    if s is None:
        return None
    s = str(s).strip()
    if not s:
        return None
    m = _DUR_RE.match(s)
    if not m or not any(m.groups()):
        return None
    h, mn, sec = m.groups()
    total = 0.0
    if h:
        total += float(h) * 3600.0
    if mn:
        total += float(mn) * 60.0
    if sec:
        total += float(sec)
    return total


def _hget(headers, key):
    """Case-insensitive-ish header get; tolerant of httpx.Headers or plain dict."""
    if headers is None:
        return None
    try:
        return headers.get(key)
    except Exception:
        return None


def compute_wait_from_headers(headers) -> float | None:
    """Decide the wait (seconds) for a TOKEN-limited 429 from response headers.

    Prefers x-ratelimit-reset-tokens (real bucket refill ~56s) over
    retry-after (coarse 4s). Falls back retry-after -> None.
    Result is capped at CAP_SECONDS; token-reset gets +TOKEN_RESET_MARGIN.
    Returns float seconds, or None if neither header is parseable.
    """
    if headers is None:
        return None
    reset_tokens = parse_groq_duration(_hget(headers, 'x-ratelimit-reset-tokens'))
    if reset_tokens is not None:
        return min(reset_tokens + TOKEN_RESET_MARGIN, CAP_SECONDS)
    retry_after = parse_groq_duration(_hget(headers, 'retry-after'))
    if retry_after is not None:
        return min(retry_after, CAP_SECONDS)
    return None


def compute_backoff(attempt: int, base: float = 15.0, cap: float = 120.0) -> float:
    """Exponential backoff with mild jitter, capped.

    attempt 0/1/2/3 -> ~15/30/60/120 (jitter reduces up to 15%, never exceeds
    nominal or cap). For the body-429 path (no headers) and header-less fallback.
    """
    nominal = min(base * (2.0 ** max(attempt, 0)), cap)
    return nominal * (1.0 - 0.15 * random())


def is_transient_error(exc, message: str = '') -> bool:
    """True if a NON-429 exception looks transient (worth one retry).

    Transient: connection/timeout/5xx. Non-transient: 4xx (bad request, auth,
    not found, unprocessable) -> never retry. Rate-limit (429) is handled
    separately by the caller and is NOT this function's concern.
    """
    name = type(exc).__name__
    if name in _NONTRANSIENT_TYPE_NAMES:
        return False
    if name in _TRANSIENT_TYPE_NAMES:
        return True
    msg = (message or str(exc)).lower()
    return any(sig in msg for sig in _TRANSIENT_SIGNALS)
