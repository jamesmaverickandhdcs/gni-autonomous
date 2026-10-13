// MAD verdict beside report sentiment - order item 9.5, S69 census flag F14 (S109).
// The ONLY place a page may decide whether the report and the debate agree.
//
// WHY. Four pages decided it four ways. /comparison excepted only 'neutral', so a report still
// waiting for its debate ('pending', written at insert by ai_engine/main.py) rendered as a
// DISAGREEMENT about a debate that had not run. The home page called every unequal pair
// DIVERGING, so a neutral debate - 41 of the 60 reports in the 30 days before S109 - read as a
// divergence there while /comparison called it no contradiction. /history and /scenarios drew
// the bear for every verdict that was not bullish. The backend rule is the canon followed here:
// monitoring_pipeline.py treats neutral and pending as no divergence. A failed arbitrator
// stores 'neutral' as a default (mad_runner.py); that is not a ruling and is never compared.
export type VerdictRelation = 'pending' | 'no-ruling' | 'agree' | 'compatible' | 'disagree' | 'unknown'

export function verdictRelation(
  sentiment?: string | null,
  madVerdict?: string | null,
  arbFailed?: boolean | null,
): VerdictRelation {
  const s = (sentiment || '').toLowerCase()
  const m = (madVerdict || '').toLowerCase()
  if (!m || m === 'pending') return 'pending'
  if (arbFailed) return 'no-ruling'
  if (!s || s === 'pending') return 'unknown'
  if (s === m) return 'agree'
  if (s === 'neutral' || m === 'neutral') return 'compatible'
  return 'disagree'
}

export const RELATION_LABEL: Record<VerdictRelation, string> = {
  agree: '\u2713 AGREE',
  compatible: '\u25C6 NO CONTRADICTION',
  pending: '\u23F3 DEBATE PENDING',
  'no-ruling': '\u26A0 NO RULING',
  disagree: '\u26A0 DISAGREE',
  unknown: '\u2014',
}

export const RELATION_NOTE: Record<VerdictRelation, string> = {
  agree: 'Both signals aligned',
  compatible: 'One side neutral: no contradiction',
  pending: 'Debate not yet run for this report',
  'no-ruling': 'Arbitrator failed: verdict is a default',
  disagree: 'Report and debate point opposite ways',
  unknown: 'Report sentiment missing',
}

export function verdictIcon(madVerdict?: string | null, arbFailed?: boolean | null): string {
  const m = (madVerdict || '').toLowerCase()
  if (!m || m === 'pending') return '\u23F3'
  if (arbFailed) return '\u26A0'
  if (m === 'bullish') return '\u{1F402}'
  if (m === 'bearish') return '\u{1F43B}'
  return '\u25C6'
}

// S112: mad_confidence holds 0.5 from the moment a report is inserted (ai_engine/main.py), before
// any debate runs, and a failed arbitrator leaves a default beside its default verdict. Neither is
// a confidence the Arbitrator stated, yet eight pages printed both as one - /comparison showed
// "PENDING ... confidence: 50%" beside "Signal AGREE", read live on 2026-10-12T19:58Z, /debate
// listed the pending report as a debate, and /researcher averaged the placeholders into its
// "Avg MAD Confidence". A page shows the Arbitrator's confidence only through the functions below.
export function statedConfidence(
  madVerdict?: string | null,
  madConfidence?: number | null,
  arbFailed?: boolean | null,
): number | null {
  const m = (madVerdict || '').toLowerCase()
  if (!m || m === 'pending' || arbFailed) return null
  return typeof madConfidence === 'number' && madConfidence > 0 ? madConfidence : null
}

export function confidenceText(
  madVerdict?: string | null,
  madConfidence?: number | null,
  arbFailed?: boolean | null,
): string {
  const m = (madVerdict || '').toLowerCase()
  if (!m || m === 'pending') return 'no debate yet'
  if (arbFailed) return 'no ruling'
  return statedPercent(madVerdict, madConfidence, arbFailed) || 'N/A'
}

export function statedPercent(
  madVerdict?: string | null,
  madConfidence?: number | null,
  arbFailed?: boolean | null,
): string {
  const c = statedConfidence(madVerdict, madConfidence, arbFailed)
  return c === null ? '' : String(Math.round(c * 100)) + '%'
}

// S112 R8: the bands a page colours and words the Arbitrator's confidence by, in one place.
// /comparison states them ("70% or more = strong. Below 50% = weak."); /comparison and
// /scenarios held 0.7 and 0.5 on the page, and /debate coloured its bars by 80 and 60 - a third
// scale no sentence states. A band is given only for a stated confidence (null otherwise), and
// detector check C19 holds every page to these functions.
export const CONFIDENCE_STRONG = 0.7
export const CONFIDENCE_MODERATE = 0.5
export type ConfidenceBand = 'strong' | 'moderate' | 'weak'

export function confidenceBand(c: number | null): ConfidenceBand | null {
  if (c === null) return null
  return c >= CONFIDENCE_STRONG ? 'strong' : c >= CONFIDENCE_MODERATE ? 'moderate' : 'weak'
}
