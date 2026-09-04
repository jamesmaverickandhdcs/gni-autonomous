# GNI TARGET + WORKING ORDER
**GENERATION 18 - 2026-09-04 (S99 close). SUPERSEDES generation 17 (`GNI_TARGET_AND_ORDER_S98.md`).**
Regenerated, never appended. The LIVE order is the HIGHEST session number.

---

## NEXT SESSION'S MISSION (S100)

**ARCHITECTURE section 5, BUILDING BLOCK VIEW, GENERATED FROM THE AST by a named tool in
`tools/`, regenerating byte-identically on an unchanged tree.**

WHY THIS IS TOP. It is JAMES'S roadmap 2, row 3 (DECISION S96-1), and row 2 shipped this close
at `2bfef91`. Section 6 answered "what actually ran"; section 5 answers "what is written" -
module, what it imports, WHO CALLS IT, which test covers it. That last field is the one both
S99 and S94 deliberately refused to answer, in writing, so that section 5 would own it.

**Definition of done:** `tools/<n>.py` writes section 5 into `docs/GNI_ARCHITECTURE_S100.md`;
run it twice on an unchanged tree and `md5sum` both outputs - identical; then flip ONE source
fact and it moves. It refuses with exit 2 on a missing input (R-S93-1), requires `--session`,
and publishes EOL-normalised hashes (R-S98-3). **`tools/gni_runtime.py` is the pattern, not
`tools/gni_state.py`** - the latter puts a clock inside its own output and fails the roadmap's
own completion test on that account (item **5.33**).

**Read before designing:** the AST is a static reader. "Imports X" is not "calls X at run time",
and section 6 already holds the runtime side. A dead-symbol / unimported-module check is the
highest-leverage by-product available here - it is the class that produced DET-DEAD and
`_FORCE_PROVIDER`, five months apart, both found by accident.

**THE ONE ITEM I WOULD RANK ABOVE THIS, for James to rule at the S100 open: item 6.11.**
GNI's own crisis posture promises that the heartbeat wakes the adaptive pipeline the moment
the escalation delta crosses its threshold, and that promise is built on a 30-minute cadence
(`gni_heartbeat.yml` declares `0,30 * * * *`). The measured
cadence is 3 to 7 hours. The system's stated detection latency and its actual detection latency
differ by an order of magnitude, and nothing published anywhere says so. It is COR, it is live,
and it is on-target for TRUTHFULNESS OF OUTPUT. I am NOT working it in place of the roadmap;
it is filed, ranked at the top of ROOT 6, and named here so the choice is James's.

## TARGET - UNCHANGED

**TRUTHFULNESS OF OUTPUT.** What GNI says must be what GNI measured.

Roadmap 2 is **2 of 4** (Protocol PART C step 4a). Row 2 shipped at this close; its written
completion test lives in `GNI_ARCHITECTURE_S99.md` with a per-row status table, and that table
now names a failing row the S98 close did not know about: **row 2 fails on section 7's own
account**, not only because section 5 is missing.

**DEFINITION OF DONE - status at this regeneration:**
- the arbitrator reads what it claims to read - ROOT 1, ARCHIVED at S96. Unchanged.
- the escalation score carries information - ROOT 8, ARCHIVED at S96. Unchanged.
- the grounding gate measures reading, not existence - ROOT 7 IMPORTANT, still blocked on
  item **7.1**'s instrument. Unchanged.
- the public surface matches the configuration - **ROOT 9 stays TOP**, unchanged this close.
  But see ROOT 6: the CONFIGURATION itself no longer matches what runs, which is a second
  door into the same target and is why ROOT 6 gained two items.

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
| **SWAP A PUBLISHED FIGURE FOR A FRESHER ONE WITHOUT ITS WINDOW** (S89's `6,175 → 16,144`, and S90's own first repeat of it) | DECISION S90-3, S90 measurement | `groq_daily_usage` holds TWO regimes: Mar/Apr/May `gni_pipeline` = exactly `6175` every month (a reservation constant, not a measurement), Jun 6,502, Jul 15,980, Aug 17,780. `16,144` was an average across the boundary and is reproducible from no window. The published figure must carry the window that produced it. |

**Reading this table is not optional before proposing anything in ROOT 8 or ROOT 1.**
A proposal that lands in this table without new measurement is a LINEAGE-BEV failure.

---
---

<!-- GRAVEYARD-END -->

<!-- GRAVEYARD-END -->

**md5 OF THIS SECTION, WITH THE COMMAND THAT PRODUCES IT (R-S96-2, R-S98-3, item 5.28):**
```bash
sed -n '/^## .*GRAVEYARD/,/^<!-- GRAVEYARD-END -->/p' docs/GNI_TARGET_AND_ORDER_S99.md \
  | tr -d '\r' | md5sum
```
Expected: `3e8ac222c6ef212261676c02d7d56f6f` - the SAME value generations 16 and 17 published,
verified against generation 17's bytes BEFORE this file was written (R-S95-1).

## THE CROSS-ROOT DIAGNOSIS (carried from generation 7 - now with five instances)

> **GNI repeatedly measures what it has already guaranteed itself, and publishes the result as
> a fact about the world.**

| instance | what is measured | what it actually is |
|---|---|---|
| ROOT 7 | "the span exists in the pool" | reported as "the agent read it" |
| ROOT 8 gate | `_high_escalation` True six of six | a crisis channel that cannot leave crisis mode |
| ROOT 8 bonus | `diversity_bonus` at ceiling in most runs | the S39 funnel quota guarantees all three pillars |
| ROOT 8 GEO | GEO pillar "active" in every run | GEO hits far exceed the cap - the pillar cannot be inactive |
| ROOT 8 PHI | the PHI gate "protecting" the score | it has never fired; its own mute condition fires with it |

Its use is predictive - when a metric is nearly constant, ask WHO GUARANTEED IT before tuning it.
No sixth instance was added this close and no row changed.

**S99 NOTE - the S98 form of this diagnosis held again, four times, and once in the reverse
direction.** Three S98 instruments reported clean results about themselves; S99 produced four
more (R-S98-6's amendment lists them). The reverse case is new and worth the line: a measure can
also be bounded by the thing it measures, so it reports its SMALLEST possible answer exactly
where the truth is largest - a 365-minute lag read as 5 minutes (R-S99-1). Ask not only "who
guaranteed this constant" but "what is the largest number this instrument could ever return".

---

## THE ORDER

Every line carries an ISO/IEC 14764 class (DECISION S92-4): **COR**rective (something is broken),
**ADA**ptive (the world moved), **PER**fective (it works, it could be better), **PRE**ventive
(nothing is broken yet).

**EXPECTED ITEM COUNT: 53 distinct numbered items between `## THE ORDER` and `## ARCHIVED.**
Generation 17 held 46 and this close closed none of them and opened seven - the mission was a
roadmap row, not an order item, and that is said plainly rather than dressed up. Every id is
bolded so the published command is true of the file it sits in, and a second differently-shaped
scan is printed beside it to reconcile against (R-S98-6):

```bash
sed -n '/^## THE ORDER/,/^## ARCHIVED/p' docs/GNI_TARGET_AND_ORDER_S99.md \
  | grep -oE '\*\*[0-9]+\.[0-9]+' | sort -u | wc -l
sed -n '/^## THE ORDER/,/^## ARCHIVED/p' docs/GNI_TARGET_AND_ORDER_S99.md \
  | grep -oE '[0-9]+\.[0-9]+' | sort -u | wc -l
```

Both must print **53**. If they disagree, an id is unbolded or a decimal has entered the prose,
and the count is not to be trusted until they agree.

### ROOT 9 - PUBLIC COPY AND REPORTED STATUS DRIFT FROM WHAT WAS MEASURED - URGENT - **TOP**

- **9.19** OPEN (S96) [PARTLY MEASURED at S98] - COR - DEGRADE-SILENT. A run in which `ctx-trim`
  leaves ZERO articles still reports SUCCESS. First byte evidence at S98 (`ARB-FIT: ctx_depth=0
  est=4997/5000`); still not the zero-article case. Next move: find a run at `ctx-trim@0`.
- **9.20** OPEN (S98) [PROPOSED, UNMEASURED] - COR. `mad_runner.py` prints `MAD skipped cleanly`
  and returns True. NOTE (S99): this is NOT the GitHub job-level `skipped` that R-S84-4's
  amendment describes; they look alike in a run list and are different doors. Do not conflate.
- **9.16** OPEN (S93) - COR. Records are from the `setup-python` side only.
- **9.17** OPEN (S94) - COR. Same shape as **9.16**, one generation later.
- **9.18** OPEN (S95) - COR. Carried unchanged.
- **9.5** OPEN - COR. Eight unresolved S69 census flags; F14 renders BEARISH over a stale basis.
- **9.11** OPEN - COR. `research/page.tsx` publishes a Groq daily-token figure against a May record.
- **9.12** OPEN [PROPOSED, not measured] - COR. `/about/devops` compares a three-account token SUM.

### ROOT 6 - FREE-TIER RESOURCES COME WITHOUT THE GUARANTEES AROUND THEM - **RE-RANKED UP (S99)**

**RE-RANK, with the reason generation 18 owes for it.** This root sat below ROOT 5 for four
generations as a storage-and-backup root. S99 measured that it also holds a LIVE CAPABILITY GAP:
the two 30-minute crons deliver about a third of their declared slots, and the guarantee GNI
publishes about its own detection latency rests on the cadence that is not happening. That is
target-bearing, not housekeeping.

- **6.11** **NEW (S99)** [MEASURED] - COR - **THE PROMISE AND THE CADENCE DISAGREE BY AN ORDER OF
  MAGNITUDE.** The heartbeat is designed to wake the adaptive pipeline the moment the escalation
  delta crosses its threshold, and the whole crisis posture rests on a 30-minute watch:
  `gni_heartbeat.yml` declares `0,30 * * * *` and `monitoring_pipeline.py` is the zero-Groq
  watcher behind it. The March-2026 rules that state this IN WORDS are deliberately NOT cited by
  id here - two of the three are absent from the register, which is item **5.37**.
  Measured over 16 complete days (`docs/gni_runtime_snapshot_S99.json`):
  `gni_heartbeat.yml` delivered 282 of 768 declared slots, `gni_selfcheck.yml` 292 of 768, and the
  per-day figure runs from 4 percent to 77 percent. Real spacing between heartbeats is 2-7 hours.
  Nothing published anywhere states this. **The question the item asks is NOT "how do we make
  GitHub faster" - there is no lever there. It is: what cadence does GNI actually have, and what
  should it therefore PROMISE?** Answer that before changing any cron. Kin of **9.11**/**9.12**:
  a published figure that no longer describes the system.
- **6.10** **NEW (S99)** [MEASURED] - ADA - **THE FREE TIER GIVES NO DELIVERY GUARANTEE, NOT
  MERELY NO TIMING GUARANTEE - AND THAT WAS NEVER MEASURED.** The ARCHIVED row "the lateness
  band" was archived because "a free-tier scheduler gives no timing guarantee". That reason
  understates it: R-S87-6's "zero runs missed" was measured over crons firing 1-3 times a day
  (S87 n=133, S91 n=8 slots) and is FALSE for the two firing 48 times a day. The delivery ratio
  is a distinct property with a distinct instrument, and the instrument now exists
  (`tools/gni_runtime.py`, the delivery table in section 6). Derived lateness band at this close: **744 min**.
  Un-archives the lateness row by measurement, per the ARCHIVED section's own condition.
- **6.5** OPEN - COR - **THERE IS NO BACKUP.** Still the highest single-point loss in the system,
  now for EIGHT generations, and never the mission. Said plainly rather than re-ranked again.
- **6.3** RE-SPECIFIED (S89) - ADA. Meter against tables; the difference is unexplained.
- **6.4** OPEN - ADA. L5 exposure when Supabase 402s. Paired with **5.30**.
- **6.8** OPEN (S90) - ADA. Heartbeat standdown suspends a block of zero-Groq checks daily.
  NARROWED (S99): this was the obvious candidate for **6.11** and it is NOT the cause. The
  standdown is ~4h15m/day = ~17 slots per 48 hours, against 66 unexplained; and it suspends
  CHECKS INSIDE a run, which still appears in the run list. Ruled out by arithmetic, not by
  opinion. The item stands on its own original merit (a rationale that cites token collision for
  a zero-Groq workflow).

### ROOT 5 - INSTITUTIONAL HARDENING - the roadmap's own root

- **5.33** **NEW (S99)** [MEASURED] - COR - **SECTION 7 FAILS THE ROADMAP'S OWN COMPLETION TEST.**
  `tools/gni_state.py` renders `datetime.now(timezone.utc)` INTO its generated stamp, so two runs
  two seconds apart on an unchanged tree differ (`06:14:00Z` vs `06:14:04Z`, md5 differs on that
  one line, verified). Roadmap 2's completion test row 2 requires every generated section to
  reproduce byte-identically. The S98 close recorded row 2 as failing only because sections 5 and
  6 were missing; section 7 fails it on its own account. Fix shape: the provenance stamp carries
  the INPUT's identity (HEAD, source name, normalised md5), never the render clock -
  `tools/gni_runtime.py` is the worked example.
- **5.34** **NEW (S99)** [MEASURED] - PRE - **M4'S SIBLING SWEEP MISSED ONE.** S98 made
  `tools/gni_macro_map.py` require `--session` (exit 2 on a bare call - the item S98 closed at `a5f2813`). `gni_state.py`
  still carries `ap.add_argument("--session", type=int, default=94)`, so a bare invocation reads
  the newest architecture document and writes `docs/GNI_ARCHITECTURE_S94.md` - S98 content under
  an S94 name, which is precisely the artifact DECISION S98-3 deleted. Protocol PART C step 9a
  now tells every close to run the generators, so this is on the path.
- **5.35** **NEW (S99)** [MEASURED, DISCLOSED AT SHIP TIME] - PER - **`gni_runtime.py`'s PAIRING
  ASSUMES FIFO AND REFUSES AT THE WINDOW EDGE.** Two limitations, both written into section 6.5
  rather than left to be found: (a) ordered matching assumes the scheduler delivers slots in
  order, and MAD's 10:43 and 11:13 slots are 30 minutes apart against a 12-hour band, so an
  out-of-order delivery would mis-pair silently; (b) against a synthetic uniform 12-hour lag the
  pairing REFUSES with "a run BEFORE its slot at the window edge" even though delivery was
  complete. The failure direction is safe - NOT MEASURABLE rather than a wrong number - but it is
  a false negative. Fix: widen run collection past the window end without letting the previous
  day's runs leak in.
- **5.36** **NEW (S99)** [MEASURED] - PRE - **THE SNAPSHOTS HAVE NO RETENTION.**
  `docs/gni_runtime_snapshot_S99.json` is 182,578 bytes and section 6 is regenerated every close,
  so one lands per session. That is deliberate - the snapshot IS the evidence and must be in the
  tree for the byte-identity test - but nothing says when an old one may go. Kin of **6.5** and of
  the Lens retention lesson: a stock grows, a flow does not. Decide the policy before there are
  twenty.
- **5.37** **NEW (S99)** [CAUGHT BY THE DETECTOR] - COR - **TWO MORE UNREGISTERED RULE IDS, AND
  C1 FAILED THIS CLOSE'S OWN DRAFT OVER THEM.** Generation 18's first draft cited three March-2026
  heartbeat/adaptive rule ids recovered from the session records; `tools/gni_rule_checks.py` C1
  failed on two as unregistered and unmanifested BEFORE the docs commit. Same class as the eight
  S90 recovered into PART 0 - now ten. The citations were removed rather than the ids invented:
  DECISION S90-4 ruled that guessing an id repeats the failure being fixed. WHAT IS OWED: recover
  both from the session records with their evidence and enter them in PART 0, or declare them lost
  in writing. Their subject is the cadence promise in **6.11**, so the two travel together.
  FOR THE RECORD: the detector S98 spent a whole session making green just failed the session that
  wrote it. That is the first time a check in this repo has caught its own close.
- **5.30** OPEN (S98) [MEASURED] - COR. `_fetch_relevant_articles` returns an empty pool from
  three places and `run_mad_protocol` divides by its size. Written fail-open, behaves fail-hard.
  The policy question IS the item: what should MAD publish when it has no articles?
- **5.31** OPEN (S98) [MEASURED] - PRE. Model resolution has no floor; resolved at module import.
- **5.32** OPEN (S98) [MEASURED] - PER. `dryrun_two_account_split.py` sits at the REPO ROOT,
  outside the CI glob, exits 1, never read.
- **5.28** OPEN (S96) - COR. An unverifiable checksum. Practice continued this generation.
- **5.29** OPEN (S96) - PER. The register has six entry shapes. Load-bearing: C6 reads it through
  the generator's parser. S99 appended in the dominant shape and did not regularise.
- **5.21** OPEN (S94) - PRE. No `.gitattributes`. Unchanged at this close: the register alone is
  `i/lf w/crlf`, and S99's append deliberately preserved its CRLF rather than silently
  converting 1556 line endings inside a docs commit.
- **5.20** PARTIALLY DISCHARGED (S94/S95) - PRE. Fixture at 14 families. What remains is the
  control probe's own evidence.
- **5.22** OPEN (S95) [ONE INSTANCE MEASURED at S99] - PER. Console fragility of `tools/*.py` on
  Windows. Instance: `python tools/gni_state.py --stdout` dies with `UnicodeEncodeError` on
  `\u2192` under cp1252 and exits 1 - an exit code its own docstring does not list. The
  file-writing path is safe (`write_text(encoding="utf-8")`); only `--stdout` is affected.
  `tools/gni_runtime.py` reconfigures stdout at import and does not have it.
- **5.23** OPEN (S95) - PER. C5's blind spot.
- **5.24** OPEN (S95) - PER. Carried unchanged from generation 15. **RETIRE CLAUSE DUE.**
- **5.25** OPEN (S95) - PRE. Carried unchanged from generation 15. **RETIRE CLAUSE DUE.**
- **5.15** OPEN (S93) - PER. Selftest coverage.
- **5.16** OPEN (S93) [ONE INSTANCE MEASURED at S98] - PER. `__main__` blocks outside `tests/`.
- **5.18** OPEN (S93) - PER. Unread wrongness ledgers. Discharged once this close by hand: the
  session record is what ruled out **6.8** as **6.11**'s cause.
- **5.19** OPEN (S93) - PER. R-S91-4's disproven evidence.
- **5.5** OPEN - PER. **RETIRE CLAUSE DUE - AND UNDISCHARGEABLE AS WRITTEN.**
- **5.6** OPEN - PER. **RETIRE CLAUSE DUE - AND UNDISCHARGEABLE AS WRITTEN.**
- **5.7** OPEN - PER. **RETIRE CLAUSE DUE - AND UNDISCHARGEABLE AS WRITTEN.**
- **5.8** OPEN - PER. **RETIRE CLAUSE DUE - AND UNDISCHARGEABLE AS WRITTEN.**
- **5.11** OPEN - PER. **RETIRE CLAUSE DUE - AND UNDISCHARGEABLE AS WRITTEN.**
- **5.12** OPEN - PER. **RETIRE CLAUSE DUE - AND UNDISCHARGEABLE AS WRITTEN.**

**THE SIX LINES ABOVE ARE A DEBT THIS GENERATION IS RECORDING, NOT PAYING.** The retire clause
says an item unworked below the line for three regenerations is CLOSED as accepted or PROMOTED
with a written reason, and dropping one silently is neither. Generations 16 and 17 carried
**5.5**, **5.6**, **5.7**, **5.8**, **5.11** and **5.12** as the bare line "Carried unchanged from
generation 15" - so the current order no longer states what they ARE. Generation 18 cannot close
or promote an item whose text it does not hold, and inventing one would be R-S98-1's disease
(a compression that replaced its own subject). **S100 discharges this by reading
`GNI_TARGET_AND_ORDER_S95.md` or earlier for their full text, then closing or promoting each in
writing.** Recorded as a debt so that the next close cannot inherit it silently.

### ROOT 7 - THE GROUNDING GATE MEASURES "EXISTS IN THE POOL", NOT "WAS READ" - IMPORTANT

- **7.1** PARTLY PAID (S86) - COR. `checked_spans` computed and discarded at the print.
- **7.2** BLOCKED - COR. Fix shape undecided; per-speaker baskets are in the GRAVEYARD.
- **7.3** PARTLY DISCHARGED (S86) - PER. Unchanged.
- **7.4** OPEN (S93) [UNMEASURED] - COR. `GROUNDING SHADOW` counts disagree across instruments.

### ROOT 2 - LABEL COVERAGE IS NARROWER THAN THE FABRICATION SURFACE - IMPORTANT

- **2.1** HALF-RULED (S86) - COR. Clause two, LABELED coverage, unmeasured.
- **2.2** BLOCKED on **2.1** - PER.
- **2.3** NARROWED (S87) - PER.
- **2.4** ONE READ FINISHES IT - COR. `/stocks` may render frozen prices.

### ROOT 3 - FALLBACK-ERA CONTAMINATION IN THE EVIDENCE BASE - IMPORTANT

- **3.1** WIDENED (S86) - COR. A constant confidence value on two dates.
- **3.2** OPEN - ADA. `data_era` column plus tagging.

### ROOT 4 - COST AND HEADROOM - IMPORTANT

- **4.1** OPEN - COR. C2 solver recalibration; **9.19** carries the first log line.
- **4.4** OPEN - PER. Measure chars per token PER POSITION.
- **4.6** OPEN (S90) - ADA. `gni_mad` monthly token draw rose through the summer.

### LIFECYCLE + SECURITY - target-independent, never ranked away

**CLOCKS REMAIN PAUSED (DECISION S92-2).** 22 secrets stored. Nothing is due, nothing is overdue,
and no session may raise an item here as "overdue" until James restarts the clocks.

---

## ARCHIVED - ONE ROW LEAVES THIS CLOSE

Archived is not closed and not solved: not worked under this target, not re-ranked each close,
not re-read at open. Anything here returns only by a new measurement and a ruling.

| what | why archived |
|---|---|
| **ROOT 1** | CERTIFIED for content and ordering (S96). |
| **ROOT 8** | discharged in part at S91; the rest waited five generations under a target it does not serve. |
| the published band table | wrong in two of five rows - real, measured, not reachable before roadmap 2. |
| the dependency manifest | a roadmap-2 by-product. Note (S99): `GNI_ARCHITECTURE` section 7.3 cites an item in the six-range that this order does not carry - a dangling item citation, the order-file twin of what C1 checks for rule ids. That number is therefore NOT reused; S99 opened **6.10** and **6.11** instead. The exact id is in `GNI_ARCHITECTURE` section 7.3, deliberately not repeated here so the count commands stay true. |
| `mad_runner.py` unordered `limit(50)` | kin of R-S92-2, no consumer waiting. |

**LEFT THE ARCHIVE THIS CLOSE: the lateness band.** It was archived because "a free-tier
scheduler gives no timing guarantee". A new measurement met the ARCHIVED section's own return
condition: the free tier gives no DELIVERY guarantee either, that is a different property, and it
had never been measured. It returns as items **6.10** and **6.11**.

`docs/GNI_RULE_CHECKABILITY_S95.tsv` remains RETIRED (S96) - on disk, out of the queue.

## CHANGED THIS REGENERATION

- **DECISION S99-1 (Claude, delegated by James with "your call").** The section 5 / 6 / 7 boundary,
  written BEFORE the first line of the generator: section 7 is what is DECLARED (workflow YAML +
  `gh secret list`), section 6 is what ACTUALLY RAN (Actions run history), section 5 is what is
  WRITTEN (the AST). Section 6 does NOT answer "what calls what" even though generation 17's
  mission text used that phrase - `gni_state.py:233` and section 5's own planned contents already
  assign `who calls it` to section 5, and two sections answering one question is a routing error.
  Chosen over "source-based call chains" (needs S100's AST early, and publishes reachability as
  if it were execution) and over "both, by scenario" (depends on a section 5 that does not exist).
- **DECISION S99-2 (Claude, delegated).** The generator SPLITS harvest from render. `--harvest`
  calls `gh` and writes a git-tracked snapshot; the render reads only that snapshot. Chosen over
  calling `gh` inline, which cannot satisfy "unchanged tree reproduces byte-identically" because
  the evidence changes every 30 minutes, and over a manual harvest outside any tool, which makes
  the harvest a habit rather than an artifact. Cost accepted: one 182 KB file per session, filed
  as **5.36**.
- **DECISION S99-3 (James).** Section 6.1 publishes the per-day delivery DISTRIBUTION beside every
  window figure. Chosen over a bare window ratio, which put a published figure in the GRAVEYARD at
  DECISION S90-3, and over "a last-N-days ratio", which needs a hand-written N and would trip C5.
  Nothing is hand-written: the spread is derived from the same per-day table section 6.4 prints.
- **DECISION S99-4 (Claude, reversible).** Lateness is attributed by ORDERED MATCHING and published
  only where delivery was complete. The nearest-preceding-slot method is rejected IN the section
  and re-probed on every run, because it is bounded by slot spacing and reported a 365-minute lag
  as 5 minutes. Where no pairing exists, section 6 prints the reason instead of a number.
- **DECISION S99-5 (Claude, reversible).** Runs are attributed to the SLOT they served wherever a
  pairing exists, not to their creation day. Creation-day attribution published 114 percent for
  `gni_market.yml`. The fallback is named inside the output rather than left for a reader to find.
- SHIPPED: **roadmap 2 row 2** - `2bfef91`, CI green at JOB level (run `33851242047`,
  `harnesses success` + `rule_checks success`). `tools/gni_runtime.py`,
  `docs/gni_runtime_snapshot_S99.json`, section 6 in `docs/GNI_ARCHITECTURE_S99.md`.
- CLOSED: **nothing**. rho = **0 / 7** this generation. The mission was a roadmap row rather than
  an order item, so the queue grew by construction; recorded plainly because a ratio dressed up is
  the loop the discovery policy exists to catch.
- NEW: **5.33**, **5.34**, **5.35**, **5.36**, **5.37**, **6.10**, **6.11**. **5.37** was opened
  by the detector failing this close's own draft, not by a session reading code.
- RE-RANKED: **ROOT 6** moves above ROOT 5, with the written reason in the root itself - it now
  holds a live capability gap, not only storage and backup.
- UN-ARCHIVED: the lateness band, by measurement, per the ARCHIVED section's own return condition.
- RECORDED AS A DEBT, NOT PAID: the retire clause on **5.5**, **5.6**, **5.7**, **5.8**, **5.11**
  and **5.12**. Their text was compressed away before generation 16; S100 reads
  `GNI_TARGET_AND_ORDER_S95.md` or earlier and closes or promotes each in writing.
- NOT DONE, AND DECLARED RATHER THAN SKIPPED: `npm run build` before the mission commit. CONTRACT
  requires it; this commit touched only `tools/` and `docs/` and no file under `src/`. Whether the
  rule should be scoped to src-touching commits is a CONTRACT question and is James's, not mine,
  so the contract is unchanged at v10 and the omission is on the record instead.

## HOW THIS FILE IS MAINTAINED

Regenerated at every close, dated, superseding, never appended. The GRAVEYARD is the single
exception and is copied BY BYTES, never retyped - this generation's copy was verified against
generation 17's published md5 BEFORE the file was written, and again inside the assembled file
(R-S95-1). The item count carries two commands beside it and both were run on the ASSEMBLED file,
not on a draft: they disagreed at 52 against 56 on the first attempt, four bare decimals had
entered the prose, and the prose was rewritten rather than the command weakened (R-S98-6).
Freshness confers no priority: an item found today does not outrank an item found in June unless
a measurement says so.
