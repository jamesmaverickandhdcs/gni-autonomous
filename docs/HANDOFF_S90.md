# HANDOFF S90 -> S91
DATE: 2026-08-31 | HEAD: `da61b13` + the S90 docs commit (verify by ls-remote) | MODEL: Opus 5
Read ONCE. Standing rules: docs/GNI_RULES.md by ID (current through R-S90-4; R-S57-1 and
R-S78-1 each carry a NEW AMENDMENT). **CONTRACT goes to v8** (citation correction only) and
**Protocol to v10** (VERSION LOG swept only). All five files ship SESSION-NUMBERED.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER_S90.md` (generation 10). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: green. Last run `33416590413` (dispatch, 16:53Z) success — it is the ROTATION CERT.
L2 MAD: green. Last debate `33375082629` (08:54Z, carries `ARB-FIT`), unread evidence.
L3 GPVS: untouched, nine sessions. L4 Quota: `not_mad` 2 runs today; worst account 67%.
L5 Public: **10 commits this session; four public pages CERTIFIED in a browser.**
STORAGE: 113/500 MB meter; `public` BASE TABLE count **33** (measured, now published). Backup: NONE.
SCHEDULE: slots `02:13Z`/`10:13Z`. Measure lateness against the SLOT (R-S87-6, 2nd amendment).
PLATFORM: **all 8 workflows on `checkout@v7` + `setup-python@v7`** — cert pending one scheduled
  run of `gni_mad` and `gni_pipeline` (Node-20 warning must be 0; v4 control = 2).
SECRETS: `GROQ_GNI_NOT_MAD` rotated + certified. `GROQ_API_KEY` and `GROQ_MAD_EVENING` NOT.
Target: TRUTHFULNESS OF OUTPUT. ROOT 9 top; ROOT 8 returns when 8.5 is designed.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| 8.6 CERTIFIED | `raw = 26.4` on post-`ee813c0` run `33373867572`; blob agrees; 6/6 predictions | SQL + browser |
| 8.6 control | the two rows beneath still `raw = null` with populated blob | same query |
| 8.4 + 9.7 CERT | score-breakdown panel live; `levels` = 9–10/7–9/5–7/3–5/0–3, ring matches | browser |
| 9.3 CLOSED | `2a6243c` residue sweep; `5b2689c` + `da61b13` figures **with windows** | browser |
| 9.3 correction | `16,144` spanned TWO regimes (flat `6175` to May, metered from Jun) | monthly SQL |
| 6.7 COMPLETE | `e54afdf` — mad + pipeline to v7. **"4 sites each" was 2 per action per file** | grep = 0 non-v7 |
| 9.10 SHIPPED | `59e4023` — `scoreToLevel` DELETED; last frontend ladder gone | build 40/40 |
| 9.10 blocker | DECISION S89-2's blocker was FALSE — `route.ts:40` is the `reports` select | file read |
| 9.9 SHIPPED | `99a9dac` + `59d57ac` — measured interval on `/autonomy` AND `/health` | build 40/40 |
| 9.8 CLOSED | `e3a4e95` — the "8h spacing preserved" comment on an 8h/16h pair | fossil grep 0 |
| 9.6 CLOSED | `8edcf12` — CONTRACT v8 + rules restructured; **8 IDs recovered** | PART 0 |
| 9.6 finding | `GNI-R-076` was a DB rule; CONTRACT cited it with `GNI-R-037`'s text | records |
| 5.6 PARTLY PAID | register: 134 rules, **18 cited**; PART 1 by TRIGGER, PART 2 = 8 CLUSTERS | grep |
| 1.9 + 5.10 | retire clause DISCHARGED; generation 3's disposition READ (`d3a2f20:184`) | git show |
| Rotation | `not_mad` key rotated; `GROQ_API_KEY: ***` + success on `33416590413` | run log |

## 3. ORDER
**MOVED.** See `docs/GNI_TARGET_AND_ORDER_S90.md` — generation 10, dated, superseding.
Do not re-derive a queue from this file. Do not fold items forward without re-ranking.
NEXT SESSION'S MISSION is declared at the top of that file. **The GRAVEYARD now has SEVEN rows:
read it before proposing anything in ROOT 8, ROOT 1, retention, or a published figure.**

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| Do 9.9/9.10 actually render right? | shipped, build green, output identical either way | 8.5 |
| Does v7 silence Node-20 on mad + pipeline? | 6 of 8 proven; these 2 unrun | next scheduled run |
| Does the new `not_mad` key work on a SCHEDULE? | proven on dispatch only | next `02:13Z` |
| What does PROBE-DRIFT actually test? | definition in S57-era records only | recover, don't infer |
| Where is `MYANMAR_DISPATCH_PAT`'s token? | both PAT tabs empty | fine-grained tab / 3rd acct |
| `LR-101` / `GNI-R-122` original text | cited as law, unfound | conversation_search |
| Is `/stocks` price cache refreshed per request? | render path read, fetch path NOT | 2.4 |
| Groq ceiling: 85K/day or the published 100K? | never measured; needs a 429 | 9.11, opportunistic |

## 5. WRONG THIS SESSION (<=6 lines)
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
| "`recommended_interval_hours` isn't in the select, so 9.9's fallback prints `undefined`" | `latest` is `frequency_log[0]`, not `latest_escalation` — I merged two interfaces I had just read | the build passing when it should not have |
| "`16,144/run` is the measured figure" — shipped it, twice | it averages a reservation era and a metered era; no window reproduces it | James asking for the monthly breakdown |
| "`73 tables`" / "`formatInterval` count is 3" / "62 unique item ids" | 33 · 2 · 60 — three banked or hand-counted numbers, all wrong (R-S54-2, R-S81-5) | SQL, the assert, the grep |
| "`GROQ_TEST_ONLY` reaches no workflow — 1.12 family" / "`mad_model_probe.py` may be lost" | it is the 4th probe account, deliberately local-only; the file is tracked at `13aed42` | conversation_search |
| "the `sed` output shows `GROQ_MAD_EVENING` is unwired" | my `sed` truncated the ternary at `gni_mad.yml:57` — R-S88-4, fifth instance today | raw grep |
| **Instruments:** `/c/tmp/k.txt` ritual invented while the real one was in the record · a retracted `git add -p` left inside a fenced block and pasted · SQL and bash shipped in one message (R-S88-1) · a `<ID>` placeholder shipped unmarked (R-S62-2) | | reading my own output, and James |

## 6. TRAPS (<=8 lines) — TEMPORARY ONLY, each with an expiry
- NEW (first carry): **`GROQ_API_KEY` feeds THREE workflows** (`gni_mad` morning, `gni_adaptive`,
  `gni_heartbeat`), not one. Rotating it is not the same operation as `not_mad`'s.
  **Expires when that key is rotated and one scheduled run of each of the three is green.**
- (EXPIRED at this close: S89's "four public-copy commits unseen in a browser" — all four pages
  opened and read this session, and their items closed as CERTIFIED.)
- (PROMOTED at this close: nothing. The two durable lessons became R-S90-1 and R-S90-3 directly.)

## 7. LOAD CHECK — next AI echoes EXACTLY these 5 lines, nothing more
HEAD = the S90 docs commit (verify by ls-remote; `da61b13` was HEAD before it) TREE CLEAN
TARGET = TRUTHFULNESS OF OUTPUT; MISSION = item 8.5 — exercise `_high_escalation == False` once, SIMULATING over stored history first (Protocol 8b); it discharges 8.5, 8.10 and the certs for 9.9 + 9.10
ORDER = `docs/GNI_TARGET_AND_ORDER_S90.md` (highest number = live) is the queue — regenerate, never fold forward, but CARRY THE GRAVEYARD (now 7 rows)
GATE = CONTRACT v8 `LINEAGE:` on every lettered proposal AND every finding (R-S89-1); a cert must DISCRIMINATE (R-S90-1); read the GRAVEYARD before proposing in ROOT 8, ROOT 1, retention, or any published figure
FIRST MOVE = `date -u` + git status + ls-remote; then collect three free certs — 6.7's Node-20 count, the `not_mad` key on a SCHEDULED run, and one SQL on `frequency_log` for a non-CRITICAL row

## 8. POINTERS (<=5 lines)
**Run `python tools/design_bench.py` BEFORE any scorer OPINION** — its banner already states the
funnel-preselection finding; do not re-derive it. `tools/replay_scorer.py` is the simulator 8.5
needs. `escalation_scorer.py` L118-127 (9/7/5/3) · `frequency_controller.py:104` writes
`frequency_log` (NOT `main.py:316`, which does not exist) · `mad_runner.py:275-302` is
`_compute_mad_succeeded` · `monitoring_pipeline.py:37-47` PROTECTION/BLACKOUT · `mad_model_probe.py`
is at repo ROOT, not `tools/`. SQL EDITOR ONLY for `full_analysis` queries, and it needs `::jsonb`.
Never put SQL and bash in one message (R-S88-1).

## DIARY S90 (<=10 lines)
Ten commits, four browser certs, a retire clause discharged four generations late — and the
thing I will carry is none of those. It is that `GNI-R-076`, cited in the contract's own CORE
DISCIPLINE, was minted in March as a rule about ALTER TABLE, and that the text we have all been
obeying under that number belongs to `GNI-R-037`. Thirty-five sessions obeyed the citation and
never the rule, and nothing caught it because both inferred meanings were good advice. That is
the same shape as everything else today: the empty secret that printed `✓ Set`, the page that
renders `30 min` whether the code is right or wrong, the `16,144` I shipped in the morning and
disproved in the afternoon. In each one the confirming signal was real and the thing it
confirmed was not the thing I thought. The rule I earned is R-S90-1 and it is the whole day in
one line: before believing an output, ask what it would look like if I were wrong.
