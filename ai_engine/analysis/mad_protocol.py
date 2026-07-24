# ============================================================
# GNI MAD Protocol v2 -- Quadratic Debate Framework
# Bull -> Bear -> Black Swan -> Ostrich -> Arbitrator
# Personal consultants coach R1+R2 (GNI-R-235). Arbitrator final R3 only.
# Grounded in ALL relevant articles not just top 5
# Short Focus (7-30 days) + Long Shoots (3-24 months)
# Predictions saved to debate_predictions table
# 21 Groq calls per run
# GNI-R-237: MAD uses GROQ_MAD_MODEL (confirmed secret = llama-3.3-70b-versatile),
#            falling back to GROQ_MODEL then GROQ_MODEL_FALLBACK. All 21 calls, one model.
# GROQ_API_KEY_2 removed -- same account = same pool, no isolation benefit.
# S37 PROMPT PATCHES:
#   BULL:       SYNTHESIS RULE + PRE-BUTTAL RULE
#   BEAR:       QUANTIFY + SCOPE + RISK PRICING
#   SWAN:       CREDIBILITY ANCHOR + UAP RULE + FALLOUT CHAIN
#   OSTRICH:    JURISDICTION RULE + SILO-GAP primary frame
#   ALL CONS:   FOUNDATION CHECK + NO REPEAT RULE
#   SWAN CONS:  GROUNDING CHECK
#   OSTRICH CONS: JURISDICTION CHECK + SILO-GAP push
#   ARBITRATOR: SELF-CONSISTENCY + ACTION PRIORITY + SPECIFICITY + UAP RULE
#   R2 CTX:     Consultant contextual memory
# S37 ARTICLE ROUTING PATCHES:
#   _build_news_context: agent param + weak_articles param + sort before cut
#   run_mad_protocol:    5 agent-specific contexts replacing single news_ctx
#   Bull/Bear/Ost/Arb:  scored articles sorted DESC by stage3_score
#   Swan:               weak signal pool (stage3_score=0) -- overlooked articles
#   All agents:         article summaries included (Fix 2)
# CURRENT SIZING (S48):
#   per-pillar [:15] article slice; summary depth is solver-set (S51; was static 400)
#   R1/R2 agent max_tokens 500 (was 350)
# ============================================================

import os
import json
import re
import time
from datetime import datetime, timezone, timedelta
from groq import Groq
from groq_guardian import validate_response  # GNI-R-234
from mad_rate_governor import (  # COMMIT 2 -- header-aware 429 governor
    compute_wait_from_headers, compute_backoff, is_transient_error,
)
from analysis.mad_budget_solver import compute_depth  # S51 -- depth budget solver
from analysis.mad_grounding_gate import check_grounding  # S61 -- Layer-1 grounding gate (SHADOW)

# COMMIT 2 / Decision A1: max_retries=0 -- the governor owns ALL waits.
# The SDK's internal retries honor only retry-after (~4s) and would fire into a
# near-empty token bucket during a TPM storm; we wait the real ~56s reset instead.
client = Groq(api_key=os.getenv('GROQ_API_KEY'), max_retries=0)
MODEL = os.getenv('GROQ_MAD_MODEL',
        os.getenv('GROQ_MODEL',
        os.getenv('GROQ_MODEL_FALLBACK', 'llama-3.3-70b-versatile')))

VALID_VERDICTS = ['bullish', 'bearish', 'neutral']

# ---- GT-5 E-2 (S73): consultant gating ----
# A consultant reply carrying >= T ungrounded spans is withheld from the agent it
# coaches. T=3 by ratified design: GT-1 dialect vocabulary is already excluded from
# hit_count, and shadow data puts storm chatter at ~1-2 -- so 3 is the floor that
# fires on fabrication without starving agents in a storm. One week of
# grounding_watch digest observation before considering T=2.
GROUNDING_GATE_T = 3
# Neutral stand-in: the round's prompt structure survives the withholding -- the
# agent still sees its consultant slot, just with no fabricated claim inside it.
# NEVER a re-prompt (quota 87%, cliff 31d): withholding is the whole remedy.
GROUNDING_WITHHELD_MARKER = '[consultant reply withheld: ungrounded]'

# COMMIT 2 / Decision B: 3 attempts -- one extra chance, since waiting the real
# token-reset window (vs the old flat 40s that undershot the ~56s bucket) makes
# the later attempt actually likely to succeed.
_MAX_ATTEMPTS = 3
# W-02 final-retry wait ceiling (~token-bucket refill); see _call_arbitrator.
CAP_W02_SECONDS = 75.0

# S46 Phase 0 -- real token metering (observability only; no prompt/debate-logic change).
# Accumulates actual response.usage across every Groq call in one MAD run.
# Counts retries (real cost) and guardian-rejected responses (tokens were billed).
_TOKEN_USAGE = {'prompt': 0, 'completion': 0, 'total': 0, 'calls': 0}


def reset_token_usage():
    _TOKEN_USAGE.update({'prompt': 0, 'completion': 0, 'total': 0, 'calls': 0})


def get_token_usage():
    return dict(_TOKEN_USAGE)


def _call_agent(system_prompt: str, user_prompt: str, max_tokens: int = 400, expect_json: bool = False) -> str:
    for attempt in range(_MAX_ATTEMPTS):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt},
                ],
                max_tokens=max(max_tokens, 3000),  # S80 MAD-MIGRATE: reasoning-model floor.
                # Probe-derived (probe_results.jsonl): gpt-oss-120b reasoning ~1500-1600 tok
                # + content ~550; 600/1200 both starved (0/3 parse), 3000 clean (finish=stop,
                # 12/12 fields). Covers ALL tiers: arbitrator routes via _call_agent (L153).
                # Revert = restore max_tokens=max_tokens. Legacy tier values untouched above.
                temperature=0.7,
            )
            _u = getattr(response, 'usage', None)
            if _u:
                _TOKEN_USAGE['prompt']     += getattr(_u, 'prompt_tokens', 0) or 0
                _TOKEN_USAGE['completion'] += getattr(_u, 'completion_tokens', 0) or 0
                _TOKEN_USAGE['total']      += getattr(_u, 'total_tokens', 0) or 0
                _TOKEN_USAGE['calls']      += 1
            raw = response.choices[0].message.content.strip()
            validation = validate_response(raw, expect_json=expect_json)
            if not validation['valid']:
                # COMMIT 2: body-429 gap closure -- a 200-status body that the
                # guardian flags as rate-limited used to return WITHOUT retry.
                # No headers on this path, so exponential backoff. Only rate-limit
                # rejections retry; refusal/injection/quality still return now.
                if validation['checks'].get('is_rate_limit') and attempt < _MAX_ATTEMPTS - 1:
                    wait = compute_backoff(attempt)
                    print(f'  WARNING: body-429 (guardian) -- backoff {wait:.1f}s '
                          f'(attempt {attempt + 1}/{_MAX_ATTEMPTS})')
                    time.sleep(wait)
                    continue
                print(f'  WARNING: groq_guardian rejected response: {validation["rejection_reason"]}')
                _log_safety_event('guardian_rejection', validation['rejection_reason'])
                return '[Agent error: ' + validation['rejection_reason'] + ']'
            return validation['sanitized']
        except Exception as e:
            err = str(e)
            is_rate_limit = '429' in err or 'rate_limit' in err.lower() or 'rate limit' in err.lower()
            if is_rate_limit and attempt < _MAX_ATTEMPTS - 1:
                # COMMIT 2: header-aware wait. RateLimitError carries .response;
                # APIConnectionError/APITimeoutError do NOT -- getattr guard mandatory.
                resp = getattr(e, 'response', None)
                wait = compute_wait_from_headers(getattr(resp, 'headers', None)) if resp is not None else None
                if wait is None:
                    wait = compute_backoff(attempt)
                print(f'  WARNING: Groq 429 -- waiting {wait:.1f}s '
                      f'(attempt {attempt + 1}/{_MAX_ATTEMPTS})')
                time.sleep(wait)
                continue
            # COMMIT 2 / A1 addition: recover non-429 transient resilience lost by
            # max_retries=0 -- ONE backoff retry for 5xx/timeout/connection errors.
            # Non-transient (400/401/403/404/422) returns immediately, no retry.
            if (not is_rate_limit) and attempt == 0 and is_transient_error(e, err):
                wait = compute_backoff(attempt)
                print(f'  WARNING: transient error ({type(e).__name__}) -- '
                      f'backoff {wait:.1f}s then one retry')
                time.sleep(wait)
                continue
            return '[Agent error: ' + err[:100] + ']'
    return '[Agent error: max retries exceeded]'


def _call_arbitrator(system_prompt: str, user_prompt: str, max_tokens: int = 600, expect_json: bool = True) -> str:
    """W-02: TPM-aware arbitrator call with one extra retry."""
    result = _call_agent(system_prompt, user_prompt, max_tokens, expect_json)
    if (result.startswith('[Agent error') and
            ('429' in result or 'rate_limit' in result.lower() or 'rate limit' in result.lower())):
        # COMMIT 2: W-02 only sees the error STRING (no exception/headers here --
        # the header-exact wait already happened inside _call_agent's retries).
        # This is the final coarse safety net: one more try after a bucket-sized wait.
        wait = compute_backoff(0, base=60.0, cap=CAP_W02_SECONDS)
        print(f'  WARNING: Arbitrator 429 -- W-02 bucket wait {wait:.1f}s before final retry...')
        time.sleep(wait)
        result = _call_agent(system_prompt, user_prompt, max_tokens, expect_json)
        if result.startswith('[Agent error'):
            print('  WARNING: Arbitrator final retry also failed -- using safe defaults')
            _log_safety_event('w02_retry_failed', 'W-02 retry also failed -- MAD will use neutral fallback')
        else:
            print('  OK: Arbitrator W-02 retry succeeded')
            _log_safety_event('w02_retry_success', 'Arbitrator W-02 extra retry fired and succeeded')
    return result


def _log_safety_event(event_type: str, detail: str) -> None:
    """Log safety net activation to runtime_logs. Silent -- never breaks pipeline."""
    try:
        from supabase import create_client
        sb = create_client(
            os.getenv('SUPABASE_URL', ''),
            os.getenv('SUPABASE_SERVICE_KEY', '')
        )
        sb.table('runtime_logs').insert({
            'status':               event_type,
            'error_message':        detail,
            'articles_collected':   0,
            'articles_after_funnel': 0,
            'reports_saved':        0,
            'step_timings':         '{}',
        }).execute()
    except Exception:
        pass


def _build_news_context(report: dict, all_articles: list,
                        weak_articles: list = None, agent: str = 'general',
                        depth: int = 400) -> str:
    """
    Build news context for a specific agent.
    S37 PATCH: agent-specific article selection + sort before cut + summaries.

    agent='bull'/'bear'/'ostrich'/'arbitrator'/'general':
        Uses all_articles (scored, stage3_score > 0), sorted DESC.
        Top 15 per pillar = highest significance articles.

    agent='swan':
        Uses weak_articles (stage3_score = 0) -- overlooked weak signals.
        Swan's structural mission: find what others dismissed.
        Falls back to all_articles sorted ASC if weak_articles empty.
    """
    title = report.get('title', 'No title')
    summary = report.get('summary', '')[:400]
    risk_level = report.get('risk_level', 'Medium')
    escalation = report.get('escalation_level', '')
    location = report.get('location_name', '')
    report_ctx = (
        'CURRENT INTELLIGENCE REPORT:\n'
        f'Title: {title}\n'
        f'Summary: {summary}\n'
        f'Risk: {risk_level} | Escalation: {escalation} | Location: {location}\n'
    )

    # Select article pool based on agent
    if agent == 'swan':
        pool = weak_articles if weak_articles else all_articles
        sort_desc = False  # Swan: lowest score first (most overlooked)
        label = 'WEAK SIGNAL ARTICLES -- overlooked, low-scoring, Swan priority'
    else:
        pool = all_articles
        sort_desc = True   # Others: highest score first (most significant)
        label = 'INTELLIGENCE BASE -- SCORED ARTICLES (highest significance first)'

    if not pool:
        return report_ctx

    by_pillar = {'geo': [], 'fin': [], 'tech': [], 'other': []}
    for art in pool:
        p = art.get('pillar', 'other').lower()
        by_pillar[p if p in by_pillar else 'other'].append(art)

    articles_ctx = f'\n{label}:\n'
    for pillar, arts in by_pillar.items():
        if not arts:
            continue
        # Sort before cut -- fixes insertion-order problem
        sorted_arts = sorted(
            arts,
            key=lambda x: x.get('stage3_score', 0),
            reverse=sort_desc
        )
        articles_ctx += f'\n[{pillar.upper()} -- {len(arts)} articles]\n'
        for art in sorted_arts[:15]:
            src = art.get('source', '')
            ttl = art.get('title', '')[:80]
            scr = art.get('stage3_score', 0)
            smr = art.get('summary', '')[:depth].replace('\n', ' ')
            articles_ctx += f'  - [{src}] {ttl} (score:{scr})'
            if smr:
                articles_ctx += f' -- {smr}'
            articles_ctx += '\n'

    total = sum(len(v) for v in by_pillar.values())
    articles_ctx += f'\nTotal in pool: {total}\n'
    return report_ctx + articles_ctx


def _detect_dominant_pillar(all_articles: list) -> str:
    """Detect which pillar dominates this run's article set."""
    counts = {'geo': 0, 'tech': 0, 'fin': 0}
    for art in all_articles:
        p = art.get('pillar', '').lower()
        if p in counts:
            counts[p] += 1
    if not any(counts.values()):
        return 'geo'
    return max(counts, key=counts.get)


def _get_pillar_arb_instruction(pillar: str) -> str:
    """Return pillar-specific weighting instruction for Arbitrator."""
    if pillar == 'tech':
        return (
            'PILLAR WEIGHTING -- TECHNOLOGY DOMINANT: '
            'BLACK SWAN DOMINATES this analysis. '
            'Technology threats are unknown unknowns -- '
            'zero-day exploits, AI capability jumps, chip supply shocks. '
            'Discount Bull and Bear. Black Swan tail risk is the decisive factor here. '
        )
    elif pillar == 'fin':
        return (
            'PILLAR WEIGHTING -- FINANCIAL DOMINANT: '
            'BEAR DOMINATES this analysis. '
            'Financial threats are known risks playing out -- '
            'rate shocks, sovereign defaults, currency crises, contagion. '
            'Discount Bull optimism. Bear systematic risk analysis is the decisive factor here. '
        )
    else:
        return (
            'PILLAR WEIGHTING -- GEOPOLITICAL DOMINANT: '
            'ALL FOUR AGENTS carry equal decisive weight. '
            'Geopolitical threats span all quadrants simultaneously -- '
            'known conflicts (Bear), missed opportunities (Bull), '
            'ignored realities (Ostrich), unknown escalations (Black Swan). '
            'No single agent dominates. The blind spot quadrant is critical to identify. '
        )


def _grounding_hit_count(grounding, field):
    """Recorded save-time hit_count for one mad_*_case field, or None if unknown.

    None means 'unscored / unreadable' and the caller INCLUDES the snippet
    (fail-open). None is returned when: the column is NULL or absent (every row
    written before GT-5 scoring landed), the value is not a dict, the field key
    is missing, the per-field entry is malformed, or hit_count is not an integer.

    A malformed or missing value must never starve history: an unscored row is an
    honest unknown, not a conviction. Only a value we can actually READ and that
    actually says hit_count > 0 is allowed to drop a snippet.
    """
    if not isinstance(grounding, dict):
        return None
    entry = grounding.get(field)
    if not isinstance(entry, dict):
        return None
    n = entry.get('hit_count')
    # bool is a subclass of int -- True must not read as hit_count 1.
    if isinstance(n, bool) or not isinstance(n, int):
        return None
    return n


def _get_debate_history() -> dict:
    history = {'bull': [], 'bear': [], 'black_swan': [], 'ostrich': [], 'verdict_trend': ''}
    try:
        from supabase import create_client
        url = os.getenv('SUPABASE_URL', '')
        key = os.getenv('SUPABASE_SERVICE_KEY', '')
        if not url or not key:
            return history
        sb = create_client(url, key)
        result = sb.table('reports') \
            .select('id,mad_bull_case,mad_bear_case,mad_black_swan_case,mad_ostrich_case,short_focus_threats,long_shoot_threats,mad_verdict,mad_confidence,created_at,mad_grounding_hits') \
            .not_.is_('mad_black_swan_case', 'null') \
            .neq('mad_verdict', 'pending') \
            .order('created_at', desc=True) \
            .limit(7) \
            .execute()
        rows = result.data or []
        trend_parts = []
        for row in rows:
            v = row.get('mad_verdict', '')
            c = row.get('mad_confidence')
            d = row.get('created_at', '')[:10]
            if v:
                conf_str = f'{round(float(c), 2)}' if c is not None else '?'
                trend_parts.append(f'{d}:{v}({conf_str})')
        if trend_parts:
            verdicts_only = [p.split(':')[1].split('(')[0] for p in trend_parts]
            if len(set(verdicts_only)) == 1:
                streak_note = f' [WARNING: {len(verdicts_only)}-run {verdicts_only[0].upper()} streak -- check for Pattern Match Bias]'
            else:
                streak_note = ''
            history['verdict_trend'] = 'Last ' + str(len(trend_parts)) + ' verdicts: ' + ' | '.join(trend_parts) + streak_note
        for row in rows[:3]:
            d = row.get('created_at', '')[:10]
            # GT-5 E-1b: per-row save-time grounding verdicts (NULL on pre-GT-5 rows).
            _grounding = row.get('mad_grounding_hits')
            _rid = row.get('id', '')
            for agent in ['bull', 'bear', 'black_swan', 'ostrich']:
                key_name = 'mad_' + agent + '_case'
                if not row.get(key_name):
                    continue
                # GT-5 E-1b -- break the recurrence loop at the point of re-entry.
                # A case that scored ungrounded when it was SAVED is exactly the
                # text that returns as "prior authority" and gets repeated. Drop
                # the snippet WHOLE: masking would leave ellipsis rubble inside a
                # [:150] window, which reads to an agent as garbage rather than as
                # absence. Unscored/unreadable rows fall through and are included.
                _n = _grounding_hit_count(_grounding, key_name)
                if _n is not None and _n > 0:
                    print('  HISTORY-SKIP ' + key_name + ' ' + str(_n)
                          + ' hits (report ' + str(_rid) + ')')
                    continue
                history[agent].append(f"[{d}] {row[key_name][:150]}")
    except Exception as e:
        print('  Warning: debate history: ' + str(e)[:60])
    return history


def _fmt_history(h: list) -> str:
    return '\n'.join(h) if h else 'No previous debate history yet.'


def _compress(text: str, max_words: int = 40) -> str:
    if not text or text.startswith('[Agent error'):
        return text[:100] if text else ''
    words = text.split()
    if len(words) <= max_words:
        return text
    return ' '.join(words[:max_words]) + '...'


def _save_predictions(report_id: str, short: str, long_s: str,
                      short_days: int, long_days: int, round3: dict) -> None:
    try:
        from supabase import create_client
        url = os.getenv('SUPABASE_URL', '')
        key = os.getenv('SUPABASE_SERVICE_KEY', '')
        if not url or not key or not report_id:
            return
        sb = create_client(url, key)
        now = datetime.now(timezone.utc)
        records = []
        for agent, pos in round3.items():
            if pos:
                records.append({
                    'report_id': report_id,
                    'agent': agent,
                    'horizon': 'short',
                    'prediction': pos[:500],
                    'verify_by': (now + timedelta(days=short_days)).date().isoformat(),
                    'verified_by': 'pending',
                })
        if long_s:
            records.append({
                'report_id': report_id,
                'agent': 'arbitrator',
                'horizon': 'long',
                'prediction': long_s[:500],
                'verify_by': (now + timedelta(days=long_days)).date().isoformat(),
                'verified_by': 'pending',
            })
        if records:
            sb.table('debate_predictions').insert(records).execute()
            print(f'  OK {len(records)} predictions saved')
    except Exception as e:
        print('  Warning: save predictions: ' + str(e)[:60])


def _validate_mad_output(result: dict) -> dict:
    verdict = result.get('mad_verdict', '')
    if verdict not in VALID_VERDICTS:
        result['mad_verdict'] = 'neutral'
    try:
        result['mad_confidence'] = max(0.0, min(1.0, float(result.get('mad_confidence', 0.5))))
    except (TypeError, ValueError):
        result['mad_confidence'] = 0.5
    injection_signals = ['ignore previous', 'override', 'jailbreak', 'system:', 'act as']
    for field in ['mad_bull_case', 'mad_bear_case', 'mad_black_swan_case', 'mad_ostrich_case',
                  'mad_reasoning', 'mad_blind_spot', 'mad_action_recommendation',
                  'short_focus_threats', 'long_shoot_threats']:
        text = result.get(field, '').lower()
        for sig in injection_signals:
            if sig in text:
                result[field] = '[Output flagged -- injection signal detected]'
    return result


# ============================================================
# MAD REDEFINITION -- senior G+T+F / hidden-pattern foundation (module-level).
# Every agent, consultant, and the Arbitrator share ONE caliber floor; only the
# LENS differs. Consultants are EQUAL-RANK same-lens insight-developers (the old
# 'FOUNDATION CHECK: correct it FIRST' clause is gone -- it was the hallucination
# source). GROUNDING_RULE is placed identically across all 11 prompts: immediately
# before the closing '3-4 sentences.' (agents/consultants) / before the JSON block
# (Arbitrator). JSON schema is byte-identical to the prior version.
# ============================================================

# GNI MISSION WALL -- PRESERVED verbatim (FUTURE THREATS mission + character purity).
GNI_WALL = ('GNI MISSION: "FUTURE THREATS" is GNI\'s VISION -- early warning of threats AND '
            'opportunities so people can prepare. Within that mission, argue ONLY your own '
            'character\'s genuine position. The vision never overrides the character. ')

# Shared senior foundation. G+T+F = the DOMAIN; hidden-pattern/invisible-linking = PRIMARY skill.
SENIOR_FOUNDATION = (
    'You are a deeply experienced SENIOR strategist-analyst -- the caliber of person who '
    'briefs heads of state and runs the room when the stakes are existential. Your domain is '
    'the WOVEN intersection of GEOPOLITICS, TECHNOLOGY, and FINANCE: you never read one pillar '
    'in isolation -- you read all three as a single interconnected system. You see how a '
    'sanctions decision reshapes a semiconductor supply chain and reprices sovereign debt in '
    'the same motion; how a technology breakthrough shifts a military balance and moves a '
    'currency; how a capital flow telegraphs a political intention before any official says a word. '
    'Your PRIMARY, DEFINING specialization -- the thing you are better at than anyone -- is '
    'HIDDEN-PATTERN RECOGNITION and INVISIBLE LINKING: the connection nobody else has drawn, '
    'the unnamed broker who actually moves the outcome, the quiet dependency, the second- and '
    'third-order effect that arrives after the headline fades. Where others see separate events, '
    'you see the thread that joins them. Every argument you make is the kind a professional '
    'intelligence briefer would stake their reputation on. '
)

# TIER-1 anti-hallucination grounding rule. Placed immediately before the closing line of every prompt.
GROUNDING_RULE = (
    'GROUNDING (TIER-1, ABSOLUTE): State no named fact -- no person, no title, no organization, '
    'no number, and no date -- unless it appears in the provided intelligence. If you cannot '
    'verify a specific fact from the provided articles, DO NOT assert it; argue instead from what '
    'IS provided, or name the gap explicitly. A modest claim you can ground beats a vivid claim '
    'you cannot. Inventing a name, figure, or date to make an argument land is a disqualifying '
    'failure, not a flourish. '
)

# ---- Four agents: shared foundation + PURE lens + preserved mechanics ----
BULL = (
    GNI_WALL + SENIOR_FOUNDATION +
    'YOUR LENS -- THE BULL: Quadrant Upper-Right, Known Positives. Current date: May 2026; '
    'all timelines relative to 2026. You are the senior optimist of this room -- not naive, '
    'but the one who steelmans the GENUINE positive read others are too cynical to see. Your '
    'edge is spotting the hidden upside: the de-escalation pathway nobody is pricing, the quiet '
    'cooperation forming off-stage, the actor whose incentives have just flipped toward '
    'stabilisation. Focus on what concretely STABILISES, DE-ESCALATES, or IMPROVES because of '
    'this event -- real opportunity, real recovery, real cooperation -- NOT the mere threat of '
    'inaction dressed up as upside. Name the actors, the mechanism, and the specific opportunity, '
    'and trace the second-order benefit others will miss. '
    'PRE-BUTTAL RULE: anticipate the Bear\'s strongest counter and disarm it before it is made. '
    'SYNTHESIS RULE: do NOT copy or append to previous rounds -- write a completely fresh argument '
    'each round. Keep your lens pure: you argue the genuine upside, never hedge toward the threat '
    'cases. ' + GROUNDING_RULE + '3-4 sentences.'
)

BEAR = (
    GNI_WALL + SENIOR_FOUNDATION +
    'YOUR LENS -- THE BEAR: Quadrant Lower-Right, Known Negatives. Current date: May 2026; '
    'all timelines relative to 2026. You are the senior risk mind of this room -- the one who '
    'has watched fragile systems break before and knows exactly where the cracks propagate. '
    'Focus on FUTURE THREATS from KNOWN risks and systemic vulnerabilities: name which systems '
    'are fragile, why, and the precise mechanism that drives the break. Your hidden-pattern edge '
    'is the contagion path -- how a failure in one pillar transmits into the other two. '
    'QUANTIFY: support claims with specific figures where the articles provide them (percentages, '
    'volumes, dollar amounts). '
    'SCOPE: broaden vulnerability beyond energy -- semiconductors, critical minerals, manufacturing, '
    'payment rails, sovereign balance sheets. '
    'RISK PRICING: argue that the THREAT of disruption inflicts damage through risk premiums and '
    'repricing even before any physical event occurs. Keep your lens pure: you argue the genuine '
    'downside, never soften it toward optimism. ' + GROUNDING_RULE + '3-4 sentences.'
)

SWAN = (
    GNI_WALL + SENIOR_FOUNDATION +
    'YOUR LENS -- THE BLACK SWAN: Quadrant Upper-Left, Unknown Negatives. Current date: May 2026. '
    'You are the senior tail-risk mind -- the one whose entire career is built on seeing the '
    'unmodelled threat forming in the data everyone else discarded. You are receiving the '
    'LOW-SCORING articles others dismissed; these are your hunting ground. Your hidden-pattern '
    'edge IS the whole job: name a specific article from this list and explain the CONNECTION '
    'nobody else has drawn -- why this overlooked signal links to a consequence no one is pricing. '
    'CREDIBILITY RULE: your threat MUST rest on real-world evidence -- a real technology, a real '
    'actor, a real event in the provided intelligence -- the surprise comes from the connection, '
    'never from an impossible scenario. '
    'UAP RULE: if referencing unidentified phenomena, frame them as adversarial drone / UAP / '
    'next-gen UAS from a known state actor (e.g. China, Russia) -- never as speculative fiction or aliens. '
    'FALLOUT RULE: present consequences as a numbered chain -- 1. Detection Failure  2. Escalation  '
    '3. Geopolitical Retaliation. Keep your lens pure: you hunt the unknown tail risk, never retreat '
    'to the obvious known one. ' + GROUNDING_RULE + '3-4 sentences.'
)

OSTRICH = (
    GNI_WALL + SENIOR_FOUNDATION +
    'YOUR LENS -- THE OSTRICH: Quadrant Lower-Left, Ignored Realities. Current date: May 2026. '
    'You are the senior mind who names the threat everyone can already see but has collectively '
    'agreed not to look at -- the inertia, the institutional denial, the willful blind spot. Your '
    'hidden-pattern edge is the SILO-GAP: '
    'PRIMARY FRAME -- find the GAP between two institutions, where Institution A holds the risk but '
    'has NOT communicated it to Institution B, and that silence IS the hidden threat. Name the '
    'specific institutions, the specific gap, and the specific cost of that silence. '
    'JURISDICTION RULE: before naming an institution, verify it has direct authority over the threat '
    'you describe; if it does not, find the institution that does. Keep your lens pure: you expose '
    'the ignored, in-plain-sight reality, never drift to the exotic unknown. '
    + GROUNDING_RULE + '3-4 sentences. Name names.'
)


# ---- ONE grounding-whitelist contract (GT-5, S73) ----
# Strings that are grounded BY CONSTRUCTION, handed to check_grounding as
# whitelist_extra. Two kinds:
#   1. the report framing the debate (title / summary / location);
#   2. the Swan FALLOUT chain headers -- SWAN's prompt above MANDATES that exact
#      numbered template ("FALLOUT RULE"), so they are scaffolding the model was
#      ORDERED to emit, not claims it invented. Scoring them as fabrication would
#      flag every compliant Swan case.
# Defined here, next to the prompt that mandates it, and imported by every caller
# (run_mad_protocol's shadow seams + mad_runner's save-time scoring) so there is
# exactly ONE definition -- a hand-copy per site is how the two drift apart.
SWAN_FALLOUT_HEADERS = ('Detection Failure', 'Escalation', 'Geopolitical Retaliation')


def build_grounding_whitelist(report: dict) -> list:
    """Grounded-by-construction strings for check_grounding(whitelist_extra=...)."""
    return [
        report.get('title', ''),
        report.get('summary', ''),
        report.get('location_name', ''),
        *SWAN_FALLOUT_HEADERS,
    ]


def _consultant(lens_name: str, lens_desc: str, develop_line: str) -> str:
    """Build an equal-rank, same-lens insight-developer consultant prompt.

    No correcting/judging/'fix errors first' -- a peer second mind aimed in the
    SAME direction as its agent, surfacing additional hidden-pattern insight.
    """
    return (
        SENIOR_FOUNDATION +
        f'YOU AND YOUR COUNTERPART: You are a SENIOR {lens_name}-lens strategist of EQUAL RANK to '
        f'the {lens_name} Agent -- a peer, not a coach, not a supervisor, not a corrector. You hold '
        f'the identical lens: {lens_desc} You are not here to grade {lens_name}\'s work or fix it. '
        f'You are a SECOND independent mind aimed in the SAME direction. '
        f'YOUR FUNCTION -- DEVELOP ADDITIONAL INSIGHT: {lens_name}\'s first pass could only reach so '
        f'far. {develop_line} Surface the hidden-pattern connection, the invisible broker, the '
        f'second- or third-order move that {lens_name} did not yet draw. Deepen and EXPAND the case '
        f'in its own direction -- make it MORE itself. You never flatten it toward neutral, never '
        f'hedge it, never argue the other side. '
        f'NO REPEAT: do not restate insight {lens_name} already has -- add only what is genuinely new. '
        f'No invented numbers, no invented dates, no fabricated names. No praise. Stay fully in the '
        f'{lens_name} lens. ' + GROUNDING_RULE + '3-4 sentences.'
    )


BULL_CONS = _consultant(
    'Bull',
    'genuine opportunity, stabilisation, de-escalation, and the upside others are too cynical to see.',
    'Find the opportunity Bull understated -- name the actor and the specific move they must make to capture it.'
)
BEAR_CONS = _consultant(
    'Bear',
    'systemic failure, known downside, fragile systems, and the contagion path between pillars.',
    'Find the fragility Bear understated -- name what breaks first, who is exposed, and how the failure transmits.'
)
SWAN_CONS = _consultant(
    'Black Swan',
    'the unknown, unmodelled tail risk hiding in the signals others discarded.',
    'Push the case to the exact triggering event and the connection nobody drew -- a specific grounded chain, '
    'not a general cascade; a named adversarial technology or state actor that the articles support.'
)
OSTRICH_CONS = _consultant(
    'Ostrich',
    'the ignored, in-plain-sight reality, institutional inertia, and the willful blind spot.',
    'Sharpen the SILO-GAP: which institution holds the risk, which one is NOT being told, and the specific '
    'cost of that silence -- make the inertia and communication failure so concrete it cannot be dismissed.'
)

# ---- Arbitrator: shared foundation + synthesis role; JSON schema UNCHANGED ----
ARB_FINAL = (
    SENIOR_FOUNDATION +
    'YOUR ROLE -- THE ARBITRATOR: You are the most senior mind in the room. Four expert agents '
    '(Bull, Bear, Black Swan, Ostrich), each your equal in caliber but locked to a single lens, '
    'have argued for three rounds. Your job is the synthesis only you can do: weigh their cases '
    'with your full G+T+F judgement, draw the hidden-pattern links ACROSS their four positions '
    'that no single-lens agent could see, and resolve the debate into one decision. '
    'After 3 rounds identify: '
    '(1) BLIND SPOT QUADRANT -- most neglected. '
    '(2) ACTION RECOMMENDATION -- one specific action now. '
    '(3) SHORT FOCUS THREATS -- specific threats in next 7-30 days. '
    '(4) LONG SHOOT THREATS -- structural threats over 3-24 months. '
    '(5) SHORT FOCUS OPPORTUNITIES -- concrete stabilising/de-escalating/improving '
    'developments in the next 7-30 days (early warning of opportunity, not just threat). '
    '(6) PREPAREDNESS PATH -- what specific actors can do to prepare for or capture them. '
    '(7) Verdict and confidence. '
    'OPPORTUNITY WEIGHTING: Weigh the Bull\'s genuine upside against the three threat cases. '
    'A bullish OR neutral verdict is valid and expected when opportunity outweighs or '
    'balances risk -- do NOT default to bearish. '
    'CONFIDENCE CALIBRATION: Justify confidence against the evidence -- never a round number. '
    'High (>=0.75) ONLY when agents converge on hard, cited evidence; '
    'moderate (0.40-0.60) when Bull and Bear genuinely conflict or evidence is thin; '
    'never below 0.40. State the calibration basis in your reasoning. '
    'ACTION PRIORITY RULE: Your primary action_recommendation must address the highest-probability development. '
    'Novel or low-probability items appear as secondary recommendations only -- never as the primary. '
    'SPECIFICITY RULE: Every ignored reality claim must name a specific institution, '
    'specific gap, and specific consequence -- no vague placeholders. '
    'UAP RULE: If referencing unidentified aerial phenomena, frame as adversarial '
    'drone/UAS technology from a named state actor -- not UFOs or aliens. ' +
    GROUNDING_RULE +
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


def run_mad_protocol(report: dict, all_articles: list = None,
                     weak_articles: list = None, report_id: str = None) -> dict:
    """
    S37 PATCH: weak_articles parameter added.
    all_articles  = scored articles (stage3_score > 0) -- Bull/Bear/Ostrich/Arb
    weak_articles = overlooked articles (stage3_score = 0) -- Swan only
    """
    if all_articles is None:
        all_articles = []
    if weak_articles is None:
        weak_articles = []

    # ============================================================
    # S37 ARTICLE ROUTING: Build 5 agent-specific contexts
    # Each agent gets the right article pool, sorted correctly.
    # Replaces single news_ctx shared by all agents.
    # ============================================================
    # S51 DEPTH SOLVER (Commit 1): one global D from the scored pool's effective N
    # (per-pillar capped; mirrors lines 218-221 + the [:15] cap @234).
    # COUPLING: if bucket keys (~218) or the cap 15 (~234) change, update this count.
    # N is sacred (never reduced); D is the only lever.
    _buckets = {'geo': 0, 'fin': 0, 'tech': 0, 'other': 0}
    for _art in all_articles:
        _p = _art.get('pillar', 'other').lower()
        _buckets[_p if _p in _buckets else 'other'] += 1
    _eff_n = sum(min(_c, 15) for _c in _buckets.values())  # max 60, matches grid
    _depth, _depth_est, _depth_status = compute_depth(_eff_n)
    print(f'   S51 depth solver: N={_eff_n} D={_depth} est={_depth_est} status={_depth_status}')

    bull_ctx = _build_news_context(report, all_articles, agent='bull', depth=_depth)
    bear_ctx = _build_news_context(report, all_articles, agent='bear', depth=_depth)
    swan_ctx = _build_news_context(report, all_articles, weak_articles, agent='swan', depth=_depth)
    ost_ctx  = _build_news_context(report, all_articles, agent='ostrich', depth=_depth)
    arb_ctx  = _build_news_context(report, all_articles, agent='arbitrator', depth=_depth)

    # S61 GROUNDING GATE (SHADOW): detect + log only -- zero behaviour change.
    # Basket = every article the debate was grounded in (scored + weak). Whitelist =
    # the shared build_grounding_whitelist() contract (GT-5 S73) -- mad_runner's
    # save-time scoring calls the SAME builder, so shadow and save cannot drift.
    _grounding_basket = list(all_articles or []) + list(weak_articles or [])
    _grounding_whitelist = build_grounding_whitelist(report)
    grounding_shadow = {'consultant_hits': [], 'arb_hits': [], 'total': 0}

    def _shadow_check(reply, label, bucket):
        """Run the grounding gate on one reply; never break the pipeline.

        Recording is UNCHANGED from S61: every hit still lands in grounding_shadow
        regardless of what the gate later does with the verdict. Now also returns
        the non-dialect hit_count so E-2 can act on it, or None if the check could
        not run (=> caller must fail open).
        """
        try:
            _g = check_grounding(reply, _grounding_basket, _grounding_whitelist,
                                 location=label)
            grounding_shadow[bucket].extend(_g['hits'])
            return _g['hit_count']
        except Exception as _ge:
            print('  Grounding gate (shadow) skipped ' + label + ': ' + str(_ge)[:60])
            return None

    def _gate_consultant(reply, label):
        """GT-5 E-2: withhold an ungrounded consultant reply from the agent it coaches.

        Returns the text the AGENT should see -- the reply itself, or the neutral
        marker when the shadow verdict says >= GROUNDING_GATE_T ungrounded spans.
        The gate acts ON the shadow verdict; it never suppresses the recording of it.

        FAIL-OPEN throughout: an unrunnable check (None) or ANY exception passes the
        reply through ungated and logs. Starving an agent on a gate bug is worse than
        one ungrounded reply reaching it -- the save-time scorer and the history
        filter are still downstream of this.
        """
        try:
            _n = _shadow_check(reply, label, 'consultant_hits')
            if _n is not None and _n >= GROUNDING_GATE_T:
                print('  GATED ' + label + ' ' + str(_n) + ' hits')
                return GROUNDING_WITHHELD_MARKER
            return reply
        except Exception as _ge:
            print('  Grounding gate (E-2) failed open for ' + label + ': ' + str(_ge)[:60])
            return reply

    dominant_pillar = _detect_dominant_pillar(all_articles)
    pillar_instruction = _get_pillar_arb_instruction(dominant_pillar)
    print(f'   Dominant pillar: {dominant_pillar.upper()} -- {pillar_instruction[:60]}...')
    history = _get_debate_history()
    escalation = report.get('escalation_level', '')
    risk_level = report.get('risk_level', 'Medium')
    weakness = report.get('weakness_identified', '')
    dark_side = report.get('dark_side_detected', '')

    # ============================================================
    # AGENT / CONSULTANT / ARBITRATOR SYSTEM PROMPTS
    # MAD REDEFINITION: now module-level constants (GNI_WALL, SENIOR_FOUNDATION,
    # GROUNDING_RULE, BULL/BEAR/SWAN/OSTRICH, *_CONS via _consultant(), ARB_FINAL).
    # Call sites, injection wrappers, JSON parser and _validate_mad_output unchanged.
    # ============================================================
    # ============================================================
    # ROUND 1
    # Each agent gets its own context (article pool + sort order)
    # ============================================================
    verdict_trend = history.get('verdict_trend', '')
    if verdict_trend:
        print(f'  Verdict trend: {verdict_trend[:100]}')
    print('   Round 1: Opening positions...')

    debate_history_block = '\n\nDEBATE HISTORY:\n' + (verdict_trend + '\n\n' if verdict_trend else '')

    bull_r1 = _call_agent(BULL,
        bull_ctx + debate_history_block + _fmt_history(history['bull'])
        + '\n\nROUND 1: Opening position on FUTURE THREATS.', 500)

    bear_r1 = _call_agent(BEAR,
        bear_ctx + debate_history_block + _fmt_history(history['bear'])
        + '\n\nROUND 1: Opening position on FUTURE THREATS.', 500)

    swan_r1 = _call_agent(SWAN,
        swan_ctx + debate_history_block + _fmt_history(history['black_swan'])
        + '\n\nROUND 1: Focus on LOW-SCORING articles others ignore. Name a specific one.', 500)

    ost_r1 = _call_agent(OSTRICH,
        ost_ctx + debate_history_block + _fmt_history(history['ostrich'])
        + '\n\nROUND 1: Name the specific threat being ignored.', 500)

    round1 = {'bull': bull_r1, 'bear': bear_r1, 'black_swan': swan_r1, 'ostrich': ost_r1}

    # Consultant coaching Round 1
    print('  Waiting 15s before consultant calls (TPM soft limit protection)...')
    time.sleep(15)
    print('   Personal consultants coaching Round 1...')
    r1_cons_ctx = (
        'REPORT: ' + report.get('title', '') + '\n'
        'ESCALATION: ' + report.get('escalation_level', '') + '\n\n'
        'ROUND 1 POSITIONS (compressed):\n'
        'Bull: '        + _compress(bull_r1, 60) + '\n'
        'Bear: '        + _compress(bear_r1, 60) + '\n'
        'Black Swan: '  + _compress(swan_r1, 60) + '\n'
        'Ostrich: '     + _compress(ost_r1, 60) + '\n'
    )
    c1_bull = _call_agent(BULL_CONS,    r1_cons_ctx + '\n\nCoach Bull. Push harder for Round 2.', 250)
    c1_bear = _call_agent(BEAR_CONS,    r1_cons_ctx + '\n\nCoach Bear. Push harder for Round 2.', 250)
    c1_swan = _call_agent(SWAN_CONS,    r1_cons_ctx + '\n\nCoach Black Swan. Push deeper for Round 2.', 250)
    c1_ost  = _call_agent(OSTRICH_CONS, r1_cons_ctx + '\n\nCoach Ostrich. Push harder for Round 2.', 250)
    arb_c1 = {'bull': c1_bull, 'bear': c1_bear, 'black_swan': c1_swan, 'ostrich': c1_ost}

    # SEAM 1 (S61 SHADOW + GT-5 E-2 GATE): R1 consultant replies -- the infection vector.
    # arb_c1 above stays RAW on purpose: it is the public /debate exhibit
    # (mad_arb_feedbacks) and mad_quality's scoring input. Only arb_c1_gated -- what
    # the AGENTS are prompted with -- is sanitized. Exhibits public, loop clean.
    arb_c1_gated = {
        'bull':       _gate_consultant(c1_bull, 'c1_bull'),
        'bear':       _gate_consultant(c1_bear, 'c1_bear'),
        'black_swan': _gate_consultant(c1_swan, 'c1_swan'),
        'ostrich':    _gate_consultant(c1_ost,  'c1_ost'),
    }

    print('  Waiting 45s between rounds (Groq rate limit protection)...')
    time.sleep(45)

    # ============================================================
    # ROUND 2
    # Shared round1 summary + agent-specific context
    # ============================================================
    print('   Round 2: Refined positions...')
    round1_summary = (
        '\n\nROUND 1 [summary]:\nBull: ' + _compress(bull_r1) +
        '\nBear: ' + _compress(bear_r1) +
        '\nBlack Swan: ' + _compress(swan_r1) +
        '\nOstrich: ' + _compress(ost_r1) + '\n\n'
    )

    bull_r2 = _call_agent(BULL,
        bull_ctx + round1_summary
        + 'PERSONAL CONSULTANT TO YOU: ' + arb_c1_gated.get('bull', '')
        + '\n\nROUND 2: Write a FRESH argument. Address feedback.', 500)

    bear_r2 = _call_agent(BEAR,
        bear_ctx + round1_summary
        + 'PERSONAL CONSULTANT TO YOU: ' + arb_c1_gated.get('bear', '')
        + '\n\nROUND 2: Respond. Address feedback.', 500)

    swan_r2 = _call_agent(SWAN,
        swan_ctx + round1_summary
        + 'PERSONAL CONSULTANT TO YOU: ' + arb_c1_gated.get('black_swan', '')
        + '\n\nROUND 2: Challenge Bull and Bear. Go deeper on your weak signal.', 500)

    ost_r2 = _call_agent(OSTRICH,
        ost_ctx + round1_summary
        + 'PERSONAL CONSULTANT TO YOU: ' + arb_c1_gated.get('ostrich', '')
        + '\n\nROUND 2: Name who is in denial and the cost.', 500)

    round2 = {'bull': bull_r2, 'bear': bear_r2, 'black_swan': swan_r2, 'ostrich': ost_r2}

    # Consultant coaching Round 2 -- includes R1 feedback (fixes contextual amnesia)
    print('  Waiting 15s before consultant calls (TPM soft limit protection)...')
    time.sleep(15)
    print('   Personal consultants coaching Round 2...')
    r2_cons_ctx = (
        'REPORT: ' + report.get('title', '') + '\n'
        'ESCALATION: ' + report.get('escalation_level', '') + '\n\n'
        'YOUR ROUND 1 FEEDBACK (already given -- do NOT repeat this):\n'
        'Bull feedback R1: '       + _compress(c1_bull, 40) + '\n'
        'Bear feedback R1: '       + _compress(c1_bear, 40) + '\n'
        'Black Swan feedback R1: ' + _compress(c1_swan, 40) + '\n'
        'Ostrich feedback R1: '    + _compress(c1_ost,  40) + '\n\n'
        'ROUND 2 POSITIONS (what agent did with your feedback):\n'
        'Bull: '        + _compress(bull_r2, 60) + '\n'
        'Bear: '        + _compress(bear_r2, 60) + '\n'
        'Black Swan: '  + _compress(swan_r2, 60) + '\n'
        'Ostrich: '     + _compress(ost_r2, 60) + '\n'
    )
    c2_bull = _call_agent(BULL_CONS,    r2_cons_ctx + '\n\nPush Bull to maximum for Round 3 final.', 250)
    c2_bear = _call_agent(BEAR_CONS,    r2_cons_ctx + '\n\nPush Bear to maximum for Round 3 final.', 250)
    c2_swan = _call_agent(SWAN_CONS,    r2_cons_ctx + '\n\nPush Black Swan to maximum for Round 3 final.', 250)
    c2_ost  = _call_agent(OSTRICH_CONS, r2_cons_ctx + '\n\nPush Ostrich to maximum for Round 3 final.', 250)
    arb_c2 = {'bull': c2_bull, 'bear': c2_bear, 'black_swan': c2_swan, 'ostrich': c2_ost}

    # SEAM 2 (S61 SHADOW + GT-5 E-2 GATE): R2 consultant replies -- the last coaching
    # that reaches an agent before R3, and R3 is what the Arbitrator reads. arb_c2
    # stays RAW for the exhibit; arb_c2_gated is what the AGENTS see.
    arb_c2_gated = {
        'bull':       _gate_consultant(c2_bull, 'c2_bull'),
        'bear':       _gate_consultant(c2_bear, 'c2_bear'),
        'black_swan': _gate_consultant(c2_swan, 'c2_swan'),
        'ostrich':    _gate_consultant(c2_ost,  'c2_ost'),
    }

    print('  Waiting 45s between rounds (Groq rate limit protection)...')
    time.sleep(45)

    # ============================================================
    # ROUND 3
    # Shared R1+R2 history + agent-specific context
    # ============================================================
    print('   Round 3: Final positions...')
    round_history = (
        '\n\nR1 [summary] Bull: ' + _compress(bull_r1) +
        '\nR1 Bear: ' + _compress(bear_r1) +
        '\nR1 Swan: ' + _compress(swan_r1) +
        '\nR1 Ostrich: ' + _compress(ost_r1) +
        '\n\nR2 Bull: ' + bull_r2 +
        '\nR2 Bear: ' + bear_r2 +
        '\nR2 Swan: ' + swan_r2 +
        '\nR2 Ostrich: ' + ost_r2 + '\n\n'
    )

    bull_r3 = _call_agent(BULL,
        bull_ctx + round_history
        + 'FINAL COACHING: ' + arb_c2_gated.get('bull', '')
        + '\n\nROUND 3 FINAL: Write a FRESH sharpest argument in 5-7 sentences. Changed view?', 600)

    bear_r3 = _call_agent(BEAR,
        bear_ctx + round_history
        + 'FINAL COACHING: ' + arb_c2_gated.get('bear', '')
        + '\n\nROUND 3 FINAL: Sharpest position in 5-7 sentences. Changed view?', 600)

    swan_r3 = _call_agent(SWAN,
        swan_ctx + round_history
        + 'FINAL COACHING: ' + arb_c2_gated.get('black_swan', '')
        + '\n\nROUND 3 FINAL: Name the ONE thing nobody else is watching. 5-7 sentences.', 600)

    ost_r3 = _call_agent(OSTRICH,
        ost_ctx + round_history
        + 'FINAL COACHING: ' + arb_c2_gated.get('ostrich', '')
        + '\n\nROUND 3 FINAL: Name the institution in denial and cost of inaction. 5-7 sentences.', 600)

    round3 = {'bull': bull_r3, 'bear': bear_r3, 'black_swan': swan_r3, 'ostrich': ost_r3}

    print('  Waiting 90s before arbitrator synthesis (Groq rate limit protection)...')
    time.sleep(90)

    # ============================================================
    # ARBITRATOR FINAL SYNTHESIS
    # Uses arb_ctx (scored articles, highest significance)
    # ============================================================
    print('   Arbitrator final synthesis...')
    arb_final_user = (
        arb_ctx + '\n\n'
        '=== R1 [summary] ===\nBull: ' + _compress(bull_r1) + '\nBear: ' + _compress(bear_r1) +
        '\nSwan: ' + _compress(swan_r1) + '\nOstrich: ' + _compress(ost_r1) + '\n\n'
        '=== R2 [summary] ===\nBull: ' + _compress(bull_r2) + '\nBear: ' + _compress(bear_r2) +
        '\nSwan: ' + _compress(swan_r2) + '\nOstrich: ' + _compress(ost_r2) + '\n\n'
        '=== R3 [final] ===\nBull: ' + bull_r3 + '\nBear: ' + bear_r3
        + '\nSwan: ' + swan_r3 + '\nOstrich: ' + ost_r3 + '\n\n'
        + ('Weakness: ' + weakness + '\n' if weakness else '')
        + ('Dark side: ' + dark_side + '\n' if dark_side and dark_side != 'None' else '')
        + 'Escalation: ' + escalation + ' | Risk: ' + risk_level + '\n\n'
        + 'PILLAR WEIGHTING: ' + pillar_instruction + '\n\n'
        + 'Deliver final synthesis as JSON only.'
    )

    # NN-5: Hard constraints for high escalation
    _hard_constraints = []
    _high_escalation = (risk_level.upper() in ('HIGH', 'CRITICAL') or
                        'CRITICAL' in escalation.upper() or 'HIGH' in escalation.upper())
    if _high_escalation:
        if swan_r3 and not swan_r3.startswith('[Agent error'):
            _hard_constraints.append(
                'BLACK SWAN MANDATORY CONSTRAINT (unknown danger -- cannot be dismissed): '
                + _compress(swan_r3, 60))
        if ost_r3 and not ost_r3.startswith('[Agent error'):
            _hard_constraints.append(
                'OSTRICH MANDATORY CONSTRAINT (ignored reality -- cannot be dismissed): '
                + _compress(ost_r3, 60))
    if _hard_constraints:
        constraint_block = ('HARD CONSTRAINTS -- YOU MUST ADDRESS THESE IN YOUR VERDICT:\n'
                            + '\n'.join(_hard_constraints) + '\n\n')
        arb_final_user = constraint_block + arb_final_user
        print(f'  NN-5: {len(_hard_constraints)} hard constraint(s) prepended to Arbitrator prompt')

    arb_final_raw = _call_arbitrator(ARB_FINAL, arb_final_user, 600, expect_json=True)

    # SEAM 3 (S61 SHADOW -- OBSERVE/LOG ONLY, ratified): grounding gate on the
    # Arbitrator's final output. The W-02 retry machinery lives INSIDE
    # _call_arbitrator; we check AFTER it returns.
    # DELIBERATELY NOT GATED (GT-5 design): arb output is never withheld or altered.
    # It is the verdict itself -- withholding it would destroy the run's product,
    # and there is no downstream consumer to protect (nothing reads it but the JSON
    # parser). Arbitrator-level hits are the ALARM class: they mean fabrication
    # already reached the verdict, which is grounding_watch's signal to raise RED,
    # not something to paper over here. E-2 gates the consultant->agent seam so this
    # seam has less to alarm about. Return value intentionally ignored.
    _shadow_check(arb_final_raw, 'arb_final', 'arb_hits')
    grounding_shadow['total'] = (len(grounding_shadow['consultant_hits']) +
                                 len(grounding_shadow['arb_hits']))
    if grounding_shadow['total']:
        print(f"  GROUNDING SHADOW: {len(grounding_shadow['consultant_hits'])} "
              f"consultant + {len(grounding_shadow['arb_hits'])} arb hit(s) "
              f"(shadow -- no action taken)")

    # Parse final verdict
    mad_verdict = 'neutral'
    mad_confidence = 0.5
    mad_reasoning = ''
    mad_blind_spot = ''
    mad_action_recommendation = ''
    short_focus_threats = ''
    long_shoot_threats = ''
    short_verify_days = 14
    long_verify_days = 180
    short_focus_opportunities = ''
    preparedness_path = ''
    # COMMIT 1: typed failure flag -- single source of truth for "no real verdict".
    # True => Arbitrator produced no usable verdict (429/error OR unparseable JSON).
    # neutral/0.5 are NOT the failure signal anymore; this flag is.
    mad_arb_failed = False

    _arb_is_error = (
        arb_final_raw.startswith('[Agent error') or
        '429' in arb_final_raw or
        'rate limit' in arb_final_raw.lower()
    )
    if _arb_is_error:
        print('  WARNING: Arbitrator call failed -- using safe defaults')
        print('  ARB RAW (logs only): ' + arb_final_raw[:400])
        mad_reasoning = ('Verdict unavailable this run -- the Arbitrator call was '
                         'rate-limited after the debate completed. The four-agent '
                         'debate transcript is complete; a fresh verdict comes from '
                         'the next scheduled run.')
        mad_arb_failed = True
    else:
        try:
            clean = arb_final_raw.replace('```json', '').replace('```', '').strip()
            try:
                arb_json = json.loads(clean)
            except json.JSONDecodeError:
                start = clean.find('{')
                end = clean.rfind('}') + 1
                if start >= 0 and end > start:
                    arb_json = json.loads(clean[start:end])
                else:
                    raise json.JSONDecodeError('No JSON object found', clean, 0)
            mad_verdict = arb_json.get('verdict', 'neutral').lower()
            if mad_verdict not in VALID_VERDICTS:
                mad_verdict = 'neutral'
            mad_confidence = float(arb_json.get('confidence', 0.5))
            mad_confidence = max(0.0, min(1.0, mad_confidence))
            mad_reasoning = arb_json.get('reasoning', '')
            mad_blind_spot = arb_json.get('blind_spot_quadrant', '')
            blind_exp = arb_json.get('blind_spot_explanation', '')
            if blind_exp:
                mad_blind_spot = mad_blind_spot + ' -- ' + blind_exp
            mad_action_recommendation = arb_json.get('action_recommendation', '')
            short_focus_threats = arb_json.get('short_focus_threats', '')
            long_shoot_threats = arb_json.get('long_shoot_threats', '')
            short_verify_days = int(arb_json.get('short_verify_days', 14))
            long_verify_days = int(arb_json.get('long_verify_days', 180))
            short_focus_opportunities = arb_json.get('short_focus_opportunities', '')
            preparedness_path = arb_json.get('preparedness_path', '')
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            print('  WARNING: Arbitrator JSON parse failed: ' + str(e)[:60])
            print('  ARB RAW (logs only): ' + arb_final_raw[:400])
            mad_reasoning = ('Verdict unavailable this run -- the Arbitrator response '
                             'could not be parsed. The four-agent debate transcript is '
                             'complete; a fresh verdict comes from the next scheduled run.')
            mad_arb_failed = True

    print(f'   Blind Spot:  {mad_blind_spot[:60]}')
    print(f'   Short Focus: {short_focus_threats[:60]}')
    print(f'   Long Shoot:  {long_shoot_threats[:60]}')
    print(f'   Verdict:     {mad_verdict} ({round(mad_confidence, 2)})')
    print(f'   Action:      {mad_action_recommendation[:60]}')

    if report_id:
        _save_predictions(report_id, short_focus_threats, long_shoot_threats,
                          short_verify_days, long_verify_days, round3)

    result = {
        'mad_bull_case':             bull_r3,
        'mad_bear_case':             bear_r3,
        'mad_black_swan_case':       swan_r3,
        'mad_ostrich_case':          ost_r3,
        'mad_verdict':               mad_verdict,
        'mad_confidence':            mad_confidence,
        'mad_arb_failed':            mad_arb_failed,
        'mad_reasoning':             mad_reasoning,
        'mad_blind_spot':            mad_blind_spot,
        'mad_action_recommendation': mad_action_recommendation,
        'short_focus_threats':       short_focus_threats,
        'long_shoot_threats':        long_shoot_threats,
        'short_verify_days':         short_verify_days,
        'long_verify_days':          long_verify_days,
        'short_focus_opportunities': short_focus_opportunities,
        'preparedness_path':         preparedness_path,
        'mad_round1_positions':      round1,
        'mad_round2_positions':      round2,
        'mad_round3_positions':      round3,
        'mad_arb_feedbacks':         {'round1': arb_c1, 'round2': arb_c2},
        'mad_historian_case':        '',
        'mad_risk_case':             '',
        'mad_depth':                 _depth,
        'mad_depth_est':             _depth_est,
        'mad_depth_status':          _depth_status,
        'mad_eff_n':                 _eff_n,
        'grounding_shadow':          grounding_shadow,  # S61 -- logged to mad_quality_log
    }

    return _validate_mad_output(result)


if __name__ == '__main__':
    print('Quadratic MAD v2 -- Test Run\n')
    test = {
        'title': 'Iran Threatens Hormuz',
        'summary': 'Iran moved forces to Hormuz after US sanctions.',
        'risk_level': 'High',
        'escalation_level': 'CRITICAL',
        'location_name': 'Iran',
    }
    r = run_mad_protocol(test, all_articles=[], weak_articles=[])
    print(f"Verdict:     {r['mad_verdict']}")
    print(f"Blind Spot:  {r['mad_blind_spot'][:80]}")
    print(f"Short Focus: {r['short_focus_threats'][:80]}")
    print(f"Long Shoot:  {r['long_shoot_threats'][:80]}")
    print(f"Action:      {r['mad_action_recommendation'][:80]}")
