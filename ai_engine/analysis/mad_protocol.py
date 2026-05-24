# ============================================================
# GNI MAD Protocol v2 -- Quadratic Debate Framework
# Bull -> Bear -> Black Swan -> Ostrich -> Arbitrator
# Personal consultants coach R1+R2 (GNI-R-235). Arbitrator final R3 only.
# Grounded in ALL relevant articles not just top 5
# Short Focus (7-30 days) + Long Shoots (3-24 months)
# Predictions saved to debate_predictions table
# 21 Groq calls per run
# GNI-R-237: GROQ_MAD_MODEL=gpt-oss-120b (all 21 calls). GROQ_MODEL fallback.
# GROQ_API_KEY_2 removed -- same account = same pool, no isolation benefit.
# S37 PATCHES:
#   BULL:       SYNTHESIS RULE (no copy-paste) + PRE-BUTTAL RULE
#   BEAR:       QUANTIFY + SCOPE (beyond oil) + RISK PRICING
#   SWAN:       CREDIBILITY ANCHOR + UAP RULE + FALLOUT CHAIN
#   OSTRICH:    JURISDICTION RULE + INTER-AGENCY SILO-GAP primary frame
#   ALL CONS:   FOUNDATION CHECK first + NO REPEAT RULE
#   SWAN CONS:  GROUNDING CHECK (no fiction push)
#   OSTRICH CONS: JURISDICTION CHECK + SILO-GAP frame push
#   ARBITRATOR: SELF-CONSISTENCY + ACTION PRIORITY + SPECIFICITY + UAP RULE
#   R2 CTX:     Consultant contextual memory -- R1 feedback injected into R2 ctx
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
        os.getenv('GROQ_MODEL_FALLBACK', 'llama-3.3-70b-versatile')))  # GNI-R-237: gpt-oss-120b -> scout -> fallback

VALID_VERDICTS = ['bullish', 'bearish', 'neutral']


def _call_agent(system_prompt: str, user_prompt: str, max_tokens: int = 400, expect_json: bool = False) -> str:
    # GNI-R-107: Rate-limit-aware Groq call with 429 retry
    # Attempt 1: primary client (GROQ_API_KEY)
    # If 429:   sleep 40s -> Attempt 2: primary client
    # If fails: return error string (pipeline continues)
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
            raw = response.choices[0].message.content.strip()
            # GNI-R-234: validate ALL Groq responses before processing
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
    """W-02: TPM-aware arbitrator call with one extra retry.
    Arbitrator is the most critical call -- gets 3 total attempts vs 2 for agents.
    If _call_agent returns a 429/rate-limit error, waits 60s and retries once more.
    """
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
        pass  # Safety logging must NEVER break the pipeline


def _build_news_context(report: dict, all_articles: list) -> str:
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
    if not all_articles:
        return report_ctx
    by_pillar = {'geo': [], 'fin': [], 'tech': [], 'other': []}
    for art in all_articles:
        p = art.get('pillar', 'other').lower()
        by_pillar[p if p in by_pillar else 'other'].append(art)
    articles_ctx = '\nINTELLIGENCE BASE -- ALL RELEVANT ARTICLES:\n'
    for pillar, arts in by_pillar.items():
        if not arts:
            continue
        articles_ctx += f'\n[{pillar.upper()} -- {len(arts)} articles]\n'
        for art in arts[:15]:
            articles_ctx += f"  - [{art.get('source','')}] {art.get('title','')[:80]} (score:{art.get('stage3_score',0)})\n"
    total = sum(len(v) for v in by_pillar.values())
    articles_ctx += f'\nTotal relevant: {total}\n'
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
    # NP-4: verdict_trend fixes Gap 6 (Zero Cross-Run Memory) + Pattern Match Bias
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
        # Build verdict trend from last 7 runs (newest first)
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
        # Agent history -- last 3 only (token budget)
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
    """
    P4: Token compression -- truncate earlier round responses.
    Takes first max_words words to preserve key argument.
    350 tokens -> ~40 tokens = 88% reduction per carried response.
    Only used for historical rounds (R1 in R3, R1+R2 in Arb).
    Most recent round always passes full text.
    """
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


def run_mad_protocol(report: dict, all_articles: list = None, report_id: str = None) -> dict:
    if all_articles is None:
        all_articles = []

    news_ctx = _build_news_context(report, all_articles)
    dominant_pillar = _detect_dominant_pillar(all_articles)
    pillar_instruction = _get_pillar_arb_instruction(dominant_pillar)
    print(f'   Dominant pillar: {dominant_pillar.upper()} -- {pillar_instruction[:60]}...')
    history = _get_debate_history()
    escalation = report.get('escalation_level', '')
    risk_level = report.get('risk_level', 'Medium')
    weakness = report.get('weakness_identified', '')
    dark_side = report.get('dark_side_detected', '')

    # ============================================================
    # AGENT SYSTEM PROMPTS
    # ============================================================

    # PATCH 1: SYNTHESIS RULE + PRE-BUTTAL RULE
    BULL = ('You are the Bull Agent. Quadrant: Upper-Right -- Known Positives. '
            'Current date: May 2026. All timelines must be relative to 2026. '
            'Focus: FUTURE THREATS from missed opportunities. '
            'Greatest threat: OPPORTUNITY COST -- failing to act on what we know. '
            'Cite specific intelligence from the articles provided. Name actors and mechanisms. '
            'SYNTHESIS RULE: Do NOT copy or append to previous rounds. Write a completely fresh argument each round. '
            'PRE-BUTTAL RULE: Anticipate Bear\'s strongest counter and address it before they make it. '
            '3-4 sentences.')

    # PATCH 2: QUANTIFY + SCOPE beyond oil + RISK PRICING
    BEAR = ('You are the Bear Agent. Quadrant: Lower-Right -- Known Negatives. '
            'Current date: May 2026. All timelines must be relative to 2026. '
            'Focus: FUTURE THREATS from known risks and systemic vulnerabilities. '
            'Name which systems are fragile, why, and what mechanism drives the break. '
            'QUANTIFY: Support claims with specific figures where known (percentages, volumes, dollar amounts). '
            'SCOPE: Broaden vulnerability beyond energy -- include semiconductors, critical minerals, manufacturing. '
            'RISK PRICING: Argue that the THREAT of disruption causes damage through risk premiums '
            'even before any physical event occurs. '
            'Ground every claim in the articles provided. 3-4 sentences.')

    # PATCH 3: CREDIBILITY ANCHOR + UAP RULE + numbered FALLOUT CHAIN
    SWAN = ('You are the Black Swan Agent. Quadrant: Upper-Left -- Unknown Negatives. '
            'Current date: May 2026. '
            'Focus: FUTURE THREATS nobody is modelling. '
            'Look for WEAK SIGNALS in low-scoring articles others dismiss. '
            'Name a specific low-scoring article and explain exactly why it deserves more attention. '
            'CREDIBILITY RULE: Your threat MUST be grounded in real-world evidence -- '
            'a real technology, real actor, real event. '
            'UAP RULE: If referencing unidentified phenomena, frame as adversarial drone/UAP/next-gen UAS '
            'from a known state actor (China, Russia) -- never as speculative fiction or aliens. '
            'FALLOUT RULE: Present consequences as a numbered chain: '
            '1. Detection Failure  2. Escalation  3. Geopolitical Retaliation. '
            'The surprise comes from the CONNECTION nobody made -- not from an impossible scenario. '
            '3-4 sentences.')

    # PATCH 4: JURISDICTION RULE + INTER-AGENCY SILO-GAP as primary frame (full rewrite)
    OSTRICH = ('You are the Ostrich Agent. Quadrant: Lower-Left -- Ignored Realities. '
               'Current date: May 2026. '
               'Focus: FUTURE THREATS already visible but collectively ignored. '
               'JURISDICTION RULE: Before naming an institution, verify it has direct authority '
               'over the threat you are describing. If it does not, find the correct institution. '
               'PRIMARY FRAME: Find the GAP between two institutions -- where Institution A holds '
               'the risk but has NOT communicated it to Institution B, and that silence IS the hidden threat. '
               'Name the specific institutions, the specific gap, the specific cost of that silence. '
               'Cite evidence from the articles provided. 3-4 sentences. Name names.')

    # ============================================================
    # CONSULTANT SYSTEM PROMPTS
    # GNI-R-235: Personal consultants -- 100% loyal to their agent.
    # UNIVERSAL PATCH: FOUNDATION CHECK first + NO REPEAT RULE on all four.
    # ============================================================

    # PATCH 5: Bull consultant
    BULL_CONS = ('You are Bull\'s personal strategist. Your ONLY loyalty is Bull. '
                 'FOUNDATION CHECK: If Bull\'s argument contains a factual error or logical contradiction, '
                 'correct it FIRST. Do NOT push harder on a wrong foundation -- fix it before pushing. '
                 'NO REPEAT RULE: Read Bull\'s current position carefully. '
                 'Do NOT repeat feedback Bull has already implemented. '
                 'THEN: Find the specific opportunity Bull understated. '
                 'Name the actor and what they must do. '
                 'No invented numbers. No dates from before 2026. '
                 'Push Bull to cite actual article evidence. No praise. 3-4 sentences.')

    # PATCH 6: Bear consultant
    BEAR_CONS = ('You are Bear\'s personal strategist. Your ONLY loyalty is Bear. '
                 'FOUNDATION CHECK: If Bear\'s argument contains a factual error or logical contradiction, '
                 'correct it FIRST. Do NOT push harder on a wrong foundation -- fix it before pushing. '
                 'NO REPEAT RULE: Read Bear\'s current position carefully. '
                 'Do NOT repeat feedback Bear has already implemented. '
                 'THEN: Find the specific fragility Bear understated. '
                 'Name what breaks first and who is exposed. '
                 'No invented dates or percentages. Every claim must trace back to article evidence. '
                 'No praise. 3-4 sentences.')

    # PATCH 7: Swan consultant -- GROUNDING CHECK + no fiction push
    SWAN_CONS = ('You are Black Swan\'s personal strategist. Your ONLY loyalty is Black Swan. '
                 'GROUNDING CHECK: If Swan drifts into fiction or unverifiable speculation, redirect it FIRST. '
                 'Do NOT push Swan toward UFOs, aliens, or scenarios without real-world grounding. '
                 'Push Swan toward MORE SPECIFIC real evidence -- a named adversarial technology, a named state actor. '
                 'NO REPEAT RULE: Read Swan\'s current position carefully. '
                 'Do NOT repeat feedback Swan has already implemented. '
                 'Push Swan to name the exact triggering event -- not a general cascade, a specific grounded one. '
                 'No invented scenarios. Stay in article evidence. No praise. 3-4 sentences.')

    # PATCH 8: Ostrich consultant -- JURISDICTION CHECK + SILO-GAP frame push
    OSTRICH_CONS = ('You are Ostrich\'s personal strategist. Your ONLY loyalty is Ostrich. '
                    'JURISDICTION CHECK: Verify Ostrich named an institution with actual authority over the threat. '
                    'If the institution is wrong, redirect to the correct one FIRST before pushing harder. '
                    'SILO-GAP FRAME: Push Ostrich to identify which institution holds the risk and which one '
                    'is NOT being told -- frame that communication gap as the core hidden threat. '
                    'Make the inertia argument and the communication failure so specific it cannot be dismissed. '
                    'No praise. 3-4 sentences. Push Ostrich harder.')

    # PATCH 9: Arbitrator -- SELF-CONSISTENCY + ACTION PRIORITY + SPECIFICITY + UAP RULE
    ARB_FINAL = ('You are the Arbitrator -- Strategic Synthesiser. '
                 'After 3 rounds identify: '
                 '(1) BLIND SPOT QUADRANT -- most neglected. '
                 '(2) ACTION RECOMMENDATION -- one specific action now. '
                 '(3) SHORT FOCUS THREATS -- specific threats in next 7-30 days. '
                 '(4) LONG SHOOT THREATS -- structural threats over 3-24 months. '
                 '(5) Verdict and confidence. '
                 'SELF-CONSISTENCY RULE: Your short_focus_threats must be consistent with your reasoning baseline. '
                 'If you predict a direction change from the baseline, name the SPECIFIC catalyst that causes the flip. '
                 'ACTION PRIORITY RULE: Your primary action_recommendation must address the highest-probability threat. '
                 'Novel or low-probability threats appear as secondary recommendations only -- never as the primary. '
                 'SPECIFICITY RULE: Every ignored reality claim must name a specific institution, '
                 'specific gap, and specific consequence -- no vague placeholders. '
                 'UAP RULE: If referencing unidentified aerial phenomena, frame as adversarial '
                 'drone/UAS technology from a named state actor -- not UFOs or aliens. '
                 'Respond ONLY with valid JSON: '
                 '{"verdict": "bullish or bearish or neutral", '
                 '"confidence": 0.0-1.0, '
                 '"reasoning": "2-3 sentences", '
                 '"blind_spot_quadrant": "bull or bear or black_swan or ostrich", '
                 '"blind_spot_explanation": "why neglected", '
                 '"action_recommendation": "one specific action now", '
                 '"short_focus_threats": "threats in 7-30 days", '
                 '"short_verify_days": 14, '
                 '"long_shoot_threats": "structural threats 3-24 months", '
                 '"long_verify_days": 180}')

    # Round 1
    verdict_trend = history.get('verdict_trend', '')
    if verdict_trend:
        print(f'  Verdict trend: {verdict_trend[:100]}')
    print('   Round 1: Opening positions...')
    r1_base = news_ctx + '\n\nDEBATE HISTORY:\n' + (verdict_trend + '\n\n' if verdict_trend else '')
    bull_r1  = _call_agent(BULL,    r1_base + _fmt_history(history['bull'])        + '\n\nROUND 1: Opening position on FUTURE THREATS.', 350)
    bear_r1  = _call_agent(BEAR,    r1_base + _fmt_history(history['bear'])        + '\n\nROUND 1: Opening position on FUTURE THREATS.', 350)
    swan_r1  = _call_agent(SWAN,    r1_base + _fmt_history(history['black_swan'])  + '\n\nROUND 1: Focus on LOW-SCORING articles others ignore.', 350)
    ost_r1   = _call_agent(OSTRICH, r1_base + _fmt_history(history['ostrich'])     + '\n\nROUND 1: Name the specific threat being ignored.', 350)
    round1 = {'bull': bull_r1, 'bear': bear_r1, 'black_swan': swan_r1, 'ostrich': ost_r1}

    # GNI-R-235: Personal consultant coaching Round 1 -- 4 separate calls
    # S28-14: 15s sleep -- 8 back-to-back calls exceed Groq TPM soft limit
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

    # Round 2
    print('   Round 2: Refined positions...')
    r2_base = (news_ctx + '\n\nROUND 1 [summary]:\nBull: ' + _compress(bull_r1) +
               '\nBear: ' + _compress(bear_r1) +
               '\nBlack Swan: ' + _compress(swan_r1) +
               '\nOstrich: ' + _compress(ost_r1) + '\n\n')
    bull_r2  = _call_agent(BULL,    r2_base + 'PERSONAL CONSULTANT TO YOU: ' + arb_c1.get('bull','')       + '\n\nROUND 2: Write a FRESH argument. Address feedback.', 350)
    bear_r2  = _call_agent(BEAR,    r2_base + 'PERSONAL CONSULTANT TO YOU: ' + arb_c1.get('bear','')       + '\n\nROUND 2: Respond. Address feedback.', 350)
    swan_r2  = _call_agent(SWAN,    r2_base + 'PERSONAL CONSULTANT TO YOU: ' + arb_c1.get('black_swan','') + '\n\nROUND 2: Challenge Bull and Bear. Go deeper.', 350)
    ost_r2   = _call_agent(OSTRICH, r2_base + 'PERSONAL CONSULTANT TO YOU: ' + arb_c1.get('ostrich','')    + '\n\nROUND 2: Name who is in denial and the cost.', 350)
    round2 = {'bull': bull_r2, 'bear': bear_r2, 'black_swan': swan_r2, 'ostrich': ost_r2}

    # GNI-R-235: Personal consultant coaching Round 2 -- 4 separate calls
    # PATCH 10: R2 consultant context includes R1 feedback already given
    # Fixes consultant contextual amnesia -- consultant sees what it already said
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

    # Round 3
    print('   Round 3: Final positions...')
    r3_base = (news_ctx +
               '\n\nR1 [summary] Bull: ' + _compress(bull_r1) +
               '\nR1 Bear: ' + _compress(bear_r1) +
               '\nR1 Swan: ' + _compress(swan_r1) +
               '\nR1 Ostrich: ' + _compress(ost_r1) +
               '\n\nR2 Bull: ' + bull_r2 + '\nR2 Bear: ' + bear_r2 +
               '\nR2 Swan: ' + swan_r2 + '\nR2 Ostrich: ' + ost_r2 + '\n\n')
    bull_r3  = _call_agent(BULL,    r3_base + 'FINAL COACHING: ' + arb_c2.get('bull','')       + '\n\nROUND 3 FINAL: Write a FRESH sharpest argument. Changed view?', 350)
    bear_r3  = _call_agent(BEAR,    r3_base + 'FINAL COACHING: ' + arb_c2.get('bear','')       + '\n\nROUND 3 FINAL: Sharpest position. Changed view?', 350)
    swan_r3  = _call_agent(SWAN,    r3_base + 'FINAL COACHING: ' + arb_c2.get('black_swan','') + '\n\nROUND 3 FINAL: Name the ONE thing nobody else is watching.', 350)
    ost_r3   = _call_agent(OSTRICH, r3_base + 'FINAL COACHING: ' + arb_c2.get('ostrich','')    + '\n\nROUND 3 FINAL: Name the institution in denial and cost of inaction.', 350)
    round3 = {'bull': bull_r3, 'bear': bear_r3, 'black_swan': swan_r3, 'ostrich': ost_r3}

    print('  Waiting 90s before arbitrator synthesis (Groq rate limit protection)...')
    time.sleep(90)  # GNI-R-237: 90s for gpt-oss-120b TPM recovery

    # Arbitrator final synthesis
    print('   Arbitrator final synthesis...')
    arb_final_user = (
        news_ctx + '\n\n'
        '=== R1 [summary] ===\nBull: ' + _compress(bull_r1) + '\nBear: ' + _compress(bear_r1) +
        '\nSwan: ' + _compress(swan_r1) + '\nOstrich: ' + _compress(ost_r1) + '\n\n'
        '=== R2 [summary] ===\nBull: ' + _compress(bull_r2) + '\nBear: ' + _compress(bear_r2) +
        '\nSwan: ' + _compress(swan_r2) + '\nOstrich: ' + _compress(ost_r2) + '\n\n'
        '=== R3 [final] ===\nBull: ' + bull_r3 + '\nBear: ' + bear_r3 + '\nSwan: ' + swan_r3 + '\nOstrich: ' + ost_r3 + '\n\n'
        + ('Weakness: ' + weakness + '\n' if weakness else '')
        + ('Dark side: ' + dark_side + '\n' if dark_side and dark_side != 'None' else '')
        + 'Escalation: ' + escalation + ' | Risk: ' + risk_level + '\n\n'
        + 'PILLAR WEIGHTING: ' + pillar_instruction + '\n\n'
        + 'Deliver final synthesis as JSON only.'
    )
    # NN-5: Hard correction channel -- Black Swan + Ostrich enforced at code level
    _hard_constraints = []
    _high_escalation = risk_level.upper() in ('HIGH', 'CRITICAL') or 'CRITICAL' in escalation.upper() or 'HIGH' in escalation.upper()
    if _high_escalation:
        if swan_r3 and not swan_r3.startswith('[Agent error'):
            _hard_constraints.append('BLACK SWAN MANDATORY CONSTRAINT (unknown danger -- cannot be dismissed): ' + _compress(swan_r3, 60))
        if ost_r3 and not ost_r3.startswith('[Agent error'):
            _hard_constraints.append('OSTRICH MANDATORY CONSTRAINT (ignored reality -- cannot be dismissed): ' + _compress(ost_r3, 60))
    if _hard_constraints:
        constraint_block = 'HARD CONSTRAINTS -- YOU MUST ADDRESS THESE IN YOUR VERDICT:\n' + '\n'.join(_hard_constraints) + '\n\n'
        arb_final_user = constraint_block + arb_final_user
        print(f'  NN-5: {len(_hard_constraints)} hard constraint(s) prepended to Arbitrator prompt')

    arb_final_raw = _call_arbitrator(ARB_FINAL, arb_final_user, 600, expect_json=True)  # W-02

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
    r = run_mad_protocol(test, all_articles=[])
    print(f"Verdict:     {r['mad_verdict']}")
    print(f"Blind Spot:  {r['mad_blind_spot'][:80]}")
    print(f"Short Focus: {r['short_focus_threats'][:80]}")
    print(f"Long Shoot:  {r['long_shoot_threats'][:80]}")
    print(f"Action:      {r['mad_action_recommendation'][:80]}")
