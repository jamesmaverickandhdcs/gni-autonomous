# GNI ROADMAP 3 — SPECIFICATION
**WRITTEN AT THE S102 CLOSE, 2026-09-08. NOT YET COMMITTED AS A ROADMAP — that is James's
declaration to make (DECISION S93-2's precedent: the roadmap is HIS, not a prior session's
suggestion). This file is the proposal plus the measurements taken to size it.**

Read with `docs/GNI_ORIGIN.md` (to be written at R3-1) and `docs/GNI_ARCHITECTURE_S102.md` §4
(DECISION S92-3, the six disciplines).

---

## 0. WHY THIS EXISTS — the five steps, as James told them

This is the account that must survive into `GNI_ORIGIN.md`. It is written in the PAST TENSE on
purpose: a record of what happened does not rot, a description of the present does.

1. **BUILT.** GNI's original vision, mission and philosophy were built and operated. This part
   worked.
2. **ADDED.** More thinking was layered on — measurement, evaluation, the 7-layer defense
   designed at S53.
3. **CHECKED, AND IT STOPPED BEING SMOOTH.** Going back to ask whether the added layers were
   actually WIRED produced the first bad answers. S69 (Jul 15) found `prompt_injection_detector.py`
   — 70 patterns — imported by nothing since March, a failed wiring attempt, a fallback
   substitution, no debt record, and the item marked DONE. The same session found three of the
   seven declared defense layers existed only on paper.
4. **THE FLOOR GAVE WAY.** Checking whether the Web App sub-pages matched what the backend
   computed opened a hole with no bottom. From that point nobody could say where the work stood.
5. **WHACK-A-MOLE, UNTIL S92.** Every fix surfaced more. At S92 three different questions in one
   session all returned the same answer — *we cannot tell you*: why does this keyfile task exist
   (no origin recoverable across 11 order generations); is SUBPAGE-IC done (five months, renamed
   three times, deadline missed by 30 days, no live document pointed at its ledger, and the
   answer to "when will it finish" was **never**); and is the assistant's own report reliable
   (three of its claims died that day). James proposed a full rewrite. The rewrite was refused
   because the CODE was right — what had failed was the ability to SEE it from outside.

**The mechanism behind all of it, stated once:** this system has no protection against work
disappearing without a declaration. Every other path is guarded — a wrong fix goes red, a wrong
number is caught, a wrong rule id is grepped. An arc that quietly stops being referenced leaves
no trace and triggers nothing. GNI's own rule (`GNI_RULES_S91.md:760`) covers closing an arc
without declaring ACHIEVED; SUBPAGE-IC was RENAMED, and renaming is not closing, so the rule
never fired.

**And the deeper one, which is why this roadmap is about claims and not documents:** the layers
were added faster than they were verified as wired. Once verification began, the backlog of
never-checked surface was discovered faster than it could be fixed. Whack-a-mole is therefore not
bad luck; it is the arithmetic of unverified accumulation.

---

## 1. RECON — measured 2026-09-08, before committing to anything

Two of the three assumptions this plan was built on turned out to be WRONG. Recorded here so the
plan is sized against measurement rather than belief.

| # | question | command | RESULT |
|---|---|---|---|
| 1 | how many public pages / claim-shaped lines? | `ls src/app/**/page.tsx src/app/*/page.tsx \| wc -l` + grep | **60 pages, 70 candidate lines** |
| 2 | is DET-DEAD still dead? | `grep -rn "prompt_injection_detector" ai_engine/ --include=*.py` | **EMPTY — STILL DEAD. NINE MONTHS.** |
| 3 | is the 7-layer overclaim still published? | `grep -rn "7-layer\|seven.layer" src/ docs/` | **`src/` = 0 hits. FIXED AT S77.** |

### What the reversal means — this is the most important paragraph in this file

The prose defect and the code defect were found on the SAME DAY (S69, Jul 15). The prose defect
was FIXED four months ago (`HANDOFF_S77.md:24` — *"D-2 CLOSED: methodology 7-layer -> real stack;
tree grep = 0"*, with a SWOT verdict of *3 live / 3 mislocated / 1 ghost*). The code defect has
never been fixed and is still dead today.

> **Prose has a reader. Code does not.** A wrong sentence gets read, recognised and corrected. A
> dead module is read by nobody, so nine months pass. **The dead-symbol gate is the first
> continuous reader `ai_engine/` will ever have.**

This reversal also re-ranks the work: `C10` (dead-symbol) is not a nice-to-have that mirrors an
already-solved problem. It addresses the half of the S69 finding that was never closed.

### Recon still owed before R3-2 is sized

- Of the 60 pages, how many make a CLAIM as opposed to rendering data? The 70-line grep is a
  candidate set, not an answer. Sizing R3-2 needs the real count.
- What is in the March 2026 white paper, and where does it live (repo / drive / site)? Claims
  sourced there cannot be harvested by a tool until the file is located.

---

## 2. THE ARTEFACTS

| file | who writes it | why |
|---|---|---|
| `docs/GNI_ORIGIN.md` | human, append-only, PAST TENSE only | the five steps. Never regenerated. A record of the past cannot go stale; a description of the present always does. |
| `docs/GNI_GLOSSARY_S<N>.md` | human for names, DERIVED for check/metric rows | six groups: id namespaces (`GNI-R-###`, `R-S##-#`, `GNI-L-###`, `C#`, `#.#`, `S##`) · session index · checks · defect names (DET-DEAD, DEGRADE-SILENT, SUBPAGE-IC) · procedures (BEV, LOAD CHECK, cert, fixture family, control probe) · metrics (rho, lambda, mu, Z, COVERAGE) |
| `docs/GNI_CLAIMS_S<N>.md` | claim text human + append-only; **STATUS DERIVED, never typed** | every promise GNI makes about itself, its source `file:line`, its fitness function or an explicit `UNMEASURED` |

**Hard rule for the claims file:** `C5` already forbids a check from carrying a hand-written
expected integer. The same rule applies here — **no status may be typed by a human.** A status
column filled in by hand is the S98 completion-test table again, and that one was wrong for four
closes.

---

## 3. THE FOUR ROWS

Each row states its completion test BEFORE the work, per the policy adopted at the S96 close.

### R3-1 · GLOSSARY + ORIGIN

- **Build:** both files above. `C8` = every abbreviation used by a live document exists in the
  glossary; every ORIGIN citation resolves to a real session record or commit.
- **Why this is not a new tool:** `C8` is `C1` generalised. `C1` says *every id cited by a live
  document must exist in the register*. `C8` says *every abbreviation used by a live document must
  exist in the glossary*. Same shape, same file, one more check.
- **Measure:** glossary entry count; ORIGIN citation count.
- **Fixture:** introduce an undefined abbreviation -> RED. Break one ORIGIN citation -> RED.
- **DONE:** CI green, and the LOAD CHECK points at both files.

### R3-2 · CLAIMS HARVEST — this ABSORBS order item 9.21

- **Build:** `tools/gni_claims.py` extracts every claim from `src/app/**/page.tsx` and the white
  paper, verbatim, with `file:line`, into `GNI_CLAIMS_S<N>.md`.
- **Method note, learned the hard way at this close:** harvest from the REPO, not from the
  rendered website. The site is not in search indexes and a browser read dies the moment it is
  taken. The pages are in git; a tool can re-read them; a check can go red.
- **9.21 is not a separate item.** Reading what the public pages say IS reading what GNI promises.
  Splitting one job across two homes is how one of them dies.
- **Measure:** claim count, verified by TWO differently-shaped counting commands that must agree,
  in the pattern the order file already uses.
- **Cert:** add a claim to a page -> count rises; remove it -> count falls.
- **DONE:** every claim has a resolving `file:line`. A claim with no source is not a claim, it is
  an assumption.

### R3-3 · STATUS + FITNESS FUNCTIONS

- **Build:** bind each claim to a fitness function or declare `UNMEASURED` explicitly.
  `C9` = declared-layer count vs wired-layer count. `C10` = dead-symbol gate.
- **Vocabulary, and it is not ours:** *Building Evolutionary Architectures* (Ford, Parsons, Kua)
  defines an architectural fitness function as **any mechanism performing an objective integrity
  assessment of some architecture characteristic**, implemented as tests, metrics, monitors or
  logs, and used to protect those characteristics automatically and continually. **`C1`-`C7` are
  already fitness functions.** What is missing is that all seven measure the repo's INTERNAL
  consistency and none measures what GNI PROMISED.
- **Measure:** `COVERAGE = claims with a fitness function / total claims`, published the way the
  macro map publishes `Z`.
- **Cert:** flip one claim from wired to unwired -> the verdict must flip. If it does not, the
  whole apparatus is decoration. (This close proved the danger: sixteen fixture families passed on
  a branch none of them had ever entered.)
- **DONE:** no blank statuses; COVERAGE published.
- **Consequence, and it is why the code pile is not a separate problem:** the 28 modules `§5`
  reports with no static reference sort themselves into three buckets — *serves a claim, not
  wired* (WIRE IT), *serves no claim* (DELETE, git remembers), *tooling* (DECLARE). **Deletion
  stops being a judgement call and becomes a derivation.**
  Established practice supports this: the strangler-fig pattern is for high-stakes, high-traffic
  systems, and using it on low-stakes code is overkill and demoralising; dead code has zero
  traffic by definition. The Mikado Method builds a dependency graph, and this graph is empty. A
  "to be removed" backlog is exactly what `SUBPAGE_CERTIFICATION.md` was.

### R3-4 · BIND — the queue to the claims

- **Build:** every order item carries a claim id. An item with no parent is out of bounds.
- **Measure:** ORPHAN RATE, and **lambda re-measured over the two closes after binding**.
- **Falsifiable prediction, written before the work:** binding discovery to a finite list of
  claims should make lambda FALL from its current ~6.5 per session. **If it does not fall, the
  diagnosis in section 0 is wrong and must be revised rather than defended.**
- **DONE:** ORPHAN RATE published and derived, in the same manner `C7` derives its bound.

---

## 4. COMPLETION TEST — for the roadmap, not for a row

### Test 1 — HISTORICAL REPLAY

Three defects that actually happened. They cannot be invented, which is what makes them stronger
evidence than any fixture we could write.

| defect | occurred | found | how found | check that should catch it |
|---|---|---|---|---|
| three paper layers | S53 (Mar) | S69 (Jul) | by accident | `C9` |
| DET-DEAD | Mar | S69 (Jul) | by accident | `C10` |
| SUBPAGE-IC renamed, orphaned | S85 | S92 | James asked | BIND |

Method: check out the tree at each era and run the new checks against it. **At least 2 of 3 must
go RED.** A red result yields a number — *nine months to nine seconds*. A green result means the
tool is decoration, and knowing that immediately is the point.

### Test 2 — THE AGENT TEST

> **A new agent must be able to answer "why are we doing Smart Office?" WITHOUT searching chat
> history.**

Baseline, recorded honestly: at the S102 close the assistant failed this twice — it could not
answer from the documents, and when it reconstructed an answer from the records it got the answer
WRONG on the first attempt, proposing "so we can answer *when will it be done* with a number"
when the actual account is the five steps in section 0.

### ACHIEVED

**4 of 4 rows + REPLAY >= 2 of 3 + AGENT TEST passed -> ROADMAP 3 ACHIEVED, dated, written into
`GNI_ORIGIN.md`.** If not achieved, the reason is written down. **Nothing in this roadmap may end
the way SUBPAGE-IC ended.**

---

## 5. SEQUENCING — proposed, James rules

| session | work |
|---|---|
| **S103** | order item **5.50** (`C6` reads BOTH macro-map INPUT lines). This makes roadmap 2 **4 of 4** and it is **DECLARED ACHIEVED**. Then the remaining recon. |
| **S104** | James commits (or declines) roadmap 3 against the recon numbers. R3-1. |
| **S105+** | R3-2 -> R3-3 -> R3-4. Recon-1's real count decides how many sessions R3-2 needs. |

**Why S103 must finish roadmap 2 first:** this project has never once seen an arc run to
completion. Roadmap 2 stands at 3 of 4 with one session of work left. Starting roadmap 3 now
would abandon an arc near its end and rename the effort — which is precisely how SUBPAGE-IC died.
One ACHIEVED declaration, earned, is worth a session; and it becomes the first positive entry in
`GNI_ORIGIN.md`.

---

## 6. WHAT TRAVELS TO EVERY SESSION AFTER THIS

```
ORIGIN   = docs/GNI_ORIGIN.md            -- how we got here. Past tense. Does not change.
GLOSSARY = docs/GNI_GLOSSARY_S<N>.md     -- every abbreviation. C8 enforces it.
CLAIMS   = docs/GNI_CLAIMS_S<N>.md       -- N claims, COVERAGE M/N, ORPHAN x%
```

All three must appear in the LOAD CHECK **with their counting commands printed beside them**.
That is the only protection against becoming `SUBPAGE_CERTIFICATION.md` — a real ledger, with
real numbers, that no live document pointed at, and which died without anyone noticing.

---

## 7. THE HONEST WARNING

When R3-2 completes, the item count will RISE and COVERAGE will start LOW — plausibly 20-30%.
This is not failure. It is the first time in five months that the number tells the truth. The
macro map's `Z` started at 35.8% and is now 41.8%; a low first reading is what a real instrument
produces.

The second honest warning is about this file itself: **it is a description, and descriptions rot.**
It must be superseded by the artefacts it specifies, not maintained alongside them. Once
`GNI_CLAIMS` exists and publishes COVERAGE, this file is history and should be archived — not
updated.
