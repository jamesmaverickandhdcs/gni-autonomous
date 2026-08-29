# GNI TARGET + WORKING ORDER
**SESSION-NUMBERED BY DESIGN (Protocol v4+).** This file ships and lands as
`docs/GNI_TARGET_AND_ORDER_S87.md`. **THE LIVE ORDER IS THE HIGHEST SESSION NUMBER.**

GENERATION 7 · 2026-08-29 · supersedes `GNI_TARGET_AND_ORDER_S86.md` (generation 6).
Regenerated, never appended. HEAD at close: `30020a9`.

---

## NEXT SESSION'S MISSION (S88)

**SHIP 8.6 — PUBLISH THE UNCAPPED MAGNITUDE — THEN 8.7 (POLARITY).**

| item | what "done" looks like |
|------|------------------------|
| 8.6 | one run writes `raw_score` to a place a reader can see, and the public surface shows magnitude beside the level |
| 8.7 | `ceasefire` no longer scores as escalation; the direction-neutral audit of all three lists is written down |

**LINEAGE-BEV IS PRE-PAID FOR BOTH.** S87 measured 192 runs with the real scorer
(`tools/replay_scorer.py`, `tools/design_bench.py`). Production writes `raw_score 19` and
publishes `10`. Uncapped range across the corpus is 10.3–26.8, median 19.2; every published
value is 10.0. `factors` on the live row reads "Geo signals: war, attack, sanction" — three
background words at 100%/94%/74% firing, no rupture word among them.

**DO NOT RE-OPEN THE RECALIBRATION.** DECISION S87-2 closed it with measurement, not opinion.
Three designs are in the graveyard and `tools/design_bench.py` re-proves them on every run.
Before proposing any scorer design, RUN THE BENCH. Reading about the graveyard is optional;
running it is not.

---

## TARGET (unchanged — no phase transition this close)

**TRUTHFULNESS OF OUTPUT.** What GNI says must be what GNI measured.

**DEFINITION OF DONE — status at this regeneration:**
- the arbitrator reads what it claims to read — ROOT 1 CERTIFIED, 1.11 open
- the grounding gate measures reading, not existence — ROOT 7 OPEN
- the escalation score carries information — **ROOT 8: half-answered.** The instrument is
  proven saturated by measurement, the level is proven unfixable inside this corpus, and the
  information is proven to EXIST in the uncapped magnitude. Publishing it is the open half.
- the public surface matches the configuration — ROOT 9 OPEN

---

## THE CROSS-ROOT DIAGNOSIS (new this close — not a new root; it names three existing ones)

> **GNI repeatedly measures what it has already guaranteed itself, and publishes the result as
> a fact about the world.**

| instance | what is measured | what it actually is |
|---|---|---|
| ROOT 7 | "the span exists in the pool" | reported as "the agent read it" |
| 8.1b | `_high_escalation` True 6/6 | a crisis channel that cannot leave crisis mode |
| 8.1 (new) | `diversity_bonus` = 3.0 in 175/191 | the S39 funnel quota (14/4/4) guarantees all three pillars |

This is recorded as a diagnosis, not a work item: its instances are already ranked. Its use is
predictive — when a metric is >90% constant, ask WHO GUARANTEED IT before tuning it.

---

## THE ORDER

### ROOT 8 — GNI PUBLISHES A SATURATED INSTRUMENT AS A MEASUREMENT OF THE WORLD · URGENT · **TOP**

**8.1 CLOSED (S86) — the audit.** Saturation across three layers, confirmed by bytes.
**8.1a** OPEN — D-11's feeds list misses three consumers: arb prompt L989, `nexus_analyzer:567`,
  `self_bias_gate:46`. Unchanged this close.
**8.1b** OPEN — NN-5 is a deliberate hard-correction channel (`1da3dfe`) whose switch is stuck.
  **S87 note:** since no recalibration is coming, the switch stays stuck by design decision, not
  by neglect. This raises 8.5's rank rather than lowering it.
**8.1c** OPEN and GROWING — `constraint=1092` of `ctx_room=4762` on `33180919784` (was 987/5091
  at S86): ~19% → ~23% of arbitrator context spent by an always-on branch, ~8–9 articles.
**8.2 CLOSED (S87) — CERTIFIED 4/4.** `4b220ab` merges all five unpublished scorer fields into
  `report`. Row `2026-08-28 21:13:16Z` returned `base_total 14 · diversity_bonus 3 · combo_bonus 2
  · raw_score 19 · final_score 10 · gate_applied null`, and the pre-commit row is null on all of
  them. Every pre-registered prediction met.
**8.3 RULED (S87) — NO RECALIBRATION OF THE LEVEL.** See DECISION S87-2. Three designs falsified
  on n=192. The item is closed as a design question and replaced by 8.6 + 8.7.
- **8.4** OPEN, RE-WORDED BY EVIDENCE. The public caveat is no longer "the instrument is broken"
  — that would attach a false exoneration to a correct alarm. It is: *the score is capped at 10
  and has been at the cap on every run since measurement began; magnitude is published beside it.*
  Cheaper than any recalibration and true under both readings of the corpus. Gated on 8.6.
- **8.5** OPEN, **RANK RAISED.** Exercise `_high_escalation == False` once, deliberately. S87
  removed the only path by which this branch would ever have fired on its own. It is untested
  code that now has no natural trigger; the selftest fixture hardcodes CRITICAL.
- **8.6** **NEXT.** Publish the uncapped magnitude. `raw_score` already reaches `full_analysis`
  as of `4b220ab`; what remains is a reader — a column, or the public surface, or both. Smallest
  change that restores 2.6× of destroyed resolution without touching a single threshold.
- **8.7** **NEW.** Polarity. `ceasefire` is in `GEO_SIGNALS` and scores +1.0 as escalation; it
  fires in 50.3% of runs. `sanction`, `troops`, `naval`, `dollar`, `gold`, `treasury` are
  direction-neutral or safe-haven terms counted as danger. One-line fix for `ceasefire`; the
  audit of the rest is the real item.
- **8.8** **NEW.** 19 keywords never fire in 192 runs — GEO 1 (`invasion`), TECH 3, **FIN 15**
  (`market crash`, `bank run`, `banking crisis`, `credit crunch`, `debt default`,
  `hyperinflation`, `liquidity crisis`, …). **DO NOT DELETE THEM** — they are the crisis
  vocabulary, and their silence is the finding: the financial system has not broken once in this
  window, so FIN's pillar activation is carried entirely by background words. Absence is
  evidence (Protocol v7 step 8h).

### ROOT 1 — THE ARBITRATOR'S INTAKE · CERTIFIED, NOW CLOSING (1.11 excepted)
- **1.11** **URGENT, TRIGGER FIRED (S86).** S87 adds a third boundary sample: `33180919784`
  `assembled=41` → `ctx-trim@4762`, `truncated=1`, `dropped=4`. With S86's 39 (no cut) and 43
  (cut), the ladder boundary is now pinned **between 39 and 41**, not "~40" by inference. The
  pillar re-rank trigger did NOT fire: lowest pillar TECH 8/11 = 73%, above the 50% threshold.
- **1.6** OPEN, confirmed 14/14 + 4/4 + 2/2. Unchanged.
- **1.7** OPEN — still needs one `truncated=0` run. S87 reproduced the partial-line inflation a
  third time in the same direction (pillar sum 38 vs `arrived` 37, `truncated=1`). See R-S87-7.
- **1.8** OPEN, unchanged — `bool(mad_bull_case)` may still leak success past the veto; read
  L275-295.
- **1.9** DE-RANKED, unchanged.
- **1.12** OPEN, unchanged — `GROQ_MODEL_FALLBACK` reaches no workflow. **Do not wire it before
  reading its value.**
- **1.13** **NEW — ROOT 1 × ROOT 8 INTERSECT.** TECH is starved in two layers independently:
  the funnel gives it 4 of 22 articles and it fires a median of 2 signals of 25 (`design_bench`),
  while in the arbitrator ladder it is the pillar that dies first (`TECH:0` at depths 100/50/20,
  restored only at depth=0). Chip and export-control coverage is structurally thin on both sides.
  Neither root's owner has looked at the other's evidence.
- **1.1 / 1.2 / 1.3 / 1.4 / 1.5 / 1.10** CLOSED in earlier sessions.

### ROOT 7 — THE GROUNDING GATE MEASURES "EXISTS IN THE POOL", NOT "WAS READ" · URGENT
- **7.1** PARTLY PAID (S86). `checked_spans` is computed and discarded at the print — the RATE
  denominator exists. Now a named instance of R-S87-7.
- **7.2** Decide the fix shape. Unchanged.
- **7.3** PARTLY DISCHARGED (S86). Unchanged.
- **7.4** OPEN — per-run line counts dialect IN, digest and `hit_count` exclude it. Confirmed
  again at S87: watch run `33116197492` printed 113/117 while per-run debate hits were 8. Never
  compare them. Now a named instance of R-S87-7.

### ROOT 9 — PUBLIC COPY DRIFTS FROM CONFIGURATION · IMPORTANT
- **9.3** OPEN — "4 pipelines" wrong in six places.
- **9.4** OPEN — `stock-context/route.ts:81` defaults to a dead model. Pairs with 2.4.
- **9.5** OPEN — eight unresolved S69 census flags; F14 (`/comparison` renders BEARISH over a
  NEUTRAL verdict) is the ugly one. RE-CERT never ran.
- **9.6** OPEN — three ID schemes in the register. S87 hit this from the other side: see 5.6.

### ROOT 6 — FREE-TIER RESOURCES COME WITHOUT THE GUARANTEES AROUND THEM · IMPORTANT
- **6.5** **THERE IS NO BACKUP.** Unchanged and still true.
- **6.2** Retention policy. Promoted at generation 3 (S86); unchanged this close.
- **6.3** SIZE METER in Mission Control. Unchanged.
- **6.4** L5 exposure when Supabase 402s. Gates 6.2.
- **6.6** **NEW.** `information_schema` shows `lens_macro_reports`, `lens_predictions`,
  `lens_s4_alert_state`, `lens_tiercd_data` in the SAME Supabase project. Project Lens shares
  GNI's 500 MB. Every runway figure quoted in 6.2/6.5 (113/500 MB, 520–660 days) silently
  includes another system's growth curve, which GNI does not control and does not measure.
- **6.1** CLOSED (S84).

### ROOT 2 — LABEL COVERAGE IS NARROWER THAN THE FABRICATION SURFACE · IMPORTANT
- **2.1** HALF-RULED (S86) — trigger B does not fire on clause 1. Clause 2 unmeasured; that is
  the only thing keeping 2.1 open.
- **2.2** Build B only if 2.1's second clause triggers it.
- **2.3** **NARROWED BY MEASUREMENT (S87) — two external explanations eliminated.** The verdict
  slide is monotonic (bearish 94→57→28→17%, conf 0.794→0.549) while escalation is not: replayed
  monthly medians are 15.1 / 12.1 / 12.9 / 14.1 with rupture-hit median flat at 4 and combo
  median RISING 5→7 in August. Tension went UP in August while bearishness went DOWN. Therefore
  neither "the world calmed" nor "the signal weakened" survives. Remaining candidates are all
  INTERNAL: article mix, prompt growth, corpus drift, and agent habituation to a constant crisis
  vocabulary. The search space is halved; the item stays open.
- **2.4** `/stocks` may render frozen prices. One grep settles it.

### ROOT 3 — FALLBACK-ERA CONTAMINATION IN THE EVIDENCE BASE · IMPORTANT
- **3.1** WIDENED (S86) — `conf = 0.5` exactly: Jun 11, Jul 7. Contamination is wider than the
  Jul 19–22 window.
- **3.2** `data_era` column + tagging. Unchanged.

### ROOT 4 — COST AND HEADROOM · IMPORTANT
- **4.5** **STILL UNREAD SINCE JUL 27** — C1's real token bill. The `groq_quota` TELEGRAM line.
- **4.1** C2 solver recalibration. `ctx-trim` fired again at S87 (`@4762`), so not dormant.
- **4.4** Measure chars/token PER POSITION. `//3` is SAFE; do not move to `//4`.
- **4.3** Groq TPD refills continuously.
- **4.2** CLOSED AS ACCEPTED (S86).

### ROOT 5 — INSTITUTIONAL HARDENING · BELOW THE LINE
- **5.5** `DEBT_REGISTER_S69.md` has no reader. Unchanged.
- **5.6** **NEW.** `GNI_RULES.md` is now **52,174 bytes** — the largest artifact in the close set
  and ~41% of the session's opening read, and no session reads it end to end; it is cited by ID.
  It grows ~6 rules per close. The register that exists to prevent repeated failures is becoming
  the least-read document. Pairs with 9.6 (three ID schemes inside it).
- **5.7** **NEW.** Seven columns in `reports` are never written by `supabase_saver`:
  `mad_grounding_hits` (jsonb — ROOT 7's natural home), `escalation_score_lower/upper`,
  `debate_summary`, `agent_positions`, `key_disagreements`, `consensus_path`. Dead schema is a
  standing invitation to assume a field is populated. Census method is in the S87 record.

### LIFECYCLE + SECURITY — target-independent, deadline-driven, never ranked away
Unchanged from generation 6.

### RETIRE CANDIDATES — the clause, honestly counted
- **1.9** — de-ranked at generation 5, unworked since. Generation 2 of 3. Not yet due.
- **4.4** — unworked three generations. **PROMOTED with a written reason:** `//3` is the safe
  side of a live estimate that gates 4.1; closing it as accepted would silently bless a number
  nobody has measured per position.
- No item is dropped silently this close.

---

## CHANGED THIS REGENERATION

**MISSION: COMPLETED.** S87's declared mission was "ship 8.2 (`score_breakdown` persistence),
then SWOT 8.3 having READ the March-24 design first". 8.2 shipped as `4b220ab` and certified
4/4 against pre-registered predictions. 8.3's SWOT was run twice from opposite premises, on
measured data, and produced a ruling rather than a preference.

**CLOSED:** 8.2 (certified) · 8.3 (ruled — replaced by 8.6 + 8.7) · three traps disposed.

**NARROWED:** 2.3 (two external explanations eliminated by replay) · 1.11 (boundary pinned to
39–41 by a third sample) · 1.7 (third reproduction of the partial-line inflation).

**NEW:** 8.6 (publish magnitude) · 8.7 (polarity) · 8.8 (19 silent keywords) · 1.13 (TECH
starved in two layers) · 6.6 (Lens shares the Supabase project) · 5.6 (the register nobody
reads) · 5.7 (seven dead columns) · the cross-root diagnosis.

**RE-RANKED: ROOT 8 KEEPS THE TOP SLOT.** 1.11's numeric re-rank trigger was evaluated against
`33180919784` and did NOT fire (TECH 8/11 = 73%, threshold 50%). ROOT 8 is the only root whose
defect is currently visible to the public every single run.

**DECISION S87-1 — 8.2 ships as a five-field merge in `main.py`, not a schema change.** Chosen
over (B) a new `score_breakdown jsonb` column and (C) editing the scorer to store untruncated
hits. Reason: `full_analysis` already accepts arbitrary report fields with zero migration
(`0530e1c`, 2026-03-27), `src/` greps to zero readers, and the schema already carries seven dead
columns (5.7) — adding an eighth with no reader repeats the defect. Widened from the order's one
named field to all five unpublished fields under R-S82-2. `LINEAGE:` line carried.

**DECISION S87-2 — NO RECALIBRATION OF THE ESCALATION LEVEL.** Chosen over the March-24 Fix-2
design and over Claude's own rupture-tier proposal. Reason, in measurement: replayed across 192
stored runs, Fix-2 gives 192/192 = 10.0 (identical to production), an actor-word tier changes 0
runs, and a rupture-word tier still gives 187/192 CRITICAL. All three fail for one reason — an
absolute threshold cannot measure a set the funnel already pre-selected (R-S87-1) — and the
corpus contains no pre-crisis regime from which any replacement constant could be derived
(R-S87-3). James's premise was the load-bearing one: the world has been bad since February, so
pulling the number down would manufacture false calm. **CRITICAL stays CRITICAL.**

**DECISION S87-3 — the fix is to publish the uncapped MAGNITUDE, level untouched.** The correct
diagnosis is loss of resolution, not excess severity: uncapped 10.3–26.8 compressed onto a
single published 10.0 (R-S87-2). This is the one repair both readings of the corpus agree on —
it satisfies "the instrument is saturated" and "the instrument is right and the world is bad"
simultaneously, which is why it survived the double SWOT.

**DECISION S87-4 — the findings are shipped as TOOLS, not as prose.** `tools/replay_scorer.py`
(`31c1906`) and `tools/design_bench.py` (`30020a9`). Reason: the March-24 design survived five
sessions inside the written record, read but not tested; it died in one command. `design_bench`
recomputes its graveyard on every run rather than banking the numbers, and prints the
pre-selected-set and no-baseline warnings automatically. A rule stored where the failure happens
costs the next session zero tokens and cannot go stale.

**DECISION S87-5 — PROTOCOL v7, NOT CONTRACT v8.** PART D gains step 8, ANALYTICAL STANCE
(a–h); the old step 8 becomes 9. It is deliberately NOT a persona: a role title makes assertion
feel earned, and confident recall is what hallucination looks like from the inside. This is how
a session reasons, which is PART D's subject, not a rule of engagement. CONTRACT stays v7 —
carry `CONTRACT_S85.md` forward unchanged.

**DECISION S87-6 (Claude's lean, PENDING JAMES'S WORD — precedent M4) — the `BLOCKER:` field.**
Every item in THIS FILE that claims work is blocked must name the measurement that established
the block, or be marked `ASSERTED, UNTESTED`. An `UNTESTED` blocker may not stop work. Reason:
"nothing about ROOT 8 is provable by SQL until `score_breakdown` is stored" was written at S74,
copied through S85 and S86 unchallenged, and was false — a five-minute read-only replay was
available from June onward. Adopted in the ORDER (where queue items live), not in CONTRACT,
because CONTRACT reached v7 in six weeks and the law-vs-state test applies to its version log.

**TRAP DISPOSITION (promote or expire, no trap rides forward unchanged twice):**
- `_arb_asm` denominator — SECOND CARRY → **PROMOTED as R-S87-7**, merged with 7.1's
  `checked_spans` and 7.4's two counters: one defect, three instances.
- MSYS `grep --include` — SECOND CARRY → **PROMOTED as R-S87-5(b)**, together with the new
  heredoc path bite found this session.
- MAD schedule moved ~9.5h, cause unknown — **PROMOTED as R-S87-6 and RETIRED as a trap.** It
  was never an event: measured over 133 scheduled runs, lateness is a property of the free tier
  that has been IMPROVING (median 243 → 177 → 61 min), with zero runs missed in 67 days, and
  `b27474e` (2026-06-22) already names the cause in its own subject line.
- NEW TRAP (first carry): pipeline↔MAD spacing is designed at 30 minutes and measured at 13 on
  2026-08-28 (14:22 vs 14:35). Both jobs drift independently, so the order can invert and MAD
  would debate a stale article set with no error raised. Expires when measured over 14 days or
  when a spacing guard lands.

**DOCS SHIPPED THIS CLOSE:** this order (generation 7) · `HANDOFF_S87.md` ·
`GNI_RULES_S87.md` (+ R-S87-1..7) · `GNI_Session_Transfer_Protocol_S87.md` (v7).
CONTRACT unchanged at v7 — carry `CONTRACT_S85.md`.

**ITEM UNIQUENESS — expected 43 distinct item IDs, with exactly two intentional repeats.**
The count was asserted at 42 before the grep and the grep returned 43; the miss is logged in the
wrongness ledger. `1.9` and `4.4` appear twice BY DESIGN — once in THE ORDER and once under
RETIRE CANDIDATES, which is the retire clause showing its working. `8.1`, `8.2` and `8.3` carry
their status inside the bold and so do not match the ID pattern. Verify:
`grep -oE '\*\*[0-9]+\.[0-9]+[a-c]?\*\*' docs/GNI_TARGET_AND_ORDER_S87.md | sort | uniq -d`
must print ONLY `**1.9**` and `**4.4**`, and `... | sort -u | wc -l` must print 43.

---

## HOW THIS FILE IS MAINTAINED
Regenerated at every close, dated, superseding. Never appended. One mission per session, taken
from the top. Decisions live here as DECISION lines — GNI mints no separate D-register.
FRESHNESS CONFERS NO PRIORITY.
