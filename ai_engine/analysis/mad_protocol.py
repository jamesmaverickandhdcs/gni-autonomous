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
# ============================================================

import os
import json
import re
import time
from datetime import datetime, timezone, timedelta
from groq import Groq
from groq_guardian import validate_response  # GNI-R-234

client = Groq(api_key=os.getenv('GROQ_API_KEY'))
MODEL = os.getenv('GROQ_MAD_MODEL',
        os.getenv('GROQ_MODEL',
        os.getenv('GROQ_MODEL_FALLBACK', 'llama-3.3-70b-versatile')))

VALID_VERDICTS = ['bullish', 'bearish', 'neutral']

# S46 Phase 0 -- real token metering (observability only; no prompt/debate-logic change).
# Accumulates actual response.usage across every Groq call in one MAD run.
# Counts retries (real cost) and guardian-rejected responses (tokens were billed).
_TOKEN_USAGE = {'prompt': 0, 'completion': 0, 'total': 0, 'calls': 0}


def reset_token_usage():
    _TOKEN_USAGE.update({'prompt': 0, 'completion': 0, 'total': 0, 'calls': 0})


def get_token_usage():
    return dict(_TOKEN_USAGE)


def _call_agent(system_prompt: str, user_prompt: str, max_tokens: int = 400, expect_json: bool = False) -> str:
    for attempt in range(2):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt},
                ],
                max_tokens=max_tokens,
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
                print(f'  WARNING: groq_guardian rejected response: {validation["rejection_reason"]}')
                _log_safety_event('guardian_rejection', validation['rejection_reason'])
                return '[Agent error: ' + validation['rejection_reason'] + ']'
            return validation['sanitized']
        except Exception as e:
            err = str(e)
            is_rate_limit = '429' in err or 'rate_limit' in err.lower() or 'rate limit' in err.lower()
            if is_rate_limit and attempt == 0:
                print('  WARNING: Groq 429 rate limit -- sleeping 40s before retry...')
                time.sleep(40)
                continue
            return '[Agent error: ' + err[:100] + ']'
    return '[Agent error: max retries exceeded]'


def _call_arbitrator(system_prompt: str, user_prompt: str, max_tokens: int = 600, expect_json: bool = True) -> str:
    """W-02: TPM-aware arbitrator call with one extra retry."""
    result = _call_agent(system_prompt, user_prompt, max_tokens, expect_json)
    if (result.startswith('[Agent error') and
            ('429' in result or 'rate_limit' in result.lower() or 'rate limit' in result.lower())):
        print('  WARNING: Arbitrator 429 -- W-02 TPM wait 60s before final retry...')
        time.sleep(60)
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
                        weak_articles: list = None, agent: str = 'general') -> str:
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
            smr = art.get('summary', '')[:100].replace('\n', ' ')
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
            .select('mad_bull_case,mad_bear_case,mad_black_swan_case,mad_ostrich_case,short_focus_threats,long_shoot_threats,mad_verdict,mad_confidence,created_at') \
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
            for agent in ['bull', 'bear', 'black_swan', 'ostrich']:
                key_name = 'mad_' + agent + '_case'
                if row.get(key_name):
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
    bull_ctx = _build_news_context(report, all_articles, agent='bull')
    bear_ctx = _build_news_context(report, all_articles, agent='bear')
    swan_ctx = _build_news_context(report, all_articles, weak_articles, agent='swan')
    ost_ctx  = _build_news_context(report, all_articles, agent='ostrich')
    arb_ctx  = _build_news_context(report, all_articles, agent='arbitrator')

    dominant_pillar = _detect_dominant_pillar(all_articles)
    pillar_instruction = _get_pillar_arb_instruction(dominant_pillar)
    print(f'   Dominant pillar: {dominant_pillar.upper()} -- {pillar_instruction[:60]}...')
    history = _get_debate_history()
    escalation = report.get('escalation_level', '')
    risk_level = report.get('risk_level', 'Medium')
    weakness = report.get('weakness_identified', '')
    dark_side = report.get('dark_side_detected', '')

    # ============================================================
    # AGENT SYSTEM PROMPTS -- S37 quality patches
    # ============================================================

    WALL = ('GNI MISSION: "FUTURE THREATS" is GNI\'s VISION -- early warning of threats AND '
            'opportunities so people can prepare. Within that mission, argue ONLY your own '
            'character\'s genuine position. The vision never overrides the character. ')

    BULL = (WALL +
            'You are the Bull Agent. Quadrant: Upper-Right -- Known Positives. '
            'Current date: May 2026. All timelines must be relative to 2026. '
            'You are an OPTIMIST who steelmans the genuine positive read of this event. '
            'Focus: what concretely STABILISES, DE-ESCALATES, or IMPROVES because of it -- '
            'real opportunity, real recovery, real cooperation -- NOT the threat of inaction. '
            'Name the actors, the mechanism, and the specific opportunity. '
            'Cite specific intelligence from the articles provided. '
            'SYNTHESIS RULE: Do NOT copy or append to previous rounds. Write a completely fresh argument each round. '
            'PRE-BUTTAL RULE: Anticipate Bear\'s strongest counter and address it before they make it. '
            '3-4 sentences.')

    BEAR = (WALL +
            'You are the Bear Agent. Quadrant: Lower-Right -- Known Negatives. '
            'Current date: May 2026. All timelines must be relative to 2026. '
            'Focus: FUTURE THREATS from known risks and systemic vulnerabilities. '
            'Name which systems are fragile, why, and what mechanism drives the break. '
            'QUANTIFY: Support claims with specific figures where known (percentages, volumes, dollar amounts). '
            'SCOPE: Broaden vulnerability beyond energy -- include semiconductors, critical minerals, manufacturing. '
            'RISK PRICING: Argue that the THREAT of disruption causes damage through risk premiums '
            'even before any physical event occurs. '
            'Ground every claim in the articles provided. 3-4 sentences.')

    SWAN = (WALL +
            'You are the Black Swan Agent. Quadrant: Upper-Left -- Unknown Negatives. '
            'Current date: May 2026. '
            'Focus: FUTURE THREATS nobody is modelling. '
            'You are receiving LOW-SCORING articles that others dismissed -- these are your hunting ground. '
            'Name a specific article from this list and explain exactly why it deserves more attention. '
            'CREDIBILITY RULE: Your threat MUST be grounded in real-world evidence -- '
            'a real technology, real actor, real event. '
            'UAP RULE: If referencing unidentified phenomena, frame as adversarial drone/UAP/next-gen UAS '
            'from a known state actor (China, Russia) -- never as speculative fiction or aliens. '
            'FALLOUT RULE: Present consequences as a numbered chain: '
            '1. Detection Failure  2. Escalation  3. Geopolitical Retaliation. '
            'The surprise comes from the CONNECTION nobody made -- not from an impossible scenario. '
            '3-4 sentences.')

    OSTRICH = (WALL +
               'You are the Ostrich Agent. Quadrant: Lower-Left -- Ignored Realities. '
               'Current date: May 2026. '
               'Focus: FUTURE THREATS already visible but collectively ignored. '
               'JURISDICTION RULE: Before naming an institution, verify it has direct authority '
               'over the threat you are describing. If it does not, find the correct institution. '
               'PRIMARY FRAME: Find the GAP between two institutions -- where Institution A holds '
               'the risk but has NOT communicated it to Institution B, and that silence IS the hidden threat. '
               'Name the specific institutions, the specific gap, the specific cost of that silence. '
               'Cite evidence from the articles provided. 3-4 sentences. Name names.')

    # ============================================================
    # CONSULTANT SYSTEM PROMPTS -- S37 quality patches
    # ============================================================

    BULL_CONS = ('You are Bull\'s personal strategist. Your ONLY loyalty is Bull. '
                 'FOUNDATION CHECK: If Bull\'s argument contains a factual error or logical contradiction, '
                 'correct it FIRST. Do NOT push harder on a wrong foundation -- fix it before pushing. '
                 'NO REPEAT RULE: Read Bull\'s current position carefully. '
                 'Do NOT repeat feedback Bull has already implemented. '
                 'THEN: Find the specific opportunity Bull understated. '
                 'Name the actor and what they must do. '
                 'No invented numbers. No dates from before 2026. '
                 'Push Bull to cite actual article evidence. No praise. 3-4 sentences.')

    BEAR_CONS = ('You are Bear\'s personal strategist. Your ONLY loyalty is Bear. '
                 'FOUNDATION CHECK: If Bear\'s argument contains a factual error or logical contradiction, '
                 'correct it FIRST. Do NOT push harder on a wrong foundation -- fix it before pushing. '
                 'NO REPEAT RULE: Read Bear\'s current position carefully. '
                 'Do NOT repeat feedback Bear has already implemented. '
                 'THEN: Find the specific fragility Bear understated. '
                 'Name what breaks first and who is exposed. '
                 'No invented dates or percentages. Every claim must trace back to article evidence. '
                 'No praise. 3-4 sentences.')

    SWAN_CONS = ('You are Black Swan\'s personal strategist. Your ONLY loyalty is Black Swan. '
                 'GROUNDING CHECK: If Swan drifts into fiction or unverifiable speculation, redirect it FIRST. '
                 'Do NOT push Swan toward UFOs, aliens, or scenarios without real-world grounding. '
                 'Push Swan toward MORE SPECIFIC real evidence -- a named adversarial technology, a named state actor. '
                 'NO REPEAT RULE: Read Swan\'s current position carefully. '
                 'Do NOT repeat feedback Swan has already implemented. '
                 'Push Swan to name the exact triggering event -- not a general cascade, a specific grounded one. '
                 'No invented scenarios. Stay in article evidence. No praise. 3-4 sentences.')

    OSTRICH_CONS = ('You are Ostrich\'s personal strategist. Your ONLY loyalty is Ostrich. '
                    'JURISDICTION CHECK: Verify Ostrich named an institution with actual authority over the threat. '
                    'If the institution is wrong, redirect to the correct one FIRST before pushing harder. '
                    'SILO-GAP FRAME: Push Ostrich to identify which institution holds the risk and which one '
                    'is NOT being told -- frame that communication gap as the core hidden threat. '
                    'Make the inertia argument and the communication failure so specific it cannot be dismissed. '
                    'No praise. 3-4 sentences. Push Ostrich harder.')

    ARB_FINAL = ('You are the Arbitrator -- Strategic Synthesiser. '
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
                 'drone/UAS technology from a named state actor -- not UFOs or aliens. '
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
                 '"preparedness_path": "what actors can do to prepare or capture"}')

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
        + '\n\nROUND 1: Opening position on FUTURE THREATS.', 350)

    bear_r1 = _call_agent(BEAR,
        bear_ctx + debate_history_block + _fmt_history(history['bear'])
        + '\n\nROUND 1: Opening position on FUTURE THREATS.', 350)

    swan_r1 = _call_agent(SWAN,
        swan_ctx + debate_history_block + _fmt_history(history['black_swan'])
        + '\n\nROUND 1: Focus on LOW-SCORING articles others ignore. Name a specific one.', 350)

    ost_r1 = _call_agent(OSTRICH,
        ost_ctx + debate_history_block + _fmt_history(history['ostrich'])
        + '\n\nROUND 1: Name the specific threat being ignored.', 350)

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
        + 'PERSONAL CONSULTANT TO YOU: ' + arb_c1.get('bull', '')
        + '\n\nROUND 2: Write a FRESH argument. Address feedback.', 350)

    bear_r2 = _call_agent(BEAR,
        bear_ctx + round1_summary
        + 'PERSONAL CONSULTANT TO YOU: ' + arb_c1.get('bear', '')
        + '\n\nROUND 2: Respond. Address feedback.', 350)

    swan_r2 = _call_agent(SWAN,
        swan_ctx + round1_summary
        + 'PERSONAL CONSULTANT TO YOU: ' + arb_c1.get('black_swan', '')
        + '\n\nROUND 2: Challenge Bull and Bear. Go deeper on your weak signal.', 350)

    ost_r2 = _call_agent(OSTRICH,
        ost_ctx + round1_summary
        + 'PERSONAL CONSULTANT TO YOU: ' + arb_c1.get('ostrich', '')
        + '\n\nROUND 2: Name who is in denial and the cost.', 350)

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
        + 'FINAL COACHING: ' + arb_c2.get('bull', '')
        + '\n\nROUND 3 FINAL: Write a FRESH sharpest argument in 5-7 sentences. Changed view?', 600)

    bear_r3 = _call_agent(BEAR,
        bear_ctx + round_history
        + 'FINAL COACHING: ' + arb_c2.get('bear', '')
        + '\n\nROUND 3 FINAL: Sharpest position in 5-7 sentences. Changed view?', 600)

    swan_r3 = _call_agent(SWAN,
        swan_ctx + round_history
        + 'FINAL COACHING: ' + arb_c2.get('black_swan', '')
        + '\n\nROUND 3 FINAL: Name the ONE thing nobody else is watching. 5-7 sentences.', 600)

    ost_r3 = _call_agent(OSTRICH,
        ost_ctx + round_history
        + 'FINAL COACHING: ' + arb_c2.get('ostrich', '')
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

    _arb_is_error = (
        arb_final_raw.startswith('[Agent error') or
        '429' in arb_final_raw or
        'rate limit' in arb_final_raw.lower()
    )
    if _arb_is_error:
        print('  WARNING: Arbitrator call failed -- using safe defaults')
        mad_reasoning = arb_final_raw
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
            mad_reasoning = arb_final_raw

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
