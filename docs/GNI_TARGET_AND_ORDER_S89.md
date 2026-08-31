# GNI TARGET + WORKING ORDER
**SESSION-NUMBERED BY DESIGN (Protocol v4+).** This file ships and lands as
`docs/GNI_TARGET_AND_ORDER_S89.md`. **THE LIVE ORDER IS THE HIGHEST SESSION NUMBER.**

GENERATION 9 · 2026-08-31 · supersedes `GNI_TARGET_AND_ORDER_S88.md` (generation 8).
Regenerated, never appended. HEAD at close: the S89 docs commit (`223da0f` + the
`nexus_analyzer` commit were HEAD before it — verify by `ls-remote`).

---

## NEXT SESSION'S MISSION (S90)

**CERTIFY WHAT S88 AND S89 SHIPPED — `ee813c0` (8.6) BY SQL, AND THE FOUR PUBLIC-COPY
COMMITS IN THE BROWSER. THEN FINISH 6.7 (the last two workflows).**

| item | what "done" looks like |
|------|------------------------|
| 8.6 cert | one post-`ee813c0` `reports` row has `escalation_score_raw` NOT NULL, equal to the blob's nested `raw_score`, while `escalation_score` stays 10.0 — and `/autonomy` renders three live cells in the browser |
| 9.7 cert | `/autonomy` shows the level from 9/7/5/3 AND the `levels` table reading 9–10 / 7–9 / 5–7 / 3–5 / 0–3, with the ring on the same row |
| 9.3 cert | `/methodology`, `/research`, `/about`, `/about/devops` all read "8 workflows — 4 core + 4 support" and the token figure reads 16,144 |
| 6.7 finish | `gni_mad.yml` and `gni_pipeline.yml` pinned to `checkout@v7` + `setup-python@v7` — FOUR call sites each, `count==1` will abort |

**PRE-REGISTERED CERT PREDICTIONS (unchanged from generation 8; written before the run
exists, R-S85-6 / step 8c):**
1. `escalation_score_raw` is NOT NULL on the first post-`ee813c0` row
2. its value is **> 10.0**
3. `escalation_score` on the same row is **exactly 10.0**
4. `escalation_score_raw` == `(full_analysis::jsonb)->'score_breakdown'->>'raw_score'`
5. `escalation_score_lower` and `escalation_score_upper` stay **NULL** (5.7 untouched)
6. `/autonomy` shows `Final Score 10.0` · `Raw Magnitude 1x–2x.x` · `Upper Bound --`

**FAILURE TEST:** if the insert throws, the column name or type is wrong and the pipeline is
DOWN — check `gh run list --workflow=gni_pipeline.yml` conclusion FIRST, before reading any row.

**CERT QUERY (SQL EDITOR ONLY — never paste into bash, R-S88-1):**
```sql
select created_at, escalation_score, escalation_score_raw,
       escalation_score_lower, escalation_score_upper,
       (full_analysis::jsonb)->'score_breakdown'->>'raw_score' as raw_in_blob
from reports order by created_at desc limit 3;
```

**HOW TO KNOW A POST-COMMIT RUN EXISTS (measure against the SLOT, not the last run —
R-S87-6 as amended at this close):**
```bash
date -u
gh run list --workflow=gni_pipeline.yml --limit 4 \
  --json databaseId,conclusion,status,event,createdAt,updatedAt
grep -n 'cron' .github/workflows/gni_pipeline.yml
```
Slots are `02:13Z` and `10:13Z`. Lateness is `actual − slot`, and the measured band is
4h39–6h05. The gap between two consecutive runs is 8h or 16h BY DESIGN and says nothing
about lateness — S89 mistook 13h of gap for 13h of lateness when the real figure was 3h07.

---

## TARGET (unchanged — no phase transition this close)

**TRUTHFULNESS OF OUTPUT.** What GNI says must be what GNI measured.

**DEFINITION OF DONE — status at this regeneration:**
- the arbitrator reads what it claims to read — ROOT 1 CERTIFIED for CONTENT; **1.14 CLOSED
  at this close: the inversion is at job START only, not at the DB read**
- the grounding gate measures reading, not existence — ROOT 7 OPEN, untouched for eight sessions
- the escalation score carries information — **ROOT 8: three-quarters answered, unchanged from
  generation 8.** Certification is still the open quarter, and it is now the ONLY thing holding
  ROOT 8 in the top slot.
- the public surface matches the configuration — **ROOT 9: the biggest single move this project
  has made on this clause.** Four commits landed in the public path (`dbc2f92`, `b9c1f03`,
  `223da0f`, and the workflow-count sweep inside it). All UNCERTIFIED in a browser.

---

## 🪦 GRAVEYARD — RULED-OUT DIRECTIONS (DECISION S88-2)

**COPY THIS SECTION INTO EVERY REGENERATION, VERBATIM. Never rewrite it from memory, never
drop it.** Protocol v8 PART C step 5 carries the same instruction, so the template cannot
delete it either. It exists because a design falsified in three seconds at S87 was first
proposed on 2026-06-01 and survived five sessions inside prose that nobody re-read.

| direction | killed by | evidence |
|---|---|---|
| **RECALIBRATE THE ESCALATION LEVEL** (Jun-01 option B; Mar-24 "Fix 2"; actor-tier; rupture-tier) | DECISION S87-2 | replayed n=192: Fix-2 gives 192/192 CRITICAL identical to production, actor-tier changes 0 runs, rupture-tier still 187/192. `tools/design_bench.py` re-proves this on EVERY run. |
| **FIX POLARITY BY EDITING A WORD LIST** (drop `ceasefire` from `GEO_SIGNALS`) | DECISION S88-3, S88 measurement | replayed n=196: **0 runs changed**, raw range/median identical. GEO hits min 8 / median 14 / max 19 against cap 5 — the pillar is cap-saturated, so ~half the 27-word list is arithmetically inert. R-S88-5. |
| **ROUND-ROBIN / PER-PILLAR ALLOTMENTS for the arbitrator budget** | DECISION S83-1, DECISION S85-1 | arrival is a CONSTANT not a share; coverage falls 14.4%→8.4% as volume rises, and the share is already stable at 62–65% of built. Ordering cannot raise coverage. The lever is per-article COST — shipped as `depth=0` (`228634c`). |
| **PER-SPEAKER GROUNDING BASKETS** (7.2 option C) | 2.1's standing law | fail-open is law; per-speaker baskets make the gate STRICTER and gates starve. |
| **RAISE THE ARB max_tokens FLOOR** to cure 413s | S80/S81 | the floor guarded the ANSWER side only; the prompt side exceeded the 8K per-request ceiling. Fixed by clamping context, not by raising the floor. |
| **DELETE `stage4_selected=False` ROWS TO RECLAIM STORAGE** (S89 proposal, killed the same session) | DECISION S89-4 | those rows ARE the XAI audit trail the March-2026 design built them to be — "every rejected article is visible with reason", the basis of the published "glass box / more transparent than industry systems" claim. Eight consumers in `src/`, including `/transparency`, `/history` and two API routes. Measured runway is ~550 days at 0.7 MB/day, so there is no capacity reason either. |

**Reading this table is not optional before proposing anything in ROOT 8 or ROOT 1.**
A proposal that lands in this table without new measurement is a LINEAGE-BEV failure.

---

## THE CROSS-ROOT DIAGNOSIS (carried from generation 7 — now with five instances)

> **GNI repeatedly measures what it has already guaranteed itself, and publishes the result as
> a fact about the world.**

| instance | what is measured | what it actually is |
|---|---|---|
| ROOT 7 | "the span exists in the pool" | reported as "the agent read it" |
| 8.1b | `_high_escalation` True 6/6 | a crisis channel that cannot leave crisis mode |
| 8.1 | `diversity_bonus` = 3.0 in 175/191 | the S39 funnel quota (14/4/4) guarantees all three pillars |
| 8.9 | GEO pillar "active" 196/196 | GEO hits are 8–19 against a cap of 5 — the pillar cannot be inactive |
| 8.10 | PHI-003 gate "protecting" the score | it has never fired in 196 runs; `combo_bonus < 3` mutes it exactly when combos fire |

Its use is predictive — when a metric is >90% constant, ask WHO GUARANTEED IT before tuning it.

**S89 NOTE — no sixth instance was added, and that is the finding.** S89 re-derived this
diagnosis from `design_bench`'s own banner ("an ABSOLUTE threshold on a PRE-SELECTED set")
and was about to file it as a NEW item 8.11, twenty turns after reading this very table at
session open. The June-01 record had reached the same conclusion five months earlier. The
diagnosis does not need a sixth row; the reader needs to re-open this page whenever something
feels new. See R-S89-1.

---

## THE ORDER

### ROOT 8 — GNI PUBLISHES A SATURATED INSTRUMENT AS A MEASUREMENT OF THE WORLD · URGENT · **TOP**
*Holds the top slot ONLY until 8.6's cert is read. After that it drops behind ROOT 9.*

- **8.1** CLOSED (S86) — the audit. Saturation across three layers, confirmed by bytes.
- **8.1a** OPEN — D-11's feeds list misses three consumers: arb prompt L989, `nexus_analyzer:567`,
  `self_bias_gate:46`. Unchanged this close.
- **8.1b** OPEN — NN-5 is a deliberate hard-correction channel (`1da3dfe`) whose switch is stuck.
  Since no recalibration is coming, the switch stays stuck by design decision, not by neglect.
  **S89 sibling, measured:** `gni_adaptive` has logged **0 Groq tokens since 2026-06-23** in
  `groq_daily_usage` — 68 days. Not dead: runs exist (dispatched by `github-actions [Bot]`,
  i.e. the heartbeat), and `about/devops:40` states the reason in its own copy — the CRITICAL
  path is Cerebras and logs 0 Groq. A crisis channel pinned to crisis mode bills nothing,
  which is why nobody noticed. RE-CONFIRMED, not new.
- **8.1c** OPEN and GROWING — `constraint=1092` of `ctx_room=4762` on `33180919784`
  (was 987/5091 at S86): ~19% → ~23% of arbitrator context spent by an always-on branch.
- **8.2** CLOSED (S87) — CERTIFIED 4/4. `4b220ab` merges five unpublished scorer fields.
- **8.3** RULED (S87) — NO RECALIBRATION OF THE LEVEL. See GRAVEYARD row 1.
- **8.4** SHIPPED (S88) `737ef06`. Cert is visual, in the browser, with 8.6's. Unchanged.
- **8.5** OPEN, **RANK RAISED AGAIN.** Exercise `_high_escalation == False` once, deliberately.
  S87 removed the only natural trigger; the selftest fixture hardcodes CRITICAL. Pairs with 8.10.
- **8.6** **SHIPPED (S88) `ee813c0`, CERT STILL PENDING — second session waiting.**
  `BLOCKER: none. The cert needs one scheduled pipeline run after 2026-08-30 19:22:15Z,
  nothing else.` S89 confirmed by `gh run list` that no such run had landed by 05:20Z.
- **8.7** RE-SPECIFIED (S88). Score half CLOSED; the direction-neutral audit of published
  EVIDENCE STRINGS (`factors`, `signals_found`) is what remains. Unchanged.
- **8.8** OPEN — 19 keywords never fire in 192 runs: GEO 1 (`invasion`), TECH 3, **FIN 15**.
  **DO NOT DELETE THEM** — their silence is the finding. Absence is evidence (Protocol step 8h).
- **8.9** OPEN — GEO is CAP-SATURATED 196/196. **S89 DE-SCOPED THE FOLLOW-ON:** generation 8
  said "TECH and FIN headroom is UNMEASURED — measure both before 8.8". S89 started that
  measurement and stopped, because R-S88-5 states what a headroom figure is FOR — deciding
  whether a LIST EDIT is inert. With list edits in the GRAVEYARD, the measurement has no
  consumer. Measure it when, and only when, a list edit is actually proposed.
- **8.10** OPEN — PHI-003 has never fired in 196 runs. Pairs with 8.5. Also:
  `final_score = max(final_score, 1.0)` is an undocumented floor that min-raw 5.6 can never reach.

### ROOT 9 — PUBLIC COPY DRIFTS FROM CONFIGURATION · URGENT
*Four commits landed here this session. Every one of them is UNCERTIFIED until a browser
confirms it — curl is a dead end (R-S54-4).*

- **9.7** **SHIPPED (S89) `dbc2f92` + `b9c1f03`, CERT PENDING.** The item as written was wrong:
  there were FOUR ladders, not three. `escalation_scorer.py:118-127` = 9/7/5/3 (canonical) ·
  `autonomy/page.tsx:41` = 8/6/4/2 · **`comparison/page.tsx:284` = a second inline 8/6/4/2
  with NO `LOW` branch** · `design_bench.py:39` (fixed at S88). Backend agreement was verified
  before shipping: `monitoring_pipeline.py:196` and `historical_correlations.py:25` both hold
  9/7/5/3, so the frontend was the lone outlier. `b9c1f03` then aligned the PUBLISHED `levels`
  table on the same page (`9–10 / 7–9 / 5–7 / 3–5 / 0–3`), which `dbc2f92` alone would have
  left contradicting its own ring highlight.
- **9.8** **SHIPPED in `dbc2f92`.** The false `FT-11` comment is deleted; the grep for other
  `FT-` comments returned exactly one hit, so the census-artifact family is closed.
  **S89 sibling found, NOT separately numbered:** `gni_pipeline.yml:5` comments
  *"8h spacing preserved"* on a `02:13`/`10:13` pair that is 8h then 16h. Same family, code-only,
  no public surface. Fix it the next time that file is opened.
- **9.3** **SHIPPED (S89) inside `223da0f`, CERT PENDING.** "4 pipelines" was wrong in SEVEN
  places, not six. Corrected as **8 workflows = 4 core + 4 support**, with the array left at
  four and retitled "The 4 Core Autonomous Pipelines". The same commit replaced
  `~6,175/run (reservation estimate)` — the `morning` account's figure, frozen since 2026-06-24 —
  with `~16,144/run (measured avg, 129 runs)` from `groq_daily_usage`, beside a `madTokens`
  value that is live. A stale constant standing next to a live one is unreadable as either.
- **9.4** **SHIPPED (S89).** `nexus_analyzer.py:29` defaulted `GROQ_MODEL_FALLBACK` to
  `llama-3.1-8b-instant`, dead since Aug 16, while `llm_health_probe` and `intelligence_funnel`
  both default to `openai/gpt-oss-20b`. `main.py:14` imports this module, so it is the sacred
  path, not dead code — and 1.12 proves no workflow supplies the env var, so the default is
  what CI uses. **`stock-context/route.ts:81` still defaults to `llama-3.3-70b-versatile` and
  was NOT touched — that model is alive; verify before assuming it is the same defect.**
- **9.5** OPEN — eight unresolved S69 census flags; F14 (`/comparison` renders BEARISH over a
  NEUTRAL verdict) is the ugly one. RE-CERT never ran. Unaudited since July.
- **9.6** **MEASURED (S89), and the finding is worse than "three ID schemes".** `GNI-R-233`
  appears in `GNI_RULES_S84..S88` (2 hits each). **`GNI-R-037` and `GNI-R-076` appear in NO
  `GNI_RULES` file at all** — only in CONTRACT, order/handoff files, and S44/S45/S61/S62/S73
  work-order and spec docs. CONTRACT v7's GATE SEQUENCE opens with `BIRD-EYE (GNI-R-037)` and
  CORE DISCIPLINE cites `GNI-R-076`; both were followed all session from inferred meaning.
  **Law cited by the contract must be findable in the register.** Pairs with 5.6.
- **9.9** **NEW.** `/autonomy:134` reads `{intervalMap[latestLevel] || latest.recommended_interval_hours}`.
  `intervalMap` holds all five levels, so the right-hand side is unreachable: the MEASURED
  interval stored in `frequency_log` by `main.py:316` has never once been displayed. The
  hardcoded map is also wrong for part of the range — `frequency_controller.py:49` drops
  CRITICAL to 0.5h only at score ≥ 9.5, so a 9.0–9.4 run stores 1.0h while the page says
  "30 min". Invisible today because 196/196 sit at 10.0. Fix is to invert the `||`.
- **9.10** **NEW, DEFERRED BY DECISION S89-2.** `/comparison` already prefers the DB's
  `escalation_level` and falls back to a ladder; `/autonomy` re-derives from score only.
  Making `/autonomy` match would delete the last frontend ladder entirely — but it requires
  adding `escalation_level` to the select in `/api/health/route.ts:40`, which is one of
  `ee813c0`'s own files. Do it AFTER the cert.
- **9.11** **NEW.** `research/page.tsx:105` publishes `Groq 100K tokens/day`. The May record
  says the ceiling was 85,000/day. Not measured this session; do not edit either number until
  the real ceiling is read. Related to ROOT 4.
- **9.1 / 9.2** CLOSED in earlier sessions.

### ROOT 1 — THE ARBITRATOR'S INTAKE · CERTIFIED FOR CONTENT AND FOR ORDERING
- **1.14** **CLOSED (S89) — THE BLOCKER WAS DISPROVEN, NOT INHERITED.** Generation 8 carried
  `BLOCKER: ASSERTED, UNTESTED`. One log read settled it: on MAD `33318313852`, checkout
  finished at `14:58:21.03Z` and the pipeline row was written at `14:58:20Z`; the article fetch
  ("Fetched 148 scored articles + 50 weak signals") happens after checkout AND after pip
  install, so the debate read a row that already existed. **The inversion is at job START only.
  Not a silent live failure; does not outrank anything.** Residue kept as **1.14b**: the log
  never prints WHICH report id it updated, so "read the fresh one" is inference, not proof.
  Caution on the timestamps: every application line carries the step's flush time, not its own.
- **1.14b** **NEW (residue of 1.14).** Make `mad_runner` print the report id it fetched and the
  id it updated. One print; converts the strongest remaining inference into a byte.
- **1.7** **CLOSED (S89) AS DISCHARGED.** Second `truncated=0` sighting, on `33318313852`:
  `available=148 assembled=31 arrived=31 truncated=0 dropped=0`. The item and its evidence
  no longer disagree.
- **1.8** **CLOSED (S89).** The item pointed at `mad_protocol.py:275-295`; the code is at
  `mad_runner.py:275-302` — **file and line both drifted, and S85 had already recorded that.**
  Bytes: `_compute_mad_succeeded` vetoes on `mad_arb_failed` FIRST, so the June leak is shut.
  The surviving `bool(mad_bull_case)` term is the ORIGINAL design, deliberately kept — the
  scope text said "False whenever `mad_arb_failed` is True, REGARDLESS of agent success", never
  "delete the clause". SQL settles the residue: of 196 rows, 14 had `mad_arb_failed` (the veto
  is doing real work, 7.1%) and **0** matched `not arb_failed AND neutral AND confidence = 0.5`.
  The clause has never once fired. `_assert_mad_integrity` is a REGRESSION ALARM, not a dead
  branch — it is structurally impossible by design and was proven to fire in the S46 dry-run
  harness when forced. Do not file it as a sibling of 8.5/8.10.
- **1.6** OPEN, confirmed 14/14 + 4/4 + 2/2, and **RE-CONFIRMED LIVE on 2026-08-30**:
  `ARB-ARRIVAL: ctx_chars=3790/3790 R1=DROPPED` on `33318313852` while `/debate` publishes R1.
  Open since S83. **This is a ROOT 9 defect wearing a ROOT 1 number; it should be re-homed or
  cross-listed at the next regeneration.**
- **1.9** DE-RANKED. **RETIRE CLAUSE DUE — see RETIRE CANDIDATES.**
- **1.11** OPEN, TRIGGER FIRED (S86), boundary pinned 39–41 (S87). Round-robin pillar fill.
  With 1.14 closed, this is now the top OPEN item in ROOT 1.
- **1.12** OPEN, and **now load-bearing**: S89 confirmed by grep that `GROQ_MODEL_FALLBACK`
  reaches NO workflow, which is exactly why 9.4's default mattered. Still: **do not wire it
  before reading its value.**
- **1.13** OPEN — TECH starved in two layers independently (funnel 4 of 22; ladder dies first).
- **1.1 / 1.2 / 1.3 / 1.4 / 1.5 / 1.10** CLOSED in earlier sessions.

### ROOT 7 — THE GROUNDING GATE MEASURES "EXISTS IN THE POOL", NOT "WAS READ" · URGENT
*Untouched for eight sessions. Named here without excuse: it is urgent and it keeps losing.*
- **7.1** PARTLY PAID (S86). `checked_spans` computed and discarded at the print. R-S87-7 instance.
- **7.2** Decide the fix shape. Per-speaker baskets are in the GRAVEYARD. Unchanged.
- **7.3** PARTLY DISCHARGED (S86). Unchanged.
- **7.4** OPEN — per-run line counts include dialect, the digest excludes it. Never compare them.

### ROOT 6 — FREE-TIER RESOURCES COME WITHOUT THE GUARANTEES AROUND THEM
- **6.7** **6 OF 8 SHIPPED (S89), CANARY-CERTIFIED.** `gni_selfcheck.yml` (`6c37b38`),
  `gni_graph.yml` (`80003bb`), then `gni_adaptive` + `gni_heartbeat` + `gni_market` +
  `gni_selfbias` (`b8ceb4d`). Certified by LOG, not by conclusion: Node-20 warning **0 on v7
  against 2 on a v4 control run**; `checkout@v7` SHA `3d3c42e5…` and `setup-python@v7` SHA
  `5fda3b95…` resolved; `Successfully set up CPython (3.11.16)`; and each canary's APP step
  did its work (`Mission Control Status: HEALTHY`; entity graph wrote `20 nodes, 14 edges`
  to Supabase). **REMAINING: `gni_mad.yml` (4 sites) and `gni_pipeline.yml` (4 sites), held
  deliberately until `ee813c0` is certified — DECISION S88-5's attribution reasoning, applied
  by Claude and recorded here as a DEVIATION from generation 8's "remaining 7 in one commit".**
  TRAP still live: both files hold TWO jobs each, so `count==1` aborts; assert 2 per anchor.
- **6.6** **CLOSED (S89) — PREMISE DISPROVEN, THEN CLEANED.** Generation 8 said four `lens_*`
  tables share the project and "every runway figure includes another system's growth". Measured:
  GNI 73 tables / 87 MB; LENS 4 tables / **104 kB** = 0.1%, with `n_tup_ins = 0` on all four —
  never written, not once. The live Project Lens runs on its OWN Supabase project (URL hashes
  differ; its 23 tables hold 108k raw articles, 251 macro reports, 1,046 tier C/D rows). The
  four in gni-dusky were a schema migration run against the wrong project. Dropped this session
  behind a row-count guard that raises rather than deletes if any row is present.
- **6.2** **DE-RANKED (S89), and its premise is now measured.** Runway: 72,570 rows over 99 days
  = ~733 rows/day at ~0.95 kB/row ≈ **0.7 MB/day**; 387 MB free ≈ **550 days**. There is no
  capacity urgency this year, and the obvious deletion target is forbidden — see GRAVEYARD row 6.
  What remains of 6.2 is a real question with a long fuse: what SHOULD age out, given that
  `pipeline_articles` is an audit trail with a published claim attached.
- **6.3** SIZE METER in Mission Control — **RE-SPECIFIED (S89).** The meter reads 113 MB;
  `pg_total_relation_size` over all user tables sums to 87 MB. **26 MB (23%) is not in any
  table** (WAL, indexes on system catalogs, storage buckets). A meter built on a table sum will
  under-report by roughly a quarter. Read the real figure, do not compute it.
- **6.4** **L5 exposure when Supabase 402s — RE-SPECIFIED, and it SURVIVES 6.6's closure.**
  The exposure was never table size; it is that a 402 takes the whole project down. 6.6's
  measurement REDUCES this materially — Lens is on its own project, so a Lens Fair-Use event
  cannot 402 GNI — but GNI can still 402 itself, and there is no backup (6.5).
- **6.5** **THERE IS NO BACKUP.** Unchanged and still true. With 6.6 closed and 6.2 de-ranked,
  this is now the highest-ranked genuinely open item in ROOT 6.
- **6.1** CLOSED (S84).

### ROOT 2 — LABEL COVERAGE IS NARROWER THAN THE FABRICATION SURFACE · IMPORTANT
- **2.1** HALF-RULED (S86) — clause 2 (LABELED coverage) unmeasured; that is the only thing
  keeping 2.1 open.
- **2.2** Build B only if 2.1's second clause triggers it.
- **2.3** NARROWED (S87) — both external explanations eliminated by replay. Remaining candidates
  are all INTERNAL: article mix, prompt growth, corpus drift, agent habituation.
- **2.4** `/stocks` may render frozen prices — **narrowed (S89), not settled.** The grep shows
  `stocks/page.tsx:269-285` reading a `priceCache` and rendering `--` when absent; whether that
  cache is refreshed per request was NOT determined. One read of the fetch path finishes it.

### ROOT 3 — FALLBACK-ERA CONTAMINATION IN THE EVIDENCE BASE · IMPORTANT
- **3.1** WIDENED (S86) — `conf = 0.5` exactly on Jun 11 and Jul 7; wider than Jul 19–22.
- **3.2** `data_era` column + tagging. **Originally due ~Aug 2; now ~29 days overdue.** Recorded
  so the age is visible, not re-ranked.

### ROOT 4 — COST AND HEADROOM · IMPORTANT
- **4.5** **CLOSED (S89) — READ AT LAST, 34 DAYS LATE, AND THE BLOCKER WAS FICTION.** Generation
  8 pointed at "the `groq_quota` TELEGRAM line"; `git grep groq_quota -- ai_engine/ .github/`
  returns **nothing** — the place it named does not exist, which is why it was never read.
  The real source is `groq_daily_usage`, written by `quota_guard.log_usage()` from three
  callers. Measured, last 14 days, stable: **`morning`/`gni_mad` 66–72K tokens · 21 requests ·
  `evening`/`gni_mad` 66–72K · 21 · `not_mad`/`gni_pipeline` 31–42K · 10–12.** Lifetime:
  `gni_mad` 247+65 runs / 11.7M tokens; `gni_pipeline` 129 runs / 2.08M since Jun 25 at
  **16,144 avg** (the figure now published, see 9.3). S86's 60–75K estimate is CONFIRMED.
- **4.1** C2 solver recalibration. `ctx-trim` fired again at S87, so not dormant.
- **4.4** Measure chars/token PER POSITION. `//3` is SAFE; do not move to `//4`.
- **4.3** Groq TPD refills continuously.
- **4.2** CLOSED AS ACCEPTED (S86).

### ROOT 5 — INSTITUTIONAL HARDENING · BELOW THE LINE
- **5.5** `DEBT_REGISTER_S69.md` has no reader. **S89 read it once** (for 6.6's lineage) and it
  answered correctly: SEC-1 was "cancelled by James, never caused issues". A register with one
  reader per five months is still not a register.
- **5.6** `GNI_RULES.md` grew again this close. Largest artifact in the set; no session reads it
  end to end. Pairs with 9.6, which now has TEACH: two of the three IDs CONTRACT cites as law
  are not in the register at all. **The GRAVEYARD remains the counter-experiment and it worked
  this session — it was read at open and it is what should have stopped the 8.11 re-derivation.**
- **5.7** BYTE-CONFIRMED (S88). Seven `reports` columns never written; two of them RENDERED on
  `/autonomy`. `escalation_score_raw` (8.6) fixes one of the two cells. Unchanged otherwise.
- **5.8** OPEN — UNNUMBERED items are invisible to the uniqueness assert and vanish.
  **S89 proved the rule against its own author: the S88 close itself left TWO unnumbered
  leads behind — the 5.2 reopen proposal and the generation-1/2 retire-roster grep. Both are
  now numbered below (5.11, 5.10).** A rule minted at a close does not protect that same close.
- **5.9** **SHIPPED (S89) `bb6bd2f`.** `docs/STATUS.md` deleted — an S46 fossil retired as a
  file type at Protocol v1, carried unnumbered through generations 4–6.
- **5.10** **NEW.** The generation-1/2 retire roster (TRANS-COUNT-CERT, CI-DEGRADE, mojibake
  print, adaptive-tidy, promotion-proposal parser, fallback live-fire, "the parked 16") has no
  disposition in any order file at HEAD. `git log --all -S'parked 16' -- docs/` shows the string
  last present at **`ee92a5a` (the S84 close, generation 4)**; `ee92a5a`'s own line 317 reads
  "RETIRED: none due — the clause completed a full cycle at generation 3", so the disposition
  should be in GENERATION 3. **Not yet read.** One command:
  `git show ee92a5a:docs/GNI_TARGET_AND_ORDER.md | grep -nE 'CLOSED|RETIRED|PROMOTED|parked 16'`
  (MSYS note: `git log -S ... -- docs/` triggers `.gitattributes` textconv and dies on a missing
  `docx2txt.exe` — pass `--no-textconv`.)
- **5.11** **NEW, PROPOSED.** Reopen 5.2 (dead-symbol / unwired-module CI detector), closed as
  accepted at S84. S88 and S89 between them found five instances of that exact class by hand:
  5.7's seven unwritten columns, the rendered-but-never-written `_lower`/`_upper`, the false
  FT-11 comment, the unreachable `||` in 9.9, and the wrong `8h spacing` comment. Unmeasured.

### LIFECYCLE + SECURITY — target-independent, deadline-driven, never ranked away
**WRITTEN OUT IN FULL. "Unchanged from generation N" is BANNED here (DECISION S88-4).**
- **PHISH-HW: OVERDUE since ~Jul 31 (~31 days).** OAuth + GitHub Apps review, security log from
  2026-07-18, report the trypatchhog.com mail. Browser, James solo, ×3 accounts.
- **KEYFILE ROTATION: OVERDUE since Aug 9 (~22 days).** One account at a time, quiet window
  ~03:30–09:30 UTC. Receipts = `gh secret list` updatedAt before/after; never echo a key.
  **S89 correction to generation 8's note:** the window is NOT invalidated by lateness — the
  protection/blackout windows are fixed clock ranges (`PROTECTION_WINDOWS = 23:00–01:30,
  09:00–10:45`; `BLACKOUT_WINDOWS = 01:30–02:30, 09:30–10:30`, `monitoring_pipeline.py:37-47`)
  and they are CONTIGUOUS, covering both `02:13` and `10:13` slots with no gap. Re-derive from
  `gh run list` on the day anyway, but the stored hours are not stale.
- **PROBE-DRIFT: OVERDUE since Aug 24 (~7 days).** Monthly, needs James's explicit authorization
  each run, never on a near-red account.
- **OC-A**: closed Jul 25, next quarterly re-check ~Oct 25.
- **PROVIDER + PLATFORM EOL WATCH — record at announcement, not at death.**
  - **`actions/checkout@v4` + `actions/setup-python@v5` → item 6.7. 6 of 8 workflows now on v7;
    `gni_mad` and `gni_pipeline` still warn on every run.**
  - `gemini-2.5-flash` dies Oct 16 (Lens's lens2 runs on it).
  - `llama-3.1-8b-instant` died Aug 16 — last hardcoded default removed at S89 (9.4).
  - Supabase free tier warns by EMAIL at 20% of a limit, then a grace period, then restricts,
    with no second grace period. Storage 113/500 MB. **No longer shared with Project Lens.**

### RETIRE CANDIDATES — the clause, honestly counted
- **1.9** — de-ranked at generation 5, unworked since. **Generation 4 of 3 — OVERDUE.**
  Generation 8 wrote "DUE AT S89. It is CLOSED as accepted or PROMOTED with a written reason
  at the next close. Not this one." S89 did not work it and does not have its text in front of
  it, so it is neither closed nor promoted here — **that is a clause violation, recorded rather
  than hidden, and it is the FIRST item S90 must dispose of before anything else in ROOT 1.**
- **4.4** — promoted with a written reason at generation 7; carried on that reason.
- **5.10 / 5.11** — new this close, first generation, not candidates yet.
- No item is dropped silently this close. Generations 1–7 verified by grep at S88 (5.1 / 5.2's
  CI half / 5.3 CLOSED AS ACCEPTED at S84, 5.2's fallback half PROMOTED to 1.10). Generation 1–2's
  retire roster is now item 5.10 rather than an unnumbered lead.

---

## CHANGED THIS REGENERATION

**MISSION: HALF COMPLETED. 6.7 done and certified beyond its stated bar; 8.6's cert BLOCKED
by the absence of a scheduled run, not by any decision.** `ee813c0` landed at 19:22:15Z on
Aug 30, after that day's last pipeline run (14:52:07Z); by 05:20Z on Aug 31 the next slot's
run had not yet arrived. The cert query, the six predictions and the failure test are carried
forward verbatim to S90. **6.7 exceeded its bar in one respect and fell short in another:**
certified by LOG with a v4 control rather than by conclusion, but 6 of 8 workflows rather
than 8 — see DECISION S89-1 and the DEVIATION note in 6.7.

**SHIPPED — eight commits, every one with `npm run build` 40/40 and explicit staging:**
`6c37b38` (6.7 canary 1) · `80003bb` (6.7 canary 2) · `dbc2f92` (9.7 ladders) ·
`b8ceb4d` (6.7 sweep ×4) · `bb6bd2f` (5.9 STATUS.md) · `b9c1f03` (9.7b levels table) ·
`223da0f` (9.3 workflow count + token figure) · the `nexus_analyzer` fallback commit (9.4).
Plus one SQL change: four empty `lens_*` tables dropped from gni-dusky (6.6).

**CLOSED:** 1.14 (blocker disproven) · 1.7 (discharged, second `truncated=0`) · 1.8 (SQL:
0 of 196 rows ever hit the surviving clause) · 4.5 (read at last; the named source did not
exist) · 6.6 (premise disproven, then cleaned) · 5.9 (shipped) · 9.8 (shipped) ·
9.7 and 9.3 and 9.4 SHIPPED, cert pending.

**NEW:** 1.14b · 9.9 (unreachable `||`; the measured interval has never been shown) ·
9.10 (deferred by decision) · 9.11 (100K vs 85K token claim) · 5.10 · 5.11 ·
GRAVEYARD row 6.

**RE-RANKED:** ROOT 8 keeps the top slot ONLY for 8.6's cert. ROOT 6 falls — 6.6 closed, 6.2
de-ranked on a measured 550-day runway — leaving 6.5 (no backup) as its live item. ROOT 9 holds
URGENT and is now the largest root by open-item count. **ROOT 7 is named as the loser: eight
sessions untouched, still urgent, and no session has chosen it. If S90 does not either work it
or de-rank it with a written reason, the honest move is to admit the rank is decorative.**

**DECISION S89-1 — the Node-20 pin uses the MAJOR FLOAT `@v7`, not an exact tag or a SHA
(option A over B and C).** Reason: this item's root cause is maintenance latency, not supply
chain — the system fell three majors behind because nobody came back, and B/C both require a
human to come back for every patch release, which reproduces the cause. `actions/*` is
published by GitHub itself and the canary produces no intelligence, so a moved tag is visible
immediately. `LINEAGE:` grep of all `*.md` in the close set — the docs name the target versions
(`checkout@v7.0.1`, `setup-python@v7.0.0`) but contain NO prior ruling on pin style; first
decision on this subject. **Cost accepted: an upstream `v7` retag changes our runners without
our knowledge. The canary is the detector.**

**DECISION S89-2 — 9.7 is fixed by aligning the frontend ladders to the engine; 9.10 (prefer
the DB column and delete the ladders) is DEFERRED until `ee813c0` is certified.** Chosen over
doing 9.10 now, which is the architecturally correct end state and is already the house pattern
on `/comparison`. Reason is ATTRIBUTION, identical to DECISION S88-5: 9.10 requires editing
`/api/health/route.ts`, one of `ee813c0`'s own files, and a failed cert would then be
un-diagnosable between the column write and the select change. `LINEAGE:` `grep -rn
'scoreToLevel|CRITICAL|HIGH' src/` (found the second inline ladder and the prose line) plus
`grep -rn 'FT-' src/` (one hit, proving 9.8's family is small) plus a conversation search that
found the March-2026 origin of the 8/6/4/2 numbers.

**DECISION S89-3 — the public workflow count reads "8 workflows: 4 core + 4 support", not
"8 pipelines" and not an expanded eight-card array (option B over A and C).** Chosen over A
(swap 4→8 in the prose) which would have left a card list of four under a heading saying eight
— the exact self-contradiction `dbc2f92` created on `/autonomy` two hours earlier — and over C
(write four new cards) which would have required inventing four schedules, four token figures
and four descriptions, i.e. publishing unmeasured constants under a target named TRUTHFULNESS.
Every figure in the shipped copy was measured this session. `LINEAGE:` `git grep -nE '\b4\b.*
pipeline' -- src/` → 7 sites, not the 6 the item claimed; `ls .github/workflows/*.yml | wc -l`
→ 8, confirmed visually in the GitHub Actions UI.

**DECISION S89-4 — `pipeline_articles` rows are NOT deleted, and 6.2 is de-ranked.** Chosen
over an age-based or `stage4_selected=False` retention policy. Reason: the March-2026 design
record states the table's purpose is Explainable-AI evidence — "every rejected article is
visible with reason", the basis of KPI 1 and KPI 3 and of the published claim that GNI is more
transparent than industry systems — and `git grep` finds eight consumers in `src/` including
`/transparency`, `/history`, `/api/pipeline-articles` and `/api/export/articles`. Deleting the
audit trail while the site still claims the audit trail exists would be a TRUTHFULNESS defect
larger than any this session fixed. Measured runway (~550 days) removes the urgency that made
the proposal look reasonable. Entered in the GRAVEYARD as row 6. **The bytes said "no query
filters on `False`"; the record said what the rows are for. See R-S89-2.**

**DECISION S89-5 — the four empty `lens_*` tables are dropped from gni-dusky.** Chosen over
leaving them (they made every ROOT 6 figure ambiguous) and over investigating further (four
byte-level facts settled it: `n_tup_ins = 0` on all four; GNI's code never names them;
Project Lens's own Supabase project holds the live data under the same names with 1,404 rows
across the four; the two `SUPABASE_URL` values hash differently). Executed inside a `do $$`
block that raises rather than drops if any row is present, so running it against the wrong
project is safe. **GNI-R-238 was cited in chat as the rule permitting the sharing; it is NOT
in `docs/` — this is a 9.6 instance committed by Claude during the same session that measured
9.6.**

**DECISION S89-6 -- EVERY CLOSE SHIPS ALL FIVE ARTIFACTS SESSION-NUMBERED, EVEN WHEN THE
CONTENT IS BYTE-IDENTICAL. Ruled by James at this close.** Chosen over the carry-forward
habit S88 started (`CONTRACT_S85.md` shipped unrenamed in the S88 set) and that S89 cited
back as precedent. Reason: CONTRACT CLOSE DELIVERY v6 enumerates all five filenames with
`S{N}` and closes the clause with NO EXCEPTIONS, and Protocol PART C step 13 repeats it --
the produced-vs-carried distinction Claude argued from is in neither document, it was
invented at this close to justify what the previous close had done. **Protocol swept to v9
the same close (R-S82-4): v8's own VERSION LOG entry ended with `CONTRACT_S85.md` carries
forward, so the template was carrying the deviation into every future session -- that
parenthetical is now RETRACTED in place.** Cost accepted: four of five files in most close
sets will be byte-identical to their predecessors, so sameness is verified by `md5sum`,
never by filename. `LINEAGE:` CONTRACT_S89 CLOSE DELIVERY v6 read in full; Protocol PART C
step 13 read in full; `md5sum` proving both carried files unmodified before the rename.

**TRAP DISPOSITION (promote or expire, no trap rides forward unchanged twice):**
- `/autonomy` renders `Raw Magnitude --` until the first post-`ee813c0` run — **SECOND CARRY →
  PROMOTED to R-S89-3.** It cannot expire, because the cert it waits on has not happened, and
  CONTRACT forbids a third unchanged carry. The general lesson (a newly added column renders
  the same `--` as a broken one, so the page looks identical to a failed ship) is now a rule;
  the specific work stays inside 8.6's cert.
- **NEW TRAP (first carry, temporary):** four commits changed PUBLIC COPY this session
  (`dbc2f92`, `b9c1f03`, `223da0f`, and 9.4's engine default) and NONE has been seen in a
  browser. Vercel deploy is unverified; curl is a dead end (R-S54-4). **Expires the moment
  `/autonomy`, `/methodology`, `/research` and `/about/devops` are opened and read.**

**ITEM UNIQUENESS — expected count stated IN ADVANCE by LISTING, not by counting from memory
(two consecutive closes were off by exactly one when counted from memory).**
ROOT 8: 8.1, 8.1a, 8.1b, 8.1c, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 8.10 = 13.
ROOT 9: 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9, 9.10, 9.11 = 9.
ROOT 1: 1.6, 1.7, 1.8, 1.9, 1.11, 1.12, 1.13, 1.14, 1.14b = 9.
ROOT 7: 7.1, 7.2, 7.3, 7.4 = 4. ROOT 6: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7 = 7.
ROOT 2: 2.1, 2.2, 2.3, 2.4 = 4. ROOT 3: 3.1, 3.2 = 2.
ROOT 4: 4.1, 4.2, 4.3, 4.4, 4.5 = 5.
ROOT 5: 5.5, 5.6, 5.7, 5.8, 5.9, 5.10, 5.11 = 7.
13+9+9+4+7+4+2+5+7 = **60 distinct IDs**, with exactly three intentional repeats
(`**1.9**`, `**4.4**`, and `**5.10**`/`**5.11**` appearing once in ROOT 5 and once under
RETIRE CANDIDATES — count that as `**5.10**` and `**5.11**` repeating). Verify:
```bash
grep -oE '\*\*[0-9]+\.[0-9]+[a-c]?\*\*' docs/GNI_TARGET_AND_ORDER_S89.md | sort | uniq -d
grep -oE '\*\*[0-9]+\.[0-9]+[a-c]?\*\*' docs/GNI_TARGET_AND_ORDER_S89.md | sort -u | wc -l
```
The first must print only `**1.9**`, `**4.4**`, `**5.10**`, `**5.11**`; the second must print 60.

---

## HOW THIS FILE IS MAINTAINED
Regenerated at every close, dated, superseding. Never appended — **except the GRAVEYARD, which
is carried forward verbatim (DECISION S88-2, Protocol v8 PART C step 5).** One mission per
session, taken from the top. Decisions live here as DECISION lines — GNI mints no separate
D-register. FRESHNESS CONFERS NO PRIORITY.
