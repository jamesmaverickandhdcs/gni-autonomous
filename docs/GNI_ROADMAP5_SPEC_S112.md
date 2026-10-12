# ROADMAP 5 - FREEDOM FROM FEAR, MEASURED - SPECIFICATION (S112)

**Status:** SPECIFIED at S112, written before anything is built. The operator ruled "A + C" at S112
(DECISION S112-5, recorded at the close): bring the founding philosophy into the promise ledger (A,
done at R11 - `docs/GNI_PHILOSOPHY_S112.md`, CLM-1106..CLM-1133) and declare this roadmap (C). The
declaration itself, with its place in ARCHITECTURE and the order, is made at the S112 close.

**Target, unchanged:** TRUTHFULNESS OF OUTPUT. **Roadmap 5 in one line:** what GNI's founding documents
say every output is measured against - Freedom from Fear and its Teenager Standard - is measured, by a
check that goes red on an output that fails it, and the measure is itself checked against people.

## 1. WHY THIS ROADMAP, FROM THE LEDGER

NN-PHI-1 says "All output is measured against the Teenager Standard, not against financial prediction
accuracy." At R11 the ledger grades it **NOT BUILT**, and the reverse holds: the one measure of outputs
GNI runs is market accuracy on SPY (GPVS). The rows that carry the standard:

| claim | rule | ledger at R11 |
|---|---|---|
| CLM-1108 | Freedom from Fear is the foundational standard against which all outputs are measured | NOT BUILT |
| CLM-1109 | T1 - can a teenager understand what is happening | PARTIAL - asked of the LLM, not measured |
| CLM-1110 | T2 - why it matters to people's lives | PARTIAL - asked, not measured |
| CLM-1111 / CLM-1125 | T3 / NN-PHI-4 - every threat has a path | PARTIAL - the parser accepts an empty path |
| CLM-1112 | T4 - fear without understanding is rejected or reframed | NOT BUILT |
| CLM-1113 | T5 - identity division is rejected | PARTIAL - inputs screened, outputs not |
| CLM-1122 | NN-PHI-1 - measured against the Teenager Standard | NOT BUILT |
| CLM-1124 | NN-PHI-3 - no manipulation technique in GNI's own output | NOT BUILT |

Roadmaps 2-4 built instruments around what GNI says about itself. This one turns them on what GNI says
to its reader.

## 2. THE GUIDELINES IT FOLLOWS (found before the design, read at their sources)

- **UN General Assembly resolution 66/290 (10 September 2012), paragraph 3:** "All individuals, in
  particular vulnerable people, are entitled to freedom from fear and freedom from want", and human
  security "calls for people-centred, comprehensive, context-specific and prevention-oriented responses
  that strengthen the protection and empowerment of all people". PHI-003 says Freedom from Fear "is not
  a political concept. It is a human development concept" - the same people-centred reading. The
  empowerment clause is NN-PHI-4's "every threat must have a path".
- **ISO 24495-1:2023 (plain language, governing principles):** readers get what they need (relevant),
  can easily find it (findable), understand it (understandable) and use it (usable). Teenager Standard
  T1 is "understandable", T2 "relevant", T3 "usable". Only the four principles as published by the
  International Plain Language Federation are relied on; no clause is cited.
- **Solutions journalism (Solutions Journalism Network):** "rigorous and compelling reporting about
  responses to social problems" - a response, insight, evidence, and its limitations. This is the
  discipline that keeps NN-PHI-4's path from becoming the "false comfort or forced optimism" PHI-003
  forbids: a path names a real response and says what it cannot do.
- **NIST AI RMF MEASURE 2.13:** "Effectiveness of the employed TEVV metrics and processes in the measure
  function are evaluated and documented." Machine proxies for a human standard are only trusted after
  they are checked against human judgement (row R5-3).
- **ICD 203 tradecraft standards 2 and 5:** uncertainties expressed and explained; customer relevance
  and implications addressed - the analyst's version of T2 and T3.

## 3. THE FOUR ROWS

Each row is answered by bytes; checks are named by function, never by number.

| row | build | DONE when, from bytes |
|---|---|---|
| **R5-1** SAMPLE | a dated, closed window of published outputs (each report's fff_what_is_happening, fff_honest_analysis, fff_human_path and summary) harvested by the DB snapshot pattern of S112 - one read-only query in the tree, its md5 in the snapshot, the operator's cell copied unaltered | `docs/gni_output_sample_S<N>.json` exists, its `query_md5` matches its query file, and it holds every report of its window (the row count is in the cell) |
| **R5-2** MACHINE MEASURES | fitness functions over the sample, one per rule that a machine can read: T1 a readability grade of fff_what_is_happening and a market-jargon count; T3/NN-PHI-4 a path present and not one of the generic phrases the prompt itself bans; T4/T5/NN-PHI-3 the PHI-003 rhetoric patterns the funnel already runs on inputs, run on GNI's own output. Thresholds are the operator's DECISION, written before the first measurement | CLM-1109, 1111, 1112, 1113, 1124, 1125 each bound to a fitness function; each has a failure test on a copy (a sample with one failing output turns its claim DEFEATED) |
| **R5-3** PEOPLE CHECK THE PROXIES | a review file `docs/GNI_FFF_REVIEW_S<N>.tsv`: a reader outside the build rates a stated number of sampled outputs on the five Teenager Standard questions; the machine measures are compared with the ratings (MEASURE 2.13) | the file holds the ratings with date and reader role; an agreement figure per measure is published beside the measure, computed by a tool, and a measure that disagrees with people is marked as such, not used to grade |
| **R5-4** GATE ON OUTPUT | before a report is saved and before a Telegram message is sent, the R5-2 checks run on GNI's own text; a failure is annotated on the report, sent to the operator and written to the audit trail. It does not block the run: NN-1 keeps the sacred pipeline unblockable, and NN-PHI-2 forbids suppressing news | a check labelled `output gate wired` finds the gate on both paths; a failure test sends one manipulative output through and finds the annotation and the audit entry |

## 4. COMPLETION TEST

**Test 1 - the ledger moved.** Of the eight rows in section 1, every one is BUILT or PARTIAL with a
measure, and none is NOT BUILT; read from `docs/GNI_PROMISE_LEDGER_S<N>.tsv` by its claim ids.

**Test 2 - the operator's verdict.** The operator reads ten sampled outputs beside their measures and
answers one question: *does a teenager reading these come away understanding, not afraid?* The verdict
is the operator's and is not delegated to the session that built the measures (as R-S110-3 requires
of roadmap 4). One line in ORIGIN: `FFF-TEST <date> S<n> PASS|FAIL -- <reason>`.

**ACHIEVED** = four rows DONE + Test 1 + Test 2 PASS, dated in ORIGIN. If not achieved, the reason is
written down.

## 5. OWED BEFORE THE ROW THAT NEEDS IT (the operator's rulings)

| owed | needed by | why |
|---|---|---|
| the sample window and its size | R5-1 | a dated window keeps the sample from going stale (DECISION S90-3, S112-4) |
| the readability threshold and the jargon list | R5-2 | a threshold typed after the measurement is a status typed by hand |
| who the outside reader is | R5-3 | the builder grading its own proxies is the self-grading roadmap 4 refused |
| annotate-and-alert, or hold-for-review | R5-4 | blocking conflicts with NN-1 and NN-PHI-2; this spec leans to annotate-and-alert |

## 6. WHAT IT CANNOT DO (written down, not discovered later)

- A readability grade measures sentence and word length, not understanding; it is a proxy, and R5-3
  exists because of that.
- The rhetoric patterns find the techniques they name; a new technique passes until it is named.
- It measures the text GNI writes, not what a reader does with it.

## 7. SEQUENCING

Roadmap 4's Test 2 first (S113 open): the ledger now holds the founding philosophy, so the answer to
"how much of what GNI set out to be is built?" can quote values, not only features. Then R5-1, whose
query is written and reviewed before it is run.
