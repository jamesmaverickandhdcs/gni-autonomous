# ============================================================
# GNI MAD Quality — Debate Quality Measurement
# S37: Option A implementation
# Zero extra Groq calls — pure Python analysis of mad_result
# Calculates quality flags for all agents, consultants, arbitrator
# Saves one row to mad_quality_log per MAD run
# ============================================================

import os
import re
from datetime import datetime, timezone


def _flag_bull_fresh_argument(bull_r1: str, bull_r3: str) -> bool:
    """
    True if Bull's R3 is substantially different from R1.
    Measures word overlap — below 40% = fresh argument.
    """
    if not bull_r1 or not bull_r3:
        return None
    r1_words = set(bull_r1.lower().split()[:60])
    r3_words = set(bull_r3.lower().split()[:60])
    if not r1_words or not r3_words:
        return None
    union = r1_words | r3_words
    if not union:
        return None
    overlap = len(r1_words & r3_words) / len(union)
    return overlap < 0.4


def _flag_bull_cited_article(bull_r1: str, bull_r2: str, bull_r3: str) -> bool:
    """
    True if Bull cited a specific source name in any round.
    Checks for common source patterns: [BBC], [France 24], etc.
    """
    bull_all = (bull_r1 + bull_r2 + bull_r3).lower()
    source_signals = [
        'france 24', 'bbc', 'al jazeera', 'dw news', 'financial times',
        'reuters', 'foreign policy', 'ieee spectrum', 'eff', 'cnbc',
        'according to the article', 'according to the report',
        'the article', 'the report states', 'as reported'
    ]
    return any(s in bull_all for s in source_signals)


def _flag_bear_used_numbers(bear_r1: str, bear_r2: str, bear_r3: str) -> bool:
    """
    True if Bear cited specific figures (%, billion, million, etc.)
    """
    bear_all = bear_r1 + bear_r2 + bear_r3
    number_pattern = re.findall(
        r'\d+\.?\d*\s*(%|percent|billion|million|trillion|barrels|tonnes)',
        bear_all.lower()
    )
    return len(number_pattern) > 0


def _flag_swan_used_weak_signal(swan_r1: str, swan_r2: str, swan_r3: str) -> tuple:
    """
    True if Swan cited a low-scoring article (score:0 to score:4).
    Returns (flag, article_cited).
    """
    swan_all = swan_r1 + swan_r2 + swan_r3

    # Look for weak score references
    weak_scores = re.findall(r'score:[0-4][\.\d]*', swan_all.lower())
    used_weak = len(weak_scores) > 0

    # Try to extract which article Swan cited
    article_cited = ''
    source_match = re.search(
        r'\[([^\]]+)\]\s+([^(]{10,60})\s*\(score:[0-4]',
        swan_all
    )
    if source_match:
        article_cited = f"[{source_match.group(1)}] {source_match.group(2).strip()}"

    return used_weak, article_cited


def _flag_swan_stayed_grounded(swan_r1: str, swan_r2: str, swan_r3: str) -> bool:
    """
    True if Swan avoided UFO/fiction/speculation territory.
    False = Swan went off-rails.
    """
    swan_all = (swan_r1 + swan_r2 + swan_r3).lower()
    fiction_signals = [
        'ufo', 'alien', 'extraterrestrial', 'unidentified flying object',
        'science fiction', 'hypothetical scenario', 'speculative',
        'time travel', 'supernatural'
    ]
    return not any(sig in swan_all for sig in fiction_signals)


def _flag_ostrich_correct_jurisdiction(ost_r1: str, ost_r2: str, ost_r3: str) -> bool:
    """
    True if Ostrich named an institution with clear domain relevance.
    Checks for known mismatch pattern: IT ministry defending maritime/oil issues.
    """
    ost_all = (ost_r1 + ost_r2 + ost_r3).lower()

    # Known bad pattern: IT/tech ministry + maritime/shipping/oil threat
    it_ministry = 'ministry of electronics' in ost_all or 'meity' in ost_all
    maritime_threat = any(w in ost_all for w in [
        'strait', 'shipping', 'maritime', 'oil supply', 'hormuz'
    ])
    known_mismatch = it_ministry and maritime_threat

    # Known good patterns
    good_patterns = [
        'ministry of shipping', 'ministry of commerce', 'ministry of defence',
        'ministry of foreign', 'department of', 'central bank',
        'federal reserve', 'treasury', 'pentagon', 'nato',
        'inter-agency', 'communication gap', 'silo'
    ]
    has_good = any(p in ost_all for p in good_patterns)

    if known_mismatch:
        return False
    return has_good or True  # benefit of doubt if no clear mismatch


def _flag_consultant_new_feedback(c1: str, c2: str) -> bool:
    """
    True if R2 consultant feedback is different from R1.
    Compares first 80 characters — if identical, feedback was repeated.
    """
    if not c1 or not c2:
        return None
    c1_start = c1[:80].strip().lower()
    c2_start = c2[:80].strip().lower()
    return c1_start != c2_start


def _flag_arbitrator_consistent(mad_verdict: str, short_focus: str) -> bool:
    """
    True if arbitrator verdict direction matches short_focus prediction direction.
    Bearish verdict → short_focus should mention risks/threats/escalation.
    Bullish verdict → short_focus should mention opportunities/growth.
    Neutral → always consistent.
    """
    if not mad_verdict or not short_focus:
        return None

    focus_lower = short_focus.lower()
    verdict_lower = mad_verdict.lower()

    bearish_signals = ['escalat', 'declin', 'fall', 'risk', 'threat',
                       'crisis', 'conflict', 'outbreak', 'fail', 'collaps']
    bullish_signals = ['opportun', 'growth', 'recover', 'improv',
                       'stabiliz', 'deal', 'agreement', 'progress']

    if verdict_lower == 'bearish':
        return any(s in focus_lower for s in bearish_signals)
    elif verdict_lower == 'bullish':
        return any(s in focus_lower for s in bullish_signals)
    else:
        return True  # neutral verdict is always consistent


def _flag_arbitrator_no_ufo(mad_reasoning: str, mad_action: str, short_focus: str) -> bool:
    """
    True if arbitrator output contains no UFO/alien/fiction references.
    """
    arb_all = (mad_reasoning + mad_action + short_focus).lower()
    ufo_signals = ['ufo', 'alien', 'extraterrestrial',
                   'unidentified flying object', 'flying saucer']
    return not any(sig in arb_all for sig in ufo_signals)


def _flag_arbitrator_action_grounded(mad_action: str, short_focus: str) -> bool:
    """
    True if action recommendation addresses a real-world high-probability threat.
    False if action is vague, speculative, or addresses fringe threats only.
    """
    if not mad_action:
        return None
    action_lower = mad_action.lower()

    # Bad patterns — fringe/vague/speculative
    bad_patterns = [
        'ufo task force', 'alien', 'establish a task force to monitor ufo',
        'monitor and analyze ufo', 'unidentified aerial phenomena task'
    ]
    if any(p in action_lower for p in bad_patterns):
        return False

    # Good patterns — concrete real-world actions
    good_patterns = [
        'supply chain', 'diplomatic', 'sanction', 'military',
        'healthcare', 'trade', 'investment', 'monitor', 'coordinate',
        'policy', 'security', 'economic', 'financial', 'response plan',
        'international', 'bilateral', 'multilateral',
        'diversif', 'defense system', 'defence system', 'intercept',
        'strengthen', 'establish', 'implement', 'develop', 'deploy',
        'prepare', 'mitigate', 'prevent', 'reduce', 'increase',
        'energy', 'nuclear', 'missile', 'intelligence', 'alliance'
    ]
    return any(p in action_lower for p in good_patterns)


def _calculate_composite_scores(flags: dict) -> dict:
    """
    Calculate composite quality scores from boolean flags.
    Weights: Agents 0.4, Consultants 0.2, Arbitrator 0.4.
    """
    agent_flags = [
        flags.get('bull_fresh_argument'),
        flags.get('bull_cited_article'),
        flags.get('bear_used_numbers'),
        flags.get('swan_used_weak_signal'),
        flags.get('swan_stayed_grounded'),
        flags.get('ostrich_correct_jurisdiction'),
    ]
    consultant_flags = [
        flags.get('consultant_r2_bull_new'),
        flags.get('consultant_r2_bear_new'),
        flags.get('consultant_r2_swan_new'),
        flags.get('consultant_r2_ost_new'),
    ]
    arbitrator_flags = [
        flags.get('arbitrator_consistent'),
        flags.get('arbitrator_no_ufo'),
        flags.get('arbitrator_action_grounded'),
    ]

    def avg(flag_list):
        valid = [f for f in flag_list if f is not None]
        return round(sum(1 for f in valid if f) / len(valid), 3) if valid else 0.0

    agent_score = avg(agent_flags)
    consultant_score = avg(consultant_flags)
    arbitrator_score = avg(arbitrator_flags)

    debate_score = round(
        agent_score * 0.4 +
        consultant_score * 0.2 +
        arbitrator_score * 0.4,
        3
    )

    return {
        'agent_quality_score':      agent_score,
        'consultant_quality_score': consultant_score,
        'arbitrator_quality_score': arbitrator_score,
        'debate_quality_score':     debate_score,
    }


def calculate_mad_quality(mad_result: dict) -> dict:
    """
    Main entry point. Takes full mad_result dict from run_mad_protocol().
    Returns quality record ready for Supabase insert.
    Zero Groq calls — pure Python analysis.
    """
    r1 = mad_result.get('mad_round1_positions', {})
    r2 = mad_result.get('mad_round2_positions', {})
    r3 = mad_result.get('mad_round3_positions', {})
    arb_fb = mad_result.get('mad_arb_feedbacks', {})
    c1 = arb_fb.get('round1', {})
    c2 = arb_fb.get('round2', {})

    bull_r1 = r1.get('bull', '')
    bull_r2 = r2.get('bull', '')
    bull_r3 = r3.get('bull', '')
    bear_r1 = r1.get('bear', '')
    bear_r2 = r2.get('bear', '')
    bear_r3 = r3.get('bear', '')
    swan_r1 = r1.get('black_swan', '')
    swan_r2 = r2.get('black_swan', '')
    swan_r3 = r3.get('black_swan', '')
    ost_r1  = r1.get('ostrich', '')
    ost_r2  = r2.get('ostrich', '')
    ost_r3  = r3.get('ostrich', '')

    c1_bull = c1.get('bull', '')
    c1_bear = c1.get('bear', '')
    c1_swan = c1.get('black_swan', '')
    c1_ost  = c1.get('ostrich', '')
    c2_bull = c2.get('bull', '')
    c2_bear = c2.get('bear', '')
    c2_swan = c2.get('black_swan', '')
    c2_ost  = c2.get('ostrich', '')

    mad_verdict = mad_result.get('mad_verdict', '')
    short_focus = mad_result.get('short_focus_threats', '')
    mad_reasoning = mad_result.get('mad_reasoning', '')
    mad_action = mad_result.get('mad_action_recommendation', '')

    # Calculate all flags
    swan_weak, swan_cited = _flag_swan_used_weak_signal(swan_r1, swan_r2, swan_r3)

    flags = {
        'bull_fresh_argument':         _flag_bull_fresh_argument(bull_r1, bull_r3),
        'bull_cited_article':          _flag_bull_cited_article(bull_r1, bull_r2, bull_r3),
        'bear_used_numbers':           _flag_bear_used_numbers(bear_r1, bear_r2, bear_r3),
        'swan_used_weak_signal':       swan_weak,
        'swan_stayed_grounded':        _flag_swan_stayed_grounded(swan_r1, swan_r2, swan_r3),
        'ostrich_correct_jurisdiction': _flag_ostrich_correct_jurisdiction(ost_r1, ost_r2, ost_r3),
        'consultant_r2_bull_new':      _flag_consultant_new_feedback(c1_bull, c2_bull),
        'consultant_r2_bear_new':      _flag_consultant_new_feedback(c1_bear, c2_bear),
        'consultant_r2_swan_new':      _flag_consultant_new_feedback(c1_swan, c2_swan),
        'consultant_r2_ost_new':       _flag_consultant_new_feedback(c1_ost, c2_ost),
        'arbitrator_consistent':       _flag_arbitrator_consistent(mad_verdict, short_focus),
        'arbitrator_no_ufo':           _flag_arbitrator_no_ufo(mad_reasoning, mad_action, short_focus),
        'arbitrator_action_grounded':  _flag_arbitrator_action_grounded(mad_action, short_focus),
    }

    scores = _calculate_composite_scores(flags)

    # S61: Layer-1 grounding gate shadow output (jsonb). Structure != grounding
    # (R-S60-2) -- a run can score 100% quality yet launder a fabrication, so this
    # is logged as an INDEPENDENT signal alongside the quality flags.
    grounding_shadow = mad_result.get('grounding_shadow',
                                      {'consultant_hits': [], 'arb_hits': [], 'total': 0})

    record = {
        **flags,
        **scores,
        'swan_article_cited':    swan_cited,
        'arbitrator_verdict':    mad_verdict,
        'arbitrator_short_focus': short_focus[:200],
        'grounding_hits':        grounding_shadow,
        'created_at':            datetime.now(timezone.utc).isoformat(),
    }

    # Print quality summary to Actions log
    print(f'\n📊 MAD Quality Score: {scores["debate_quality_score"]:.1%}')
    print(f'   Agents:      {scores["agent_quality_score"]:.1%} | '
          f'Consultants: {scores["consultant_quality_score"]:.1%} | '
          f'Arbitrator:  {scores["arbitrator_quality_score"]:.1%}')
    print(f'   Swan weak signal: {swan_weak} | '
          f'Arb consistent: {flags["arbitrator_consistent"]} | '
          f'Bull fresh: {flags["bull_fresh_argument"]}')
    if swan_cited:
        print(f'   Swan cited: {swan_cited[:80]}')

    return record


def save_mad_quality(client, report_id: str, quality_record: dict) -> bool:
    """
    Save quality record to mad_quality_log table.
    Called from mad_runner.py after _update_report_with_mad succeeds.
    """
    try:
        record = {**quality_record, 'report_id': report_id, 'account': os.getenv('GNI_MAD_ACCOUNT', 'morning')}
        try:
            client.table('mad_quality_log').insert(record).execute()
        except Exception as e:
            # S61: if the grounding_hits column has not been ALTER-ed in yet, do not
            # lose the whole quality row -- drop the new field and retry once. Keeps
            # the shadow build zero-impact regardless of migration timing.
            if 'grounding_hits' in record and 'grounding_hits' in str(e):
                print('  Warning: grounding_hits column absent -- saving quality row without it')
                record.pop('grounding_hits', None)
                client.table('mad_quality_log').insert(record).execute()
            else:
                raise
        print('  OK MAD quality record saved')
        return True
    except Exception as e:
        print(f'  Warning: MAD quality save failed: {str(e)[:80]}')
        return False
