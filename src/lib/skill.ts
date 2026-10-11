// Directional skill of the GPVS market call - S111 (R60).
// WHY. Read on 2026-10-12 over every verified outcome: 248 of 260 directional calls were Bearish
// while SPY rose in about 60% of the windows, so the calls were right in 42% (3 days) and a
// forecast that always said Bullish would have been right in 61%. A hit rate means skill only
// against the rate a call with no information would reach (WMO JWGFVR: skill is measured
// against a reference forecast). The test is Pesaran & Timmermann (1992), Journal of Business &
// Economic Statistics 10(4):461-465, in the form statsmodels implements
// (statsmodels.stats.diagnostic.pesaran_timmermann): one-sided here, at PT_ALPHA.
// The windows of neighbouring reports overlap, which the test does not model: a PT above the
// critical value is necessary for a claim of skill, not sufficient.
export const PT_ALPHA = 0.05
export const PT_CRITICAL = 1.645 // standard-normal quantile at 1 - PT_ALPHA (checked by a harness)

export interface SkillRow {
  predicted_sentiment?: string | null
  change: number | null | undefined
}

export interface DirectionalSkill {
  n: number
  hitRate: number
  noSkillRate: number
  alwaysBullishRate: number
  alwaysBearishRate: number
  pt: number | null
}

// Bearish/Bullish calls with a measured SPY change; Neutral calls make no direction claim.
// A move is "up" when change > 0, as in statsmodels; a call is "up" when it is Bullish.
export function directionalSkill(rows: SkillRow[]): DirectionalSkill | null {
  const pairs = rows
    .map(r => ({ s: (r.predicted_sentiment || '').toLowerCase(), c: r.change }))
    .filter(r => (r.s === 'bearish' || r.s === 'bullish') && typeof r.c === 'number' && Number.isFinite(r.c))
    .map(r => ({ up: (r.c as number) > 0, callUp: r.s === 'bullish' }))
  const n = pairs.length
  if (n < 2) return null
  const pY = pairs.filter(p => p.up).length / n
  const pZ = pairs.filter(p => p.callUp).length / n
  const pHat = pairs.filter(p => p.up === p.callUp).length / n
  const pInd = pY * pZ + (1 - pY) * (1 - pZ)
  const v = (pInd * (1 - pInd)) / n
  const w = ((2 * pY - 1) ** 2 * pZ * (1 - pZ) + (2 * pZ - 1) ** 2 * pY * (1 - pY)) / n
  const pt = v - w > 0 ? (pHat - pInd) / Math.sqrt(v - w) : null
  return { n, hitRate: pHat, noSkillRate: pInd, alwaysBullishRate: pY, alwaysBearishRate: 1 - pY, pt }
}
