// Escalation wording for public pages - order item 9.22(c), definition-of-done line D2.
// The ONLY place a page may turn an escalation score into text: check C11
// ("escalation magnitude") goes red on any page that formats escalation_score itself.
//
// WHY. The score is capped at ESCALATION_CAP. Measured at S106 over every report: 262 of 263
// since 2026-05-24 sit exactly at the cap, and the 67 that store the uncapped magnitude run
// from 10.0 to 26.5 (median 19.6). The capped figure alone therefore carries no information;
// the magnitude certified at S90 (escalation_score_raw) is shown beside it, and a capped
// figure with no magnitude on record says so. ICD 203 tradecraft standards 1 and 2: describe
// the method, express the uncertainty.
export const ESCALATION_CAP = 10

// A single report: "10.0/10 · raw 24.5". Rows written before S90 carry no raw value.
export function formatEscalation(score: number | null | undefined, raw?: number | null): string {
  if (score == null) return 'N/A'
  const capped = `${score.toFixed(1)}/${ESCALATION_CAP}`
  if (raw != null) return `${capped} · raw ${raw.toFixed(1)}`
  return score >= ESCALATION_CAP ? `${capped} · at cap, raw not recorded` : capped
}

// An average of capped scores is bounded by the cap too, and says so.
export function formatCappedAverage(avg: number | null | undefined, digits = 1): string {
  if (avg == null || Number.isNaN(avg)) return 'N/A'
  return `${avg.toFixed(digits)}/${ESCALATION_CAP} (average of capped scores)`
}

// Hover text for any element that shows a score.
export const ESCALATION_NOTE =
  `Escalation is capped at ${ESCALATION_CAP}; "raw" is the uncapped magnitude the pipeline measured.`
