# GNI STATUS -- as of S46 close (2026-06-21)

**Branch:** main | **HEAD:** b27474e (verified on origin) | **Model used:** Opus 4.8

## SHIPPED + VERIFIED THIS SESSION (origin/main, ls-remote confirmed)

| Hash | What | State |
|------|------|-------|
| 460ce84 | false-neutral integrity fix (`mad_arb_failed` flag) | LIVE |
| c40a5c2 | header-aware rate governor | LIVE + PRODUCTION-PROVEN |
| bb280a4 | MAD agent/consultant/arbitrator redefinition | LIVE + 1 clean live cron |
| ef3f9bf | adaptive logs 0 Groq tokens (Cerebras-only) | LIVE |
| b27474e | cron drift-fix (:00 -> :13/:43/:58) | LIVE |

(Prior S46 foundation already on main: 77f874e token metering, c5104ec Bull de-bias.)

## CRON SCHEDULE (NEW, post-Commit-5, all UTC)

| Job | Times | Notes |
|-----|-------|-------|
| Intelligence pipeline (+ 3 pillar reports, in-process) | 02:13 / 10:13 | 8h spacing |
| MAD (`gni_mad.yml`) | 02:43 / 10:43 | = pipeline +30, handshake-gated; 10:43 inside 09:00-10:45 protection window |
| Entity graph (`gni_graph.yml`) | 02:58 / 10:58 | = +45, 15min after MAD |
| verify-outcomes (GPVS) | gated on schedule `'13 10 * * *'` | string updated in Commit 5 |
| Self-bias gate | 06:00 | unchanged, no collision |
| Heartbeat | every :00/:30 | dispatches adaptive on escalation >=2.0 |
| Adaptive | workflow_dispatch (event-triggered) | Cerebras-only, 0 Groq |
| Self-check (mission control) | every 30 min | |
| Market | 14:00-20:00 weekdays | non-Groq data |

## QUOTA STATE (the live constraint)

- Ceilings: `TPD_SAFE_CEILING=85000`, `TPD_HARD_LIMIT=100000` (quota_guard.py:19-20).
  **PROJECT-INTERNAL, not confirmed = Groq's real TPD.** 429 probe established TPM=12K only.
- Reset: midnight UTC (per-UTC-calendar-day bucket).
- Pipeline = sacred (always permitted). MAD = NON-sacred (blockable -- caused the 12:22 block).
- Adaptive = Cerebras, logs 0 Groq tokens (Commit 4) -- no longer pollutes the bucket.
- **OPEN:** real MAD ~48-65K/run post-Commit-3; 2xMAD ~96-130K/day at/over the 100K hard cap.
  Stale `PIPELINE_COSTS['gni_mad']=7433` masks this (gate under-counts ~6.5x).

## OPEN THREADS

1. **TWO-ACCOUNT MAD SPLIT** (S47 top priority) -- MAD cron1 -> Groq account A, cron2 ->
   account B. Removes the 2xMAD budget constraint. NOT built. See brief for the 3 checks.
2. **Real MAD tokens/run measurement** -- prerequisite number, get early from `groq_daily_usage`.
3. **Four Treasures applied to GNI** (multi-session) -- start with Treasure-3 assertion sweep;
   first target = the stale 7433 estimate.
4. **WATCH (verification only):** read Commit-3 debate transcript fresh; confirm adaptive logs
   0; confirm new cron drift reduced.

## SIDE-NOISE (low priority)

- Source health 24/47 (403 wave: Stimson, Amnesty, Myanmar Now). Alert-noise; trending down.
- Claude Code "claude.exe in use" auto-update nag -- close extra session.

## HEALTH SNAPSHOT (from last good runs)

- Pipeline: SUCCESS, ~520s, quality ~8.85-8.9/10.
- MAD: production-proven completing real verdicts (governor surviving storms).
- Dashboard: 9/9 staging pages OK.
- Predictions / GPVS: running (verify-outcomes gate string fixed in Commit 5).
