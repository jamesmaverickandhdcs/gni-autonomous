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
// Section 6 of the architecture (runtime view) measured what RAN in one dated window. A dated
// measurement stays true of its window after the schedule changes; when section 6 is
// re-harvested, these follow it. Order item 9.22(a), S106: they replace "twice daily", "24/7",
// "Always On" and "may fire 2-3 hours late", none of which any measurement supported.
export const RUNTIME_WINDOW = '2026-08-20 to 2026-09-06'
// gni_pipeline.yml: 36 of 36 scheduled runs delivered; lateness against the slot.
export const PIPELINE_CADENCE = `twice a day (36 of 36 scheduled runs delivered, ${RUNTIME_WINDOW})`
export const PIPELINE_LATENESS =
  `about 4 h after the scheduled time and up to 12 h (median 260 min, p90 616 min, max 727 min, ${RUNTIME_WINDOW})`
// gni_heartbeat.yml 271 of 864 slots, gni_selfcheck.yml 283 of 864.
export const MONITOR_DELIVERY =
  `scheduled every 30 min, and about one slot in three ran (heartbeat 31%, selfcheck 33%, ${RUNTIME_WINDOW})`
export const MONITOR_SHORT = 'every 30 min scheduled; about 1 in 3 ran'

// A workflow with no measured bound: its schedule is a request, not a rate.
export const SCHEDULE_REQUESTED_30 =
  'scheduled every 30 min (a request to GitHub Actions, not a measured rate)'
