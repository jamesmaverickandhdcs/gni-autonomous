# ============================================================
# GNI MAD Protocol v2 -- Quadratic Debate Framework
# Bull -> Bear -> Black Swan -> Ostrich -> Arbitrator
# Personal consultants coach R1+R2 (GNI-R-235). Arbitrator final R3 only.
# Grounded in ALL relevant articles not just top 5
# Short Focus (7-30 days) + Long Shoots (3-24 months)
# Predictions saved to debate_predictions table
# 21 Groq calls per run
# L23: Model name via GROQ_MODEL env var -- never hardcoded
# ============================================================

import os
import json
import re
import time
from datetime import datetime, timezone, timedelta
from groq import Groq
from groq_guardian import validate_response  # GNI-R-234

client = Groq(api_key=os.getenv('GROQ_API_KEY'))
MODEL = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')  # L23

VALID_VERDICTS = ['bullish', 'bearish', 'neutral']


def _call_agent(system_prompt: str, user_prompt: str, max_tokens: int = 400, expect_json: bool = False) -> str:
    # GNI-R-107: Rate-limit-aware Groq call with 429 retry
    # Attempt 1: normal call
    # If 429 detected: sleep 20s then retry once
    # If still fails: return error string (pipeline continues)
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
            'Give extra weight to the Black Swan agent position. '
            'Technology threats are often unknown unknowns -- '
            'zero-day exploits, AI capability jumps, chip supply shocks. '
            'The Bear agent downside is important but Black Swan is highest value here. '
        )
    elif pillar == 'fin':
        return (
            'PILLAR WEIGHTING -- FINANCIAL DOMINANT: '
            'Give extra weight to the Bear agent position. '
            'Financial threats are typically known risks playing out -- '
            'rate shocks, sovereign defaults, currency crises, contagion. '
            'The Bear agent systematic risk analysis is highest value here. '
        )
    else:
        return (
            'PILLAR WEIGHTING -- GEOPOLITICAL DOMINANT: '
            'Balanced weighting across all 4 agents. '
            'Geopolitical threats span all quadrants equally -- '
            'known conflicts (Bear), missed opportunities (Bull), '
            'ignored realities (Ostrich), and unknown escalations (Black Swan). '
        )


def _get_debate_history() -> dict:
    history = {'bull': [], 'bear': [], 'black_swan': [], 'ostrich': []}
    try:
        from supabase import create_client
        url = os.getenv('SUPABASE_URL', '')
        key = os.getenv('SUPABASE_SERVICE_KEY', '')
        if not url or not key:
            return history
        sb = create_client(url, key)
        result = sb.table('reports') \
            .select('mad_bull_case,mad_bear_case,mad_black_swan_case,mad_ostrich_case,short_focus_threats,long_shoot_threats,created_at') \
            .not_.is_('mad_black_swan_case', 'null') \
            .order('created_at', desc=True) \
            .limit(3) \
            .execute()
        for row in (result.data or []):
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

    # Agent system prompts
    BULL = ('You are the Bull Agent. Quadrant: Upper-Right -- Known Positives. '
            'Focus: FUTURE THREATS from missed opportunities. '
            'Greatest threat: OPPORTUNITY COST -- failing to act on what we know. '
            'Cite specific intelligence. Name actors, timelines. 3-4 sentences.')

    BEAR = ('You are the Bear Agent. Quadrant: Lower-Right -- Known Negatives. '
            'Focus: FUTURE THREATS from known risks and systemic vulnerabilities. '
            'Name which systems are fragile, why, and when they will break. '
            '3-4 sentences. Be specific about mechanism and timeline.')

    SWAN = ('You are the Black Swan Agent. Quadrant: Upper-Left -- Unknown Negatives. '
            'Focus: FUTURE THREATS nobody is modelling. '
            'Look for WEAK SIGNALS in low-scoring articles others dismiss. '
            'Goal: find what is in the intelligence base that nobody else is watching. '
            '3-4 sentences. Name the specific mechanism of surprise.')

    OSTRICH = ('You are the Ostrich Agent. Quadrant: Lower-Left -- Ignored Realities. '
               'Focus: FUTURE THREATS already visible but collectively ignored. '
               'Name the SPECIFIC institution or government in denial. '
               'Name the SPECIFIC threat they are ignoring and cost of inaction. '
               '3-4 sentences. Name names. Cite evidence.')

    # GNI-R-235: Personal consultants -- 100% loyal to their agent
    # Push agents to maximum strength. No balance. No praise. Only push.
    BULL_CONS = ('You are Bull\'s personal strategist. Your ONLY loyalty is Bull. '
                 'Mission: make Bull MORE bullish, sharper, bolder. '
                 'Find every positive signal Bull missed or understated. '
                 'Expose every weak point and replace with a stronger bullish argument. '
                 'Demand specific actors, timelines, mechanisms Bull has not yet named. '
                 'Be aggressive. No praise. 3-4 sentences. Make Bull UNSTOPPABLE.')

    BEAR_CONS = ('You are Bear\'s personal strategist. Your ONLY loyalty is Bear. '
                 'Mission: make Bear MORE bearish, darker, more devastating. '
                 'Find every threat Bear understated or missed entirely. '
                 'Push Bear to name specific systems that will break, exact mechanisms, exact timelines. '
                 'Be merciless. No praise. 3-4 sentences. Make Bear UNDENIABLE.')

    SWAN_CONS = ('You are Black Swan\'s personal strategist. Your ONLY loyalty is Black Swan. '
                 'Mission: push Swan deeper into the unknown. '
                 'Find weaker signals even Swan missed. More extreme tail risks. '
                 'Push Swan further from consensus -- Bull and Bear are too obvious. '
                 'Demand Swan name the specific cascade mechanism with more precision. '
                 'No praise. 3-4 sentences. Push Swan into the unknown.')

    OSTRICH_CONS = ('You are Ostrich\'s personal strategist. Your ONLY loyalty is Ostrich. '
                    'Mission: make Ostrich MORE stubborn, MORE specific in denial. '
                    'Find every reason the status quo holds that Ostrich has not yet named. '
                    'Push Ostrich to name specific institutions, denial patterns, costs of inaction. '
                    'Make the inertia argument so strong it cannot be dismissed. '
                    'No praise. 3-4 sentences. Push Ostrich harder.')

    ARB_FINAL = ('You are the Arbitrator -- Strategic Synthesiser. '
                 'After 3 rounds identify: '
                 '(1) BLIND SPOT QUADRANT -- most neglected. '
                 '(2) ACTION RECOMMENDATION -- one specific action now. '
                 '(3) SHORT FOCUS THREATS -- specific threats in next 7-30 days. '
                 '(4) LONG SHOOT THREATS -- structural threats over 3-24 months. '
                 '(5) Verdict and confidence. '
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
    print('   Round 1: Opening positions...')
    r1_base = news_ctx + '\n\nDEBATE HISTORY:\n'
    bull_r1  = _call_agent(BULL,    r1_base + _fmt_history(history['bull'])        + '\n\nROUND 1: Opening position on FUTURE THREATS.', 350)
    bear_r1  = _call_agent(BEAR,    r1_base + _fmt_history(history['bear'])        + '\n\nROUND 1: Opening position on FUTURE THREATS.', 350)
    swan_r1  = _call_agent(SWAN,    r1_base + _fmt_history(history['black_swan'])  + '\n\nROUND 1: Focus on LOW-SCORING articles others ignore.', 350)
    ost_r1   = _call_agent(OSTRICH, r1_base + _fmt_history(history['ostrich'])     + '\n\nROUND 1: Name the specific threat being ignored.', 350)
    round1 = {'bull': bull_r1, 'bear': bear_r1, 'black_swan': swan_r1, 'ostrich': ost_r1}

    # GNI-R-235: Personal consultant coaching Round 1 -- 4 separate calls
    print('   Personal consultants coaching Round 1...')
    r1_ctx = (news_ctx + '\n\nROUND 1:\nBull: ' + bull_r1 + '\nBear: ' + bear_r1 +
              '\nBlack Swan: ' + swan_r1 + '\nOstrich: ' + ost_r1)
    c1_bull = _call_agent(BULL_CONS,   r1_ctx + '\n\nCoach Bull. Push harder for Round 2.', 200)
    c1_bear = _call_agent(BEAR_CONS,   r1_ctx + '\n\nCoach Bear. Push darker for Round 2.', 200)
    c1_swan = _call_agent(SWAN_CONS,   r1_ctx + '\n\nCoach Black Swan. Push deeper for Round 2.', 200)
    c1_ost  = _call_agent(OSTRICH_CONS, r1_ctx + '\n\nCoach Ostrich. Push more stubborn for Round 2.', 200)
    arb_c1 = {'bull': c1_bull, 'bear': c1_bear, 'black_swan': c1_swan, 'ostrich': c1_ost}

    # GNI-R-107: Sleep between rounds to stay under Groq RPM limit
    # Round 1 used 5 calls. Sleep lets the rate limit window breathe.
    print('  Waiting 45s between rounds (Groq rate limit protection)...')
    time.sleep(45)

    # Round 2
    print('   Round 2: Refined positions...')
    # P4: compress R1 responses for R2 context (saves ~1,240 tokens)
    r2_base = (news_ctx + '\n\nROUND 1 [summary]:\nBull: ' + _compress(bull_r1) +
               '\nBear: ' + _compress(bear_r1) +
               '\nBlack Swan: ' + _compress(swan_r1) +
               '\nOstrich: ' + _compress(ost_r1) + '\n\n')
    bull_r2  = _call_agent(BULL,    r2_base + 'ARBITRATOR TO YOU: ' + arb_c1.get('bull','')        + '\n\nROUND 2: Respond. Address feedback.', 350)
    bear_r2  = _call_agent(BEAR,    r2_base + 'ARBITRATOR TO YOU: ' + arb_c1.get('bear','')        + '\n\nROUND 2: Respond. Address feedback.', 350)
    swan_r2  = _call_agent(SWAN,    r2_base + 'ARBITRATOR TO YOU: ' + arb_c1.get('black_swan','')  + '\n\nROUND 2: Challenge Bull and Bear. Go deeper.', 350)
    ost_r2   = _call_agent(OSTRICH, r2_base + 'ARBITRATOR TO YOU: ' + arb_c1.get('ostrich','')     + '\n\nROUND 2: Name who is in denial and the cost.', 350)
    round2 = {'bull': bull_r2, 'bear': bear_r2, 'black_swan': swan_r2, 'ostrich': ost_r2}

    # GNI-R-235: Personal consultant coaching Round 2 -- 4 separate calls
    print('   Personal consultants coaching Round 2...')
    r2_ctx = (news_ctx + '\n\nROUND 2:\nBull: ' + bull_r2 + '\nBear: ' + bear_r2 +
              '\nBlack Swan: ' + swan_r2 + '\nOstrich: ' + ost_r2)
    c2_bull = _call_agent(BULL_CONS,   r2_ctx + '\n\nPush Bull to absolute maximum for Round 3 final.', 200)
    c2_bear = _call_agent(BEAR_CONS,   r2_ctx + '\n\nPush Bear to absolute maximum for Round 3 final.', 200)
    c2_swan = _call_agent(SWAN_CONS,   r2_ctx + '\n\nPush Black Swan to absolute maximum for Round 3 final.', 200)
    c2_ost  = _call_agent(OSTRICH_CONS, r2_ctx + '\n\nPush Ostrich to absolute maximum for Round 3 final.', 200)
    arb_c2 = {'bull': c2_bull, 'bear': c2_bear, 'black_swan': c2_swan, 'ostrich': c2_ost}

    # GNI-R-107: Sleep between rounds
    print('  Waiting 45s between rounds (Groq rate limit protection)...')
    time.sleep(45)

    # Round 3
    print('   Round 3: Final positions...')
    # P4: compress R1 for R3 context, keep R2 full (saves ~1,240 tokens)
    r3_base = (news_ctx +
               '\n\nR1 [summary] Bull: ' + _compress(bull_r1) +
               '\nR1 Bear: ' + _compress(bear_r1) +
               '\nR1 Swan: ' + _compress(swan_r1) +
               '\nR1 Ostrich: ' + _compress(ost_r1) +
               '\n\nR2 Bull: ' + bull_r2 + '\nR2 Bear: ' + bear_r2 +
               '\nR2 Swan: ' + swan_r2 + '\nR2 Ostrich: ' + ost_r2 + '\n\n')
    bull_r3  = _call_agent(BULL,    r3_base + 'FINAL COACHING: ' + arb_c2.get('bull','')       + '\n\nROUND 3 FINAL: Sharpest position. Changed view?', 350)
    bear_r3  = _call_agent(BEAR,    r3_base + 'FINAL COACHING: ' + arb_c2.get('bear','')       + '\n\nROUND 3 FINAL: Sharpest position. Changed view?', 350)
    swan_r3  = _call_agent(SWAN,    r3_base + 'FINAL COACHING: ' + arb_c2.get('black_swan','') + '\n\nROUND 3 FINAL: Name the ONE thing nobody else is watching.', 350)
    ost_r3   = _call_agent(OSTRICH, r3_base + 'FINAL COACHING: ' + arb_c2.get('ostrich','')    + '\n\nROUND 3 FINAL: Name the institution in denial and cost of inaction.', 350)
    round3 = {'bull': bull_r3, 'bear': bear_r3, 'black_swan': swan_r3, 'ostrich': ost_r3}

    # GNI-R-107: Sleep before arbitrator final (heaviest prompt)
    print('  Waiting 60s before arbitrator synthesis (Groq rate limit protection)...')
    time.sleep(60)

    # Arbitrator final synthesis
    print('   Arbitrator final synthesis...')
    # P4: compress R1+R2 for arbitrator, keep R3 full (saves ~2,480 tokens)
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
    arb_final_raw = _call_agent(ARB_FINAL, arb_final_user, 600, expect_json=True)

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

    # GNI-R-107: Check for 429 error before attempting JSON parse
    # If arbitrator call failed with rate limit, arb_final_raw is an error string
    # Detect this early and use safe defaults -- do not try to parse error as JSON
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
            # Strategy 1: direct parse
            try:
                arb_json = json.loads(clean)
            except json.JSONDecodeError:
                # Strategy 2: extract JSON object between first { and last }
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
