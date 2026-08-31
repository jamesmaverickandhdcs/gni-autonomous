# HANDOFF S89 -> S90
DATE: 2026-08-31 | HEAD: `223da0f` + the `nexus_analyzer` commit + THIS docs commit (verify by
ls-remote) | MODEL: Opus 5
Read ONCE. Standing rules: docs/GNI_RULES.md by ID (current through R-S89-3; R-S87-6 carries a
SECOND AMENDMENT). CONTRACT v7 is UNCHANGED IN CONTENT; **Protocol goes to v9** (VERSION LOG swept only). Both ship SESSION-NUMBERED as
`CONTRACT_S89.md` and `GNI_Session_Transfer_Protocol_S89.md` — CLOSE DELIVERY v6 lists all
five files with `S{N}` and says NO EXCEPTIONS. Ruled by James at this close; S88's
carry-forward of `CONTRACT_S85.md` was the deviation, not the precedent.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER_S89.md` (generation 9). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: green. Last run `33318041130` created 14:52:07Z Aug 30, 6m13. NO run since.
L2 MAD: green. Last debate `33318313852`; watch arm `33319340901` (17 s, no `ARB-FIT`).
L3 GPVS: untouched, eight sessions. L4 Quota: **C1's bill READ at last — see DELTA.**
L5 Public: **four commits landed in the public path this session, ALL UNCERTIFIED in a browser.**
STORAGE: 113/500 MB meter; user tables sum to 87 MB across 73 tables, all GNI's — the four
  `lens_*` tables are DROPPED. Backup: NONE.
SCHEDULE: slots `02:13Z` / `10:13Z`. Lateness Aug 30 = 6h05 and 4h39. Measure against the
  SLOT, never against the previous run (R-S87-6, second amendment).
PLATFORM: 6 of 8 workflows on `checkout@v7` + `setup-python@v7`. `gni_mad` and `gni_pipeline`
  still print the Node 20 warning — 4 call sites each, held for `ee813c0`'s cert.
Target: TRUTHFULNESS OF OUTPUT. ROOT 8 top until 8.6's cert is read; then ROOT 9.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| 6.7 SHIPPED ×6 | `6c37b38` `80003bb` `b8ceb4d` — selfcheck, graph, adaptive, heartbeat, market, selfbias | build 40/40 each |
| 6.7 CERT | Node-20 warning **0 on v7 vs 2 on a v4 control run**; SHAs `3d3c42e5` / `5fda3b95`; CPython 3.11.16 | 3 logs |
| 6.7 app-level | canary APP steps did real work: `Mission Control HEALTHY`; graph wrote 20 nodes/14 edges | run logs |
| 9.7 SHIPPED | `dbc2f92` — FOUR ladders, not three; `comparison:284` was a second 8/6/4/2 with no LOW | diff 2 files |
| 9.7b SHIPPED | `b9c1f03` — the published `levels` table on `/autonomy` aligned to 9–10/7–9/5–7/3–5/0–3 | diff 5 lines |
| 9.3 SHIPPED | `223da0f` — "4 pipelines" wrong in **7** places; now 8 = 4 core + 4 support | diff 4 files |
| 9.3 figure | `~6,175/run` was the `morning` account, frozen 2026-06-24 → `~16,144` measured | `groq_daily_usage` |
| 9.4 SHIPPED | `nexus_analyzer:29` fallback `llama-3.1-8b-instant` (dead Aug 16) → `gpt-oss-20b` | grep, 3 sites now agree |
| 5.9 SHIPPED | `bb6bd2f` — `docs/STATUS.md` deleted | 61 deletions |
| 4.5 CLOSED | 14-day bill stable: mad `morning` 66-72K/21 req · mad `evening` 66-72K/21 · pipeline `not_mad` 31-42K/10-12 | SQL |
| 4.5 blocker | the named source, "the `groq_quota` TELEGRAM line", **does not exist in the repo** | `git grep` empty |
| 6.6 CLOSED | LENS 4 tables / **104 kB** / `n_tup_ins=0` vs GNI 73 / 87 MB. Lens lives on its OWN project | 2 SQL + url hashes |
| 1.14 CLOSED | checkout 14:58:21Z, row written 14:58:20Z, fetch after pip install — start-only inversion | MAD log |
| 1.7 + 1.8 CLOSED | 2nd `truncated=0`; and 0 of 196 rows ever hit the surviving `bool(mad_bull_case)` | log + SQL |
| Storage gap | meter 113 MB − table sum 87 MB = **26 MB (23%) not in any table** | `pg_statio_user_tables` |

## 3. ORDER
**MOVED.** See `docs/GNI_TARGET_AND_ORDER_S89.md` — generation 9, dated, superseding.
Do not re-derive a queue from this file. Do not fold items forward without re-ranking.
NEXT SESSION'S MISSION is declared at the top of that file. **The GRAVEYARD now has SIX rows:
read it before proposing anything in ROOT 8, ROOT 1, or storage retention.**

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| Does `escalation_score_raw` persist? | code shipped twice-over, still no post-commit run | 8.6 cert, 6 predictions |
| Do the four public-copy commits render? | build 40/40, Vercel deploy unseen | browser, 4 pages |
| Where was the gen-1/2 retire roster disposed? | narrowed to generation 3 by `git log -S` | 5.10, one `git show` |
| Is `/stocks` price cache refreshed per request? | render path read, fetch path NOT | 2.4 |
| Is TECH or FIN cap-saturated? | GEO proven; **de-scoped — no consumer until a list edit is proposed** | 8.9 |
| Groq ceiling: 85K/day or the published 100K? | never measured | 9.11 |
| Does 2.1's clause 2 (LABELED coverage) trigger B? | unmeasured | the only thing keeping 2.1 open |
| Do S69 flags F2/F3/F8/F9/F12-F15 still fire live? | unaudited since Jul | 9.5 |

## 5. WRONG THIS SESSION (<=6 lines)
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
| "The `levels` table contradicts the engine — 9.7 is a clean 3-table fix" | it encodes the SCHEDULER's bands, set in March 2026, and `dbc2f92` briefly made the page contradict its own ring highlight | James asking for the history; fixed by `b9c1f03` |
| "`_assert_mad_integrity` is structurally dead, a sibling of 8.5/8.10" / "the surviving `bool(mad_bull_case)` is a leak" | it is a REGRESSION ALARM, deliberately impossible, proven to fire in the S46 dry-run; and the clause was deliberately kept — the scope said "veto regardless", never "delete" | conversation_search after James said to read the record |
| "The protection window leaves a 43-minute unguarded gap before the 02:13 slot" | `BLACKOUT_WINDOWS` (01:30–02:30) sits one line below `PROTECTION_WINDOWS` and closes it exactly | reading ten more lines |
| "`gni_adaptive` has been dead for 68 days" / "heartbeat's standdown is a lateness blind spot" | it runs on the Cerebras path and logs 0 Groq — stated in GNI's own public copy; the standdown is GNI-R-122 working correctly | `about/devops:40`; GNI-R-122 |
| "The funnel pre-selects, so ROOT 8's root is the funnel — filing as NEW item 8.11" | that is the CROSS-ROOT DIAGNOSIS verbatim, at the top of the file I read at session open, and the June-01 record had it five months earlier | James: "S88 မှာလည်း ဒါမျိုး ဖြစ်ဖူးတယ်" |
| Instruments: `\| cat` swallowed the exit status · `grep -i mission_control` matched every line and `tail -8` showed cleanup · `git grep pattern -A 14` read `-A` as a revision · trusted the order's banked line numbers for 1.8 (file AND line had drifted) · a residue grep that searched for the string, not for wrongness | R-S88-4, six instances in one session | reading my own output |

## 6. TRAPS (<=8 lines) — TEMPORARY ONLY, each with an expiry
- NEW (first carry): FOUR commits changed PUBLIC COPY this session and none has been seen in a
  browser. Vercel deploy unverified; curl is a dead end (R-S54-4). **Expires when `/autonomy`,
  `/methodology`, `/research` and `/about/devops` are opened and read.**
(PROMOTED at this close: the `Raw Magnitude --` trap, on its second carry → **R-S89-3**. It could
 not expire because the cert it waits on has not happened, and a third unchanged carry is what
 CONTRACT forbids. The work stays inside 8.6's cert.)

## 7. LOAD CHECK — next AI echoes EXACTLY these 5 lines, nothing more
HEAD = the S89 docs commit (verify by ls-remote; `223da0f` + the nexus commit were HEAD before it) TREE CLEAN
TARGET = TRUTHFULNESS OF OUTPUT; MISSION = certify `ee813c0` by SQL and the four public-copy commits in the BROWSER, then finish 6.7 (mad + pipeline, 4 sites each)
ORDER = `docs/GNI_TARGET_AND_ORDER_S89.md` (highest number = live) is the queue — regenerate, never fold forward, but CARRY THE GRAVEYARD (now 6 rows)
GATE = CONTRACT v7 `LINEAGE:` on every lettered proposal AND on every finding (R-S89-1); Protocol v8 PART C step 5; read the GRAVEYARD before proposing in ROOT 8, ROOT 1, or retention
FIRST MOVE = `date -u` + git status + ls-remote; then `gh run list` for a post-`ee813c0` pipeline run, measured against the SLOT not the previous run, BEFORE any cert query

## 8. POINTERS (<=5 lines)
**Run `python tools/design_bench.py` BEFORE any scorer OPINION.** Its banner already states the
funnel-preselection finding — do not re-derive it as new.
`escalation_scorer.py` thresholds L118-127 (9/7/5/3) · `monitoring_pipeline.py:196` and
`historical_correlations.py:25` hold the same ladder · `monitoring_pipeline.py:37-47` holds
PROTECTION/BLACKOUT windows · `mad_runner.py:275-302` is `_compute_mad_succeeded` (NOT
`mad_protocol.py`) · `adaptive_pipeline.py:41` `ESCALATION_MODES` · `frequency_controller.py:16`
`FREQUENCY_MAP` + the `>= 9.5` branch at L49 · `/autonomy` `scoreToLevel` L42, `levels` L74-80.
SQL EDITOR ONLY for any `full_analysis` query, and it needs `::jsonb`.

## DIARY S89 (<=10 lines)
Seven wrong claims, five of them the same shape: I read the bytes, found two numbers that
disagreed, and called it a contradiction without asking who had made them differ. Every time,
the record held a decision that explained the difference — the scheduler's bands set in March,
a regression alarm built to be impossible, a blackout window one line below the one I read.
The commit that survives from this session's largest fix is the SECOND one, `b9c1f03`, which
exists only because James asked "have you read the history" after the first had already
shipped. The near-miss I want carried is smaller and worse: I read the CROSS-ROOT DIAGNOSIS at
session open and twenty turns later was about to file it as my own discovery, numbered 8.11.
The GRAVEYARD stopped nothing on its own — a person asking a question stopped it. So the rule
I earned is not "read more", it is: when something feels new, that feeling is the signal to
re-open the page, because the file I was handed is where my own last idea already lives.
