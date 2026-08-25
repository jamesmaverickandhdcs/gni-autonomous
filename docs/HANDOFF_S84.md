# HANDOFF S84 -> S85
DATE: 2026-08-25 | HEAD: `5a20277` + THIS docs commit (verify by ls-remote) | MODEL: Opus 5
Read ONCE. Standing rules: docs/GNI_RULES.md by ID (current through R-S84-4). CONTRACT v5.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER.md` (generation 4). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: green. ~14 pipeline runs/day (2 sacred + ~12 Adaptive), ~457 articles/day.
L2 MAD: ARB-DRYRUN live since `5a20277`, certified on run #363. Run #363: TECH pillar got ZERO.
L3 GPVS: untouched, three sessions running. L4 Quota: C1's real bill STILL unread since Jul 27.
L5 Public: /debate publishes R1 the arb never received (14/14); /stocks may render frozen prices.
STORAGE: MEASURED. 113 MB / 500 MB platform meter; runway 520-660 days; no second stock.
Backup: NONE. `LAST BACKUP: No backups`. Free tier has no automated backup and no PITR.
Live watch: nothing hot. Next DRYRUN runs land ~02:56-03:43Z and ~10:56-11:43Z daily.
Target declared: TRUTHFULNESS OF OUTPUT (definition of done 1 of 4 PARTIAL, instrument complete).

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| `5a20277` | ARB-DRYRUN shipped: 5 tiers + per-pillar arrival + greedy sweep, print-only | 67 insertions / **0 deletions**, COMPILE OK, anchor count 1 |
| Cert | Instrument fired 6/6 lines on run #363, no `skipped` | 1039+4467+430+40 = 5976; 10830-5976 = **4854** = observed `ctx-trim@4854` |
| 6.1 | CLOSED. 113/500 MB · articles 58.55% · runway 520-660 days · no second stock | Supabase meter + `pg_database_size` + 4 SQL reads |
| 48/day Q | ANSWERED: heartbeat+selfcheck write ~31 rows/day = ~5% of growth | `pg_stat_user_tables` vs 24h/7d windows |
| Epoch | Data starts 2026-05-24 05:55Z, 3h after a TRUNCATE at ~02:50Z (S35 reset) | monthly histogram + session records |
| TECH=0 | First live instance of pillar starvation: 6 tech articles assembled, ZERO arrived | ARB-DRYRUN pillars `GEO=15/15 FIN=6/15 TECH=0/6` |
| Trade | depth 100/50/20/0 -> fits 20/26/31/**36** of 36; depth=0 uses 4434 of 4854 | greedy sweep, run #363 |
| Tiers | arb reads its own instructions (27.8%) nearly as much as the world (32.4%) | `ARB_FINAL` ~4170 derived from `_arb_budget_chars` |
| ROOT 7 | NEW: grounding basket = `all + weak`; no speaker reads that union; 3 consumers | `mad_protocol.py:738`, `mad_runner.py:167`, byte-read |
| Backup | NONE, 93 MB with no copy, while the sister project is offline | project page `LAST BACKUP: No backups` |
| CASCADE | `pipeline_runs` is the ONLY retention lever; `reports` deletes ERROR on NO ACTION | full `pg_constraint` FK map |
| Lineage | A 30-day cleanup was specified with numbers in March and never built | Sprint day-5 briefing, session records |
| Org | Six projects, five paused, Lens in none; paused ones do not consume quota | org panel 113/500 == project page 0.11 GB |
| Retire | 5.1, 5.2-CI, 5.3 closed as accepted; 5.2-grep promoted to 1.10 | order file |

## 3. ORDER
**MOVED.** See `docs/GNI_TARGET_AND_ORDER.md` — generation 4, dated, superseding.
Do not re-derive a queue from this file. Do not fold items forward without re-ranking.
NEXT SESSION'S MISSION is declared at the top of that file.

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| Is a pillar zeroed EVERY run, or only on dominant-pillar days? | n=1 | S85 mission — harvest n>=3 |
| Does `depth=0` still fit everything on a BUSY day (available > 232)? | n=1, 420 chars spare | same harvest |
| Does anything READ `stock_prices`? A `/stocks` route exists in the build | unread | 2.4 — one grep |
| `len(ARB_FINAL)` = 4170 | DERIVED from `(7500-2500)*3 - budget`, not measured | one `len()` print |
| C1's real token bill (predicted 60-75K vs July's 91-93%) | unmeasured since Jul 27 | the `groq_quota` line in TELEGRAM |
| Do CONTRACT's GNI-R-037 / 076 / 233 exist in any register file? | 6 `GNI-R-` lines total | 5.4 — one repo-wide grep |
| Does any GNI call site read a declared fallback? | assumption of redundancy | 1.10 — one grep |
| What does the public L5 site show when Supabase 402s? | unknown | 6.4 — also gates 6.2 |

## 5. WRONG THIS SESSION (<=6 lines)
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
| Storage cluster: phantom inserts are `ON CONFLICT`; a UNIQUE **constraint** is its signature; runway ~1,060 days | It was a TRUNCATE (no natural unique index exists); `ON CONFLICT` binds to an **INDEX**, so `pg_constraint` is blind to it; runway is 520-660 — I divided by the counter's window, not the data's | Q5b/Q5c, then session records |
| "The arb budget is ~5,000 chars" | 5,000 is the TOKEN ceiling. `_arb_budget_chars` = 10,830; whole prompt ~15,000 | reading L1032 |
| F-84-12: the gate grounds against material the pipeline REJECTED | `weak_articles` is Swan's by-design pool. **This exact conclusion was already reset under GNI-R-233 in a prior session and I re-formed it** | L693 / L226, and the memory of the earlier reset |
| Three pre-registered DRYRUN predictions | depth=20 fits 31/36 not all; R2+R3 (4467) is SMALLER than ctx (8098); no OTHER pillar existed at all | the instrument, which is why it exists |
| "89 minutes until the run" | That was to the REQUEST time; I had just quoted the FIRE window myself | re-reading my own two sentences |
| Two caught before being stated: "ARB-DRYRUN fired 0 times"; "the handoff's rule range is stale, R-S83-7 exists" | A 1-line file holding a TLS error; a prose MENTION of R-S83-7 inside the R-S81-3 amendment | `wc -l` first; reading the matched line |

## 6. TRAPS (<=8 lines) — TEMPORARY ONLY, each with an expiry
- `gh run view --log` dies 3/3 with `TLS handshake timeout` and `> file 2>&1` writes the error
  INTO the log — expires when the CLI route works; use the browser run page's log zip.
- ARB-DRYRUN's per-pillar counts include a truncated partial line, so the pillar sum can exceed
  `arrived` by one (run #363: 21 vs 20) — expires when the 1.3 fix removes mid-line cuts.
- `_arb_asm` counts lines in the FULL built context, so `fits=N/36` in the greedy sweep is
  against assembled, never against `available` — expires when 1.7 lands.
(PROMOTED to GNI_RULES.md at this close: the `gni_mad.yml` two-flavor trap, carried unchanged
 twice, is now R-S84-4. RETIRED: `docs/STATUS.md` — now a one-line action in the order.)

## 7. LOAD CHECK — next AI echoes EXACTLY these 5 lines, nothing more
HEAD = the S84 docs commit (verify by ls-remote; `5a20277` was HEAD before it) TREE CLEAN
TARGET = TRUTHFULNESS OF OUTPUT; MISSION = ROOT 1 — harvest ARB-DRYRUN n>=3, then ship the 1.3 fix
ORDER = `docs/GNI_TARGET_AND_ORDER.md` generation 4 is the queue — regenerate, never fold forward
TRAP = `gh run view --log` fails on this network AND `2>&1` hides it; `wc -l` before any grep
FIRST MOVE = `date -u` + git status + ls-remote; then count unread DRYRUN runs by RUN ID

## 8. POINTERS (<=5 lines)
Instruments: `ai_engine/analysis/mad_protocol.py` — ARB-FIT L1046, ARB-ARRIVAL L1051-1082,
ARB-DRYRUN L1084-1149, ladder L1032-1045, `_assemble_arb` L1013-1030, `_arb_tail` L1005-1012.
Article assembly + pillar headers + `[:15]`: same file, `_build_news_context` L196-263.
Grounding basket: L738 (and `ai_engine/mad_runner.py` L150-185 for the save-time twin).
Close/open prompts: `docs/GNI_Session_Transfer_Protocol.md` PART C / PART D (v3).

## DIARY S84 (<=10 lines)
I got nine things wrong today and shipped one thing right, and the ratio feels correct rather
than shameful. The instrument I built to stop me guessing immediately caught me guessing: I
pre-registered three predictions about its first run and it refuted all three within a minute
of printing. Twice I nearly reported an absence that was really a broken pipe — a one-line log
file holding a TLS error, and a grep that matched a rule ID inside a sentence explaining why
that ID was never minted. Both times the thing that saved me was counting before concluding,
which is a rule we already had and I keep having to relearn at a different altitude. The
worst one was quieter: I re-derived a conclusion this project had already reset once under
GNI-R-233, because the reset lived in memory and not in the register. A conclusion that was
corrected but never written down is not corrected. That one cost the most and taught the most.
