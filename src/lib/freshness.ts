// Freshness wording for public pages - ARCHITECTURE section 10, SLO-2.
// The four FRESHNESS_ literals below MIRROR the SLO-CFG lines of the live architecture, and
// C7 compares them on every push: move the bound there and the detector stays red until this
// file follows. Never publish a workflow's declared cron as its cadence (section 10.1).
export const FRESHNESS_BOUND_HOURS = 8
export const FRESHNESS_EXCEEDANCE_MAX = 0.10
export const FRESHNESS_WINDOW_FROM = '2026-08-27'
export const FRESHNESS_WINDOW_TO = '2026-09-03'

const inTen = Math.round((1 - FRESHNESS_EXCEEDANCE_MAX) * 10)

// Table cells.
export const FRESHNESS_SHORT =
  `at most ${FRESHNESS_BOUND_HOURS} h old, ${inTen} times in 10 ` +
  `(measured ${FRESHNESS_WINDOW_FROM} to ${FRESHNESS_WINDOW_TO})`
// Prose.
export const FRESHNESS_LINE =
  `GNI's view of the world is at most ${FRESHNESS_BOUND_HOURS} hours old, ${inTen} times in 10 ` +
  `(measured ${FRESHNESS_WINDOW_FROM} to ${FRESHNESS_WINDOW_TO})`
// A workflow with no measured bound: its schedule is a request, not a rate.
export const SCHEDULE_REQUESTED_30 =
  'scheduled every 30 min (a request to GitHub Actions, not a measured rate)'
