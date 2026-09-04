# GNI Autonomous — Rules Registry
# Bro Alpha (James Maverick) + Claude · Reference by ID — do not re-derive
# RESTRUCTURED AT S90 (2026-08-31). Nothing was deleted. PART 3 is the S89 file VERBATIM.

## HOW THIS FILE IS ORGANISED — read this paragraph, then PART 1

The register held 134 rules and the live document set cited 18 of them. [S96 CORRECTION: the 134 was banked with no method. S95 measured 154 and closed at 159; S96 re-derived 159 markers, 57 CHECKABLE / 102 not. The 53/106 in the S95 close docs is WRONG. R-S96-2.] Rules were being
broken not because they were unread but because they did not surface AT THE MOMENT OF THE
ACT. So PART 1 groups the ACTIVE rules by TRIGGER — the thing you are about to do — and
PART 2 names the CLUSTERS, groups of rules that are one lesson wearing several numbers.
PART 3 is the full historical register, byte-identical to `GNI_RULES_S89.md`, and is the
authority on any rule's exact wording. PART 1 is an INDEX, never a replacement: a one-line
summary is a lead, and the full text in PART 3 is the rule.

---

# PART 0 — RECOVERED IDS AND A CITATION DEFECT (S90, item 9.6)

**Measured at S90:** the four live documents (CONTRACT, TARGET+ORDER, HANDOFF, Protocol)
cite 8 rule IDs that appear NOWHERE in this register: `GNI-R-037`, `GNI-R-076`,
`GNI-R-122`, `LR-101`, `R-S54-1`, `R-S54-2`, `R-S54-3`, `R-S54-4`.

**Structural cause — not forgetfulness.** This register was born at the S55 close
(CONTRACT VERSION LOG v1 says so). Every `R-S54-*` rule predates the file by one session.
The `GNI-R-###` series predates it by months and lived in a DOCX series
(`GNI_Unified_Rules_v5_3.docx` and its ancestors, GNI-R-001..~242), which was never
migrated. Law cites a page that this file never had.

**THE REAL DEFECT — CITATION DRIFT, worse than absence.** Recovered from session records:

| ID | ORIGINAL definition (from the record) | How CONTRACT v7 cites it today |
|---|---|---|
| `GNI-R-037` | Mar 2026: *"Read the FULL file before rewriting. File on disk is truth. What you see in chat may be stale."* Also recorded as `repr()` read before any replacement. Apr 2026: cited as *"Bird-eye view first before deep dive"*. | `BIRD-EYE (GNI-R-037)` — the FIRST WORD of the GATE SEQUENCE |
| `GNI-R-076` | Mar 22 2026: *"ALTER TABLE for new column additions before any writes"* — a DATABASE rule, the specific case of GNI-R-064. | *"read the FULL file before any patch (GNI-R-076)"* — which is GNI-R-037's original text |
| `GNI-R-180` | *"Bird-eye reset after three failures"* — the actual bird-eye rule | not cited anywhere |

So the two IDs at the top of the gate sequence have SWAPPED and DRIFTED. `GNI-R-076`
is cited today with `GNI-R-037`'s meaning; `GNI-R-037` is cited with a meaning
(`BIRD-EYE`) that belongs to `GNI-R-180`. Every session since S55 has obeyed the CITATION
and never the RULE, and both citations happen to be good practice, which is exactly why
nobody noticed for 35 sessions. **A rule cited by inferred meaning is a banked pointer
(R-S54-2) wearing the clothes of law.**

**RECOVERED VERBATIM — these four are law and were unfindable (S54 close, 2026-06-30):**

- **R-S54-1** — Big-write delegation: any file write >~30 lines goes to Claude Code
  (direct-to-disk, self-reads-back), NOT a hand-pasted heredoc. Bracket-paste truncation
  produced mangled terminal echo on both big writes of S54. Hand-paste is reserved for
  short patches (<~30 lines) and surgical `sed`/`str_replace`.
  **CHECKABLE: no** — governs how a write is DELIVERED in chat; the repo records no delivery method
- **R-S54-2** — Believe the LIVE byte over a banked number, ESPECIALLY a number from your
  own close docs. "159 reports" was banked; live was 76. A count in a session doc is a
  fossil the moment it is written.
  **CHECKABLE: no** — a judgement about which source to trust when two disagree
- **R-S54-3** — Verify the COMMAND finished, not just the FILE. After a paste confirm
  `$?`=0 AND a clean `$` prompt (not a `>` heredoc trap), AND check the file's MIDDLE
  (brace balance, structural anchors each = expected count). A head/tail check passes
  over a mid-file drop.
  **CHECKABLE: no** — about terminal state after a paste; no committed artifact holds it
- **R-S54-4** — Curl/fetch is a dead-end live-verify for this site; the browser is ground
  truth. `/api/*` is auth-gated, the key is never in the shell and must NOT be exported,
  web-fetch sees only pre-hydration shells. NEVER conclude "broken/empty/erroring" from a
  curl/fetch result — read the rendered page.
  **CHECKABLE: no** — chooses a verification tool for a human; nothing to assert against
- **R-S54-5** — affirms GNI-R-233: the FAMILIAR explanation is the TELL (vindicated 5x in
  one session).

**STILL UNRECOVERED: `LR-101` (pure-ASCII patch anchors) and `GNI-R-122` (heartbeat
standdown is correct behaviour).** Both are cited by live documents and are followed from
inferred meaning. Do not restate them as law until the original text is found.

**STANDING CHECK (new, cheap, runs at every close):** every ID cited by a live document
must exist in this register.
```bash
for id in $(cat CONTRACT_S*.md GNI_TARGET_AND_ORDER_S*.md HANDOFF_S*.md GNI_Session_Transfer_Protocol_S*.md \
    | grep -oE 'GNI-R-[0-9]+|R-S[0-9]+-[0-9]+|LR-[0-9]+' | sort -u); do
  grep -q -- "$id" GNI_RULES_S*.md || echo "CITED BUT NOT REGISTERED: $id"
done
```

---

### UNREGISTERED ID MANIFEST

Read by `tools/gni_rule_checks.py` (C1, R-S90-2). Renaming this heading halts the
tool with EXIT 2 rather than silently passing every citation. Statuses are closed:
`DANGLING-LAW` `UNMIGRATED-DOCX` `DEFINED-IN-CONTRACT` `DISCUSSION-ONLY`

| id | status | reason |
|---|---|---|
| `GNI-R-037` | UNMIGRATED-DOCX | cited as BEV law; text lives in the un-migrated DOCX register |
| `GNI-R-064` | DISCUSSION-ONLY | named only while CONTRACT describes the S90 citation defect |
| `GNI-R-076` | UNMIGRATED-DOCX | cited with the wrong meaning for ~35 sessions; text unmigrated |
| `GNI-R-114` | DANGLING-LAW | order item 6.8 rests on it; no recoverable text |
| `GNI-R-122` | DANGLING-LAW | cited as law by order and handoff; unfound |
| `GNI-R-180` | DISCUSSION-ONLY | named only while CONTRACT describes the S90 citation defect |
| `GNI-R-233` | DEFINED-IN-CONTRACT | CONTRACT_S94.md:24 defines it inline; routing debt |
| `LR-101` | DANGLING-LAW | cited as law by CONTRACT, order, handoff; unfound |

Eight rows. S90 measured eight; those four are fixed and four new ones accrued,
so the COUNT is unchanged and the MEMBERSHIP is not. A row leaves this table only
when the ID is registered in PART 3, or the citation is deleted.

# PART 1 — ACTIVE RULES BY TRIGGER

Each line is an INDEX ENTRY. The rule is its full text in PART 3.

## TRIGGER 1 — I am about to WRITE A PATCH
- **R-S58-1** Text-mode patching is BANNED. Read `rb`, write `wb`, byte anchors.
- **R-S57-1** Line endings are per-ANCHOR facts — this repo mixes CRLF and LF per file AND per region.
- **R-S72-1 / R-S76-1 / R-S80-1** Multi-line anchors join on the file's OWN detected newline; single-line anchors are immune; print the newline before asserting.
- **R-S81-5** A guard's expected count is DERIVED from the edit list, never hand-counted; assert RELATIVE to the file's state read at the start.
- **R-S85-3** An idempotency guard tests the ANCHOR's absence, never a sentinel drawn from the new text.
- **R-S54-1** >~30 lines goes to Claude Code, not a hand-paste. **LR-078** ship-to-file over heredoc. **LR-101** pure-ASCII anchors.
- **R-S77-1** Chained build/verify/commit after a patch run UNCONDITIONALLY — gate the chain on the PATCHED print or split the paste.
- **R-S87-5** MSYS/MINGW translates ARGUMENTS, not string literals: `/tmp` inside a heredoc is `C:\tmp`; `grep --include` is silently dropped when an unquoted flag variable expands.
- **GNI-R-037 (original text)** Read the FULL file before rewriting. The file on disk is truth; what is in chat may be stale.

## TRIGGER 2 — I am about to TRUST A NUMBER OR AN INSTRUMENT
- **R-S54-2** Live byte over any banked number, especially one from our own docs.
- **R-S67-2** Verify the instrument's RANGE (caps, truncation, short-circuits) — *and its EPOCH* (2026-08-25 amendment): a counter and the data it counts can start at different times.
- **R-S82-2** An instrument dumps the WHOLE category, not the field the hypothesis names.
- **R-S84-2** When two meters disagree, calibrate against the one that ENFORCES.
- **R-S86-2** Two instruments printing the same word may count different things; near-agreement is a finding about the difference, never corroboration.
- **R-S87-7** Name the DENOMINATOR at the print site.
- **R-S88-4** Design the EXTRACTION for the question; positional truncation (`head`, `tail`) is a guess about where the answer lives.
- **R-S80-2** An instrument certifies only the call-shape it holds.
- **R-S84-1** If the producing function is PURE, call it — never derive a formula you can measure.

## TRIGGER 3 — I am about to CALL SOMETHING A FINDING
- **R-S89-1** LINEAGE-BEV applies to a FINDING, not only a proposal. Before calling two byte-facts a contradiction, search for the DECISION that created the difference.
- **R-S69-1** A byte-census says what IS; only session history says which side is CANONICAL.
- **R-S86-6** `git log -S '<symbol>'` is the third lineage stage — a commit subject is the only lineage written by the person who made the change.
- **R-S83-1** A disclosed limitation is a CLAIM, not a fact. **LR-107** a brief-claimed bug is a hypothesis.
- **GNI-R-233 / LR-102 / R-S54-5** FAMILIAR/EASY = THE TELL. When corrected, RESET to zero.
- **R-S84-3** A correction that is not WRITTEN DOWN as a correction will re-form in a later session with fresh confidence.
- **R-S81-1** A zero-match indicts the PATTERN first — *and a REDIRECTED FAILURE is worse than silence, because it produces a corpus* (2026-08-25 amendment): `wc -l` before `grep`, always.
- **R-S82-1** To find an artifact, grep its STRUCTURE, not its name — a high match count misleads exactly as a zero match does.
- **R-S83-2** Novelty is an IDENTITY question. Compare run IDs; print the id next to the claim.
- **R-S75-2** A grep hit showing ONE condition of a chained query is not the filter.
- **Protocol step 8h** Absence is evidence: never-firing keywords, never-taken branches, a regime with no counterexample.

## TRIGGER 4 — I am about to PROPOSE (lettered A/B/C)
- **CONTRACT v7 LINEAGE-BEV** — a lettered proposal without a `LINEAGE:` line has not been made.
- **R-S85-1** An unresearched lean STEERS James's ruling and launders itself into an operator decision.
- **Read the GRAVEYARD** in the live order file before proposing in ROOT 8, ROOT 1, or retention.
- **R-S81-3** Absolute allotments, never leftover budgeting — *and count DISTINCT IDENTITY, not rows* (2026-08-24 amendment).
- **R-S87-1** An ABSOLUTE threshold cannot measure a PRE-SELECTED set — ask WHO SELECTED the set being scored.
- **R-S88-5** A pillar at its CAP cannot be moved by editing its word list; measure headroom before proposing any list edit.
- **R-S90-4** A rule invoked to defer ONE item binds every item of the same class in the same session.
- **R-S90-2** An id cited by a live document is law only if the register holds it; a citation followed by inferred meaning is a banked pointer.
- **R-S82-3** A stopgap never closes a root. **R-S69-2** a deferral without an instrument is a debt that launders itself into fact.
- **Before minting a rule number**, search BOTH ID schemes — a grep for one is blind to the other (S83 amendment note).

## TRIGGER 5 — I am about to SHIP / COMMIT
- **R-S81-6** Grep ONE DISTINGUISHING PHRASE PER AGREED ELEMENT before committing; producing text in conversation FEELS like shipping it.
- **R-S85-6** State the FAILURE TEST in the commit that ships the change. A cert that cannot fail is a ceremony.
- **R-S55-1** Sibling sweep: a bug in one consumer of a shared route → grep ALL consumers. **R-S82-4** this applies to TEMPLATES when law changes.
- **R-S55-2** Widen the fossil grep before declaring a class swept. **R-S59-1** census before sweep. **R-S71-2** census the CLASS, not the named list.
- **R-S73-1** One semantic contract = ONE definition; extract a shared builder rather than hand-copying.
- **R-S73-2** Census ALL consumers before gating a value in place; a value feeding a loop AND a public exhibit gets a gated COPY.
- **R-S70-1** Any table gaining a new writer triggers a WRITERS census.
- **R-S55-3** Confirm the PATCHED print before trusting any verify-grep. **R-S54-3** then exit status and a clean prompt.
- **One thing per commit.** `git status` first; stage files EXPLICITLY.

## TRIGGER 6 — I am about to CERTIFY
- **GNI-R-242** A fix is a hypothesis until verified against live data. Test-clean is not proven-working.
- **R-S87-4** A shipped patch is not a wired feature — verify the CONSUMER CHAIN and the store, not the edit.
- **R-S83-4** A cert that measures MECHANICS (no 413s, no empties, it arrived) has not certified the instrument; a behaviour cert needs a BAND measured before and after.
- **R-S74-3** Certification via CI logs starts at the run's CHECKOUT SHA.
- **R-S78-2** A green run proves completion, not WHICH path served it.
- **R-S89-3** A newly added column renders the SAME empty marker a failed ship would. Name the run that will clear it.
- **R-S86-5** A refuted prediction may be naming a missing CONDITION, not a wrong fix — diff the runs for the variable that moved.
- **R-S54-4** The browser is the only live-verify. **R-S60-1** hard-refresh first; a stale bundle mimics a code bug perfectly.
- **R-S90-1 — A CERT MUST DISCRIMINATE.** Before reading a page as proof, ask what it would look like if the change had NOT shipped. `/autonomy` renders `30 min` from the hardcoded map and from the measured `0.5` identically, so the screenshot certified nothing. A cert whose PASS and FAIL states are visually identical is a ceremony (kin of R-S85-6 and R-S89-3).

## TRIGGER 7 — I am about to DELETE, RETIRE, OR CALL SOMETHING DEAD
- **R-S89-2** "No query filters on it" is not "nobody needs it" — find the PUBLISHED CLAIM the data supports first.
- **R-S88-3** Absence from the LIVE file is not a dropped item — read the generations between.
- **R-S85-4** A finding folded into another arc's scope DIES when that arc is declared achieved.
- **R-S79-2** A deprecation list proves the list, not the runtime — grep live logs before declaring anything dead or alive.
- **R-S86-3** A conditional that never evaluates False is not a conditional; an untaken branch is untested code however old.
- **R-S65-3 / R-S66-2** Never blind-wrap keyword lists in word boundaries; census what real signal entered through a bug's side door before closing it.
- **R-S63-2** Fallback resources are guilty-until-verified. **R-S63-3** no protection may permanently mute its own alert path.

## TRIGGER 8 — I am writing COMMANDS FOR JAMES
- **R-S79-1** Every action ships as a runnable command; never ship a gated block in the same message as its gate.
- **R-S81-4** ONE load-bearing block per message; rollbacks never travel with applies; assume any block may run twice, out of order, or not at all.
- **R-S88-1** SQL and shell never share a paste block — `->` IS a redirection and silently truncates files.
- **R-S62-2** Any placeholder is loudly marked; James runs commands verbatim.
- **R-S67-1** When a change spans code and live state, hand over NUMBERED GATES with the code push explicitly first — paste order becomes system state.
- **R-S62-1** Claude Code tasks get a post-run mechanical verification block and a one-command revert path.
- **R-S90-3** A REVISED procedure must re-emit its preconditions; one left in the superseded message is not part of the block.
- **R-S78-1 (amended S90)** A receipt proves the WRITE, not the VALUE — dispatch and grep the env dump for `***`.
- **R-S65-2** Executor diffs get chat clearance BEFORE the git trigger, every time.

## TRIGGER 9 — I am about to say something about TIME, SCHEDULES, OR RUNS
- **R-S83-3** Read the clock in the SAME block that makes the claim. Never state elapsed time from turn count or memory.
- **R-S87-6** Scheduler lateness is a measured PROPERTY of the free tier, not an event. **First amendment (S88):** where two schedulers lag independently, the GAP is a distribution, not the constant its cron comment claims. **Second amendment (S89): lateness is measured against the SLOT, never against the previous run.**
- **R-S81-7** Record REQUESTED time and OBSERVED time separately. Requests: pipeline 02:13/10:13, MAD 02:43/10:43, grounding-watch 11:13 UTC.
- **R-S84-4** `gni_mad.yml` runs BOTH the debate and the grounding-watch — distinguish by `ARB-FIT`, never by time alone.
- **R-S81-8** Groq TPD is a leaky bucket refilling continuously; there is no daily reset. Any "the quota resets" reasoning is about a fiction.

## TRIGGER 10 — SESSION OPEN AND CLOSE
- **R-S86-4** PART D is instantiated from the highest-numbered protocol FILE, never from a chat transcript.
- **R-S83-5** A ritual document needs a path into the session that begins with a READ.
- **R-S85-5** A register with no scheduled reader decays into an archive. *(This file's answer to that rule is PART 1 plus the standing check in PART 0.)*
- **R-S82-5** Apply the law-vs-state test to the VERSION LOG itself, not only to the sections.
- **R-S74-1** Registry appends assert ID-uniqueness against FILE BYTES; the next free ID is a read result, never a memory.
- **R-S55-5 / CONTRACT CLOSE DELIVERY v6** Every close artifact is session-numbered; the live file is the highest number; the close ends with a FILE MANIFEST.

## PHI-003 NON-NEGOTIABLES (unchanged, quick reference)
NN-PHI-1 GNI serves the human being, not the market (Teenager Standard) · NN-PHI-2 all news
directions equal · NN-PHI-3 no manipulation techniques in output · NN-PHI-4 every threat has a
path · NN-PHI-5 absence is intelligence, coverage gaps reported (OPEN since S37) · NN-PHI-6
adversarial sources are signal not authority · NN-PHI-7 data reset when philosophy resets.

---

# PART 2 — CLUSTERS: ONE LESSON, SEVERAL NUMBERS

A cluster is a set of rules that were minted separately and say the same thing. Read the
cluster, not the member. **Where a cluster keeps growing, the register is treating a
recurring failure as a series of new discoveries** — that is the hazard this part exists
to make visible.

**CLUSTER A — THE PATCH ANCHOR (10 rules, 8 sessions, and it still fired twice at S90).**
`R-S57-1` → `R-S58-1` → `R-S72-1` → `R-S76-1` → `R-S80-1` → `R-S81-5`, plus `LR-078`,
`LR-101`, `R-S85-3`, `R-S77-1`. Six of these say some version of *derive the newline from
the file's own bytes*. At S90 a multi-line anchor failed twice anyway — first as LF against
CRLF, then as CRLF against a file that turned out to mix BOTH inside the same ten-line
block, which `R-S57-1` states in its own first sentence ("per-ANCHOR facts ... per-file AND
per-region") and which every later rule quietly narrowed to per-file. **The cluster's
correct form, and the S90 addition: locate a multi-line region STRUCTURALLY (first line
matches, scan to the closing token) and never join remembered text with any newline at
all.** Single-line anchors remain immune and are always preferred.

**CLUSTER B — MATCH COUNT IS NOT EVIDENCE, IN EITHER DIRECTION.**
`R-S81-1` (zero match indicts the pattern) + `R-S81-1 AMENDED` (a redirected failure
produces a corpus; `wc -l` before `grep`) + `R-S82-1` (a high match count misled) +
`R-S83-2` (a CORRECT match on a stale artifact misled) + `R-S75-2` (a partial match on a
chained query misled). Four different match outcomes, one lesson: **only the SHAPE of the
match is evidence.**

**CLUSTER C — THE INSTRUMENT IS PART OF THE SYSTEM UNDER TEST.**
`R-S67-2` (+epoch) · `R-S82-2` · `R-S84-2` · `R-S86-2` · `R-S87-7` · `R-S88-4` · `R-S80-2`.
Range, epoch, category coverage, enforcement, naming, denominator, extraction, call-shape —
seven ways the measuring device decides the answer before the world does.

**CLUSTER D — THE SYSTEM GUARANTEED THE THING IT IS MEASURING.**
`R-S87-1` (absolute threshold on a pre-selected set) · `R-S87-2` (a cap always at its limit
is censorship) · `R-S87-3` (a single-regime corpus cannot be calibrated) · `R-S86-3` (a
conditional that never evaluates False) · `R-S88-5` (a pillar at its cap cannot be moved by
a list edit). **This cluster IS the CROSS-ROOT DIAGNOSIS in the order file.** When a metric
is >90% constant, ask WHO GUARANTEED IT before tuning it.

**CLUSTER E — SHIPPED ≠ WIRED ≠ CERTIFIED.**
`GNI-R-242` · `R-S87-4` · `R-S83-4` · `R-S74-3` · `R-S78-2` · `R-S85-6` · `R-S86-5` ·
`R-S89-3` · S90's discriminating-cert rule. Five months passed between `score_breakdown`
being patched and anyone noticing it reached 0 of 191 rows.

**CLUSTER F — THE BYTES SAY WHAT IS; THE RECORD SAYS WHICH SIDE IS CANONICAL.**
`R-S69-1` · `R-S85-1` · `R-S86-6` · `R-S84-3` · `R-S88-3` · `R-S89-1` · `R-S89-2` ·
`GNI-R-233` · `LR-102` · `LR-107` · `R-S54-5`. **The largest cluster, and the one with the
most repeat offences.** Its S89 form is the sharpest: *two numbers that differ are often
two different subjects.*

**CLUSTER G — A DOCUMENT NOBODY OPENS IS NOT A REGISTER.**
`R-S85-5` · `R-S85-4` · `R-S83-5` · `R-S82-4` · `R-S86-4` · and now PART 0's citation
drift. The failure mode is always the same: the artifact exists, is correct, and is never
read at the moment it would have mattered.

**CLUSTER H — THE PASTE IS THE EXECUTION MODEL.**
`R-S79-1` · `R-S81-4` · `R-S88-1` · `R-S62-2` · `R-S67-1` · `R-S77-1`. James runs blocks
verbatim, in order, sometimes twice. Every one of these was earned by a block that ran when
it should not have, or did not run when it looked like it had.

---

# PART 3 — HISTORICAL REGISTER (verbatim `GNI_RULES_S89.md`, nothing removed)

*Authority on exact wording. PART 1 indexes it; it does not replace it. S90's own earned
rules are appended at the S90 close, below this line, in the usual format.*

---


## GNI-R Rules (Architecture/Operational)
  **CHECKABLE: no** — a cognitive tell - felt familiarity has no representation in bytes

**GNI-R-240** — MAD Handshake Gate: MAD waits for Intelligence pipeline completion via polling (60s intervals, 25 attempts max) before running. Time assumptions replaced by guarantee-based gate.
  **CHECKABLE: yes** — grep ai_engine/mad_runner.py for the polling gate constants (60s, 25 attempts)

**GNI-R-241** — Content Type Classification Mandatory: Every article passing Stage 1 MUST have content_type set to news, news_with_review, or review_only before reaching Stage 2. Any pipeline run skipping classification is invalid.
  **CHECKABLE: yes** — SQL: rows past Stage 1 with content_type IS NULL must be zero

**GNI-R-242** — A Fix Is a Hypothesis Until Verified: No fix is "done" until verified against regenerated output or live data. Test-clean (compiles, passes self-test, no crash) is NOT proven-working (actually catches/produces the intended result in production). State fixes as test-clean-but-prod-pending until live data confirms. (S40: flatline check never fired <4 reports; workflow alerts untested on real failure; published_at confirmed only after a post-fix run.)

## LR Rules (Lessons Learned)
  **CHECKABLE: no** — governs when a claim may be CALLED done; the claim lives in prose

**LR-078** — Ship-to-file patch over bash heredoc: Git Bash corrupts heredocs with bracketed paste. Always write patches to /tmp/*.py files and run with python /tmp/patch.py.
  **CHECKABLE: no** — patch scripts live in /tmp and are never committed - nothing to scan

**LR-091** — Naming consistency check required: Before any integration commit involving new env vars or DB column names, grep all files that read those names and verify exact string match. The 343-hour Telegram webhook darkness (SUPABASE_SERVICE_ROLE_KEY vs SUPABASE_SERVICE_KEY) is the permanent reminder — one wrong character = silent failure for weeks.
  **CHECKABLE: yes** — every os.getenv name must resolve to a stored secret or a workflow env (section 7.2 emits the join)

**LR-092** — py_compile ALL modified .py files before commit.
  **CHECKABLE: yes** — python -m py_compile over changed .py files in CI

**LR-095** — HTTP error: always check r.text[:200] first, never diagnose from status code alone.
  **CHECKABLE: no** — governs how a human diagnoses an HTTP error, not the shape of code

**LR-096** — Never dump raw DB blob columns >1000 chars into AI prompts.
  **CHECKABLE: no** — no truncation convention exists to assert prompt fields against

**LR-098** — When removing pip package: grep code/ for imports first across ALL files, not just one.
  **CHECKABLE: yes** — every package in a workflow inline pip list must be imported by a reachable module
**LR-102** — Confidence is a signal to slow down, not speed up: When a task feels familiar or a fix feels obvious, treat that feeling as the trigger to read the full file / trace the data first — not as permission to skip BEV. "I know this" is not evidence. (S40: guessed a table name, guessed where GNI-R-228 lived, reconstructed file content from memory, assumed the next-free rule number — every time, the actual read corrected it.)
  **CHECKABLE: no** — a cognitive tell; confidence is not stored anywhere
**LR-103** — Real data over constructed tests: A test you wrote proves the code does what you IMAGINED; only real, un-curated input proves it does what the world NEEDS. When validating, include at least one live example (real headline, real input), not only cases designed to pass. (S40: entity_extractor passed 8/8 constructed but real headlines "Japan's"/"Lebanon's" instantly exposed a possessive bug -- the constructed tests never used a possessive.)
  **CHECKABLE: no** — governs the CHOICE of test input, which the test file does not record
**LR-104** — Rank work by blast radius, not just possibility: Before building, sort candidate tasks by risk -- schema/production changes = highest (hold for fresh focus + SQL-before-code); config/standalone modules = safe. Energy or enthusiasm is never a reason to do the riskiest thing at the tail of a long session. (S40: built new sources + standalone modules safely; deliberately held B3 schema-wiring for a fresh session.)
  **CHECKABLE: no** — ranks candidate work by risk before it exists; no artifact to rank
**LR-105** — Protect the future of the work over the momentum of the moment: Never make a failing check pass cosmetically. Revert to the honest proven state and log the real finding loud. A codebase must never lie about what it can do. (S40: a real-headline test found a genuine bug at 8/10 -- reverted to honest 8/8 + logged the bug for a proper fix rather than papering it green.)
  **CHECKABLE: no** — forbids cosmetic green; distinguishing cosmetic from real needs the intent

**LR-099** — Philosophy Compatibility Gate: When Claude reads a finalized philosophy document AND has access to the implementation codebase, Claude must perform a compatibility audit unprompted. Map each non-negotiable principle to its code implementation. Any gap found must be surfaced immediately. Full context visibility = full audit responsibility. Reference: phi_compatibility_check.md in repo root.

## PHI-003 Non-Negotiables (Quick Reference)
  **CHECKABLE: no** — an audit obligation on the agent; no artifact records whether it happened

- NN-PHI-1: GNI serves the human being, not the market. Teenager Standard.
  **CHECKABLE: no** — a value statement about who GNI serves; no measurable predicate
- NN-PHI-2: All news directions equal — good, bad, opportunity, threat.
  **CHECKABLE: no** — requires judging whether coverage is direction-balanced; needs a labelled corpus
- NN-PHI-3: Manipulation techniques never in GNI output.
  **CHECKABLE: no** — detecting manipulation in output requires reading the output for meaning
- NN-PHI-4: Every threat must have a path. fff_human_path always required.
  **CHECKABLE: yes** — SQL: reports rows with fff_human_path IS NULL must be zero (needs DB, not CI)
- NN-PHI-5: Absence is intelligence. Coverage gaps reported. (OPEN — S37)
  **CHECKABLE: no** — OPEN since S37; 'coverage gap' has no operational definition to assert
- NN-PHI-6: Adversarial sources are signal not authority.
  **CHECKABLE: no** — requires weighing a source's authority - a judgement about content
- NN-PHI-7: Data reset when philosophy resets.

Last updated: May 24, 2026 — GNI S36
  **CHECKABLE: no** — a policy about when to reset data; the trigger is a human decision

## LR-106 -- LLM JSON parsers must guarantee dict-or-None
Any function parsing LLM JSON output (e.g. _parse_json_response) MUST coerce the
result to dict-or-None before returning. LLMs intermittently wrap the report in an
array [{...}]; json.loads then returns a list and downstream .get() crashes ('list'
object has no attribute 'get'). Unwrap single-object lists to the dict; return None
for [] or non-dict arrays. Root-caused from Jun 7 Intelligence #210 (the only failure
in 9 autonomous days). Fix: commit a15bcc0.
  **CHECKABLE: yes** — AST: every _parse_json_response-class function's return paths yield dict or None

## LR-107 -- A brief-claimed bug is a hypothesis, not a fact
A bug asserted in a prior session's brief (or by anyone) is unverified until reproduced
against live execution. S42 had TWO false ones: the S41 "URGENT" possessive bug (a test
artifact from heredoc apostrophe-stripping) and the initial "Sunday digest mutates shared
state" theory for #210 (the code shared no state; real cause was list-shaped JSON). Verify
before fixing. Confidence is the tell to slow down. Extends GNI-R-233 / LR-102.
  **CHECKABLE: no** — governs trust in a prior session's claim; trust has no byte form

- **R-S55-1 - Sibling sweep:** when a bug is found in ONE consumer of a shared route/field, grep ALL consumers before closing the arc. (The 4th false-185% sibling on /about/devops sat undiscovered for 2 sessions.)
  **CHECKABLE: no** — 'all consumers of a shared route' has no mechanical boundary
- **R-S55-2 - Widen the fossil grep:** after any fossil is found, generalize its pattern before declaring the class swept. (The "02:00" grep missed the ":30" MAD variants.)
  **CHECKABLE: no** — widening a pattern is an act of imagination; there is no wider-pattern oracle
- **R-S55-3 - Confirm the patch ran before trusting the verify:** require the PATCHED/DONE print first; verify-greps on an unpatched file prove nothing. (U1 was "verified" twice on an unpatched file.)
  **CHECKABLE: no** — about the ORDER of two steps in a terminal session; no artifact
- **R-S55-4 - One calibration:** model-coupled fixes (budget solver, quality scorer, grounding gate) bundle WITH the model migration, never before it.
  **CHECKABLE: no** — bundling policy for model-coupled fixes; scope lives in the plan, not the tree
- **R-S55-5 - Transfer Protocol v1 adopted:** HANDOFF_S{N}.md + CONTRACT.md replace the 6-file close. Caps hard, delta-only, LOAD CHECK echo mandatory. Spec: docs/GNI_Session_Transfer_Protocol.md.
  **CHECKABLE: no** — records the adoption of Protocol v1 - a historical fact, not a predicate

- **R-S56-1 - Escape at the boundary:** a failure reason (or any external/LLM text) is hostile input to any formatting channel (Telegram HTML, etc). Escape at insertion or drop the parser. (The Stimson 403 reason contained literal <unknown>, poisoned its own alert, and shadow-killed reserves for 967h. Sibling sweep closed the class across 3 files in S56-S57.)
  **CHECKABLE: yes** — grep every Telegram send site: an HTML-mode send interpolating external text must call the escape helper
- **R-S57-1 - Line endings are per-ANCHOR facts:** this repo mixes CRLF and LF per-file AND per-region. Every patch script carries the LF->CRLF fallback and confesses which matched; never infer a file's convention from one hit.
  **CHECKABLE: no** — governs patch scripts in /tmp; the repo keeps no copy of them

- **R-S58-1 - Text-mode patching banned:** Python text-mode open() is a line-ending NORMALIZER: it converts CRLF->LF on read, so writing the
string back rewrites the entire file's endings even for a 2-char edit. ALL patch scripts on this
repo read rb / write wb with BYTE anchors (b"..."). Text-mode file patching is banned.
  **CHECKABLE: no** — same as R-S57-1 - the banned open() lives in uncommitted patch scripts

R-S59-1: Census before sweep -- grep the FULL tree for a claim before patching any instance; never chain a git commit after a sweep-verify grep in the same paste (81->70 took 3 commits because commit fired before census was read).
  **CHECKABLE: no** — 'census before sweep' is an ordering of two human acts; no artifact

R-S60-1: Browser verification requires a hard-refresh (Ctrl+Shift+R) first -- a stale client
  bundle perfectly mimics a code bug (V-W13: code, API, and DB were all clean; cache was the bug).
  **CHECKABLE: no** — about a browser hard-refresh before verifying; nothing in the repo
R-S60-2: Structural quality scores do not measure grounding. A MAD run scoring 100% published
  two fabricated entities. Grounding requires its own deterministic gate against the article basket.
  **CHECKABLE: no** — a design principle: structure is not grounding. No predicate over bytes
R-S60-3: Never pipe an ungrounded layer's output into grounded layers unchecked. Consultants
  receive no article basket; labeling their text "PERSONAL CONSULTANT TO YOU" launders invention
  into evidence. 4/4 confirmed specimens entered through this channel.
  **CHECKABLE: no** — 'ungrounded into grounded' requires knowing which layer is grounded - a judgement

R-S62-1: Claude Code tasks get a POST-RUN mechanical verification block (greps + diff-stat +
  build) and a one-command revert path. Never assign live watch-duty to the operator --
  safety lives in commands, not attention.
  **CHECKABLE: no** — governs how a Claude Code task is handed over; no committed artifact
R-S62-2: Any placeholder in a command MUST be loudly marked (warning emoji + "PLACEHOLDER" +
  what to substitute). The operator runs commands verbatim. (S62: <path> and YOUR_KEY both ran literally.)
  **CHECKABLE: no** — placeholder marking lives in a chat message, not in the tree
R-S62-3: Server-side Supabase reads go through createNoStoreClient (src/lib/supabaseNoStore.ts).
  New API routes never call createClient directly -- Vercel Data Cache serves fossils otherwise.
  **CHECKABLE: yes** — SHIPPED C4: git grep createClient under src/app/api must be empty

R-S63-1: Any option list whose reply-number maps to list POSITION in a consumer (Telegram
  webhook class) must preserve numbering across changes -- annotate bad options, never
  filter, until every consumer is read and updated in the same commit.
  **CHECKABLE: no** — 'reply-number maps to list POSITION' needs the consumer's semantics
R-S63-2: Fallback resources (reserves, backups, secondaries) are guilty-until-verified:
  live-check + dedupe-against-primaries before they may be offered as safety. A dead
  reserve is worse than none -- it converts an outage into a silent one.
  **CHECKABLE: no** — 'guilty until verified' is a stance toward a resource, not a code shape
R-S63-3: No protection may permanently mute its own alert path. Any "already handled ->
  skip alert" state needs an escalation branch for re-failure.
  **CHECKABLE: no** — requires proving a branch can be reached again - a reachability proof, not a grep

R-S64-1: "Success. No rows returned" (any silent DB response) proves nothing. Every
  UPDATE gets a SELECT verify, and state audits census the WHOLE table (no LIMIT) --
  a LIMIT hid a live PRIMARY-DUP row in S64.
  **CHECKABLE: yes** — grep audit/census scripts for .limit( - a whole-table audit may not truncate
R-S64-2: Aggregated views (trace Collected, dashboard counts) cannot answer WHO served
  a slot -- reserve articles log under the primary's name. The run's raw console log is
  the only authority on serve-path questions; read it before concluding.
  **CHECKABLE: no** — about what an aggregate CANNOT answer; absence of an answer is not greppable
R-S64-3: Dedupe fallback resources by feed DOMAIN, not display name. "Radio Free
  Europe" vs "RFE/RL" sailed past a name-set guard while serving identical rferl.org
  content -- name spelling is not identity.
  **CHECKABLE: yes** — assert the fallback dedupe key is a parsed feed domain, not a display name
R-S65-1: Fetch-based "recovery" is not recovery. Any auto-retire/auto-activate criterion
  must consult yield or serve-path, not transport alone -- C2 retired a reserve for a
  primary that fetched fine and served zero.
  **CHECKABLE: no** — 'consult yield or serve-path' requires reading what a criterion MEANS
R-S65-2: Executor (Claude Code) diffs get chat clearance BEFORE the git trigger, every
  time, however clean they look. Review-then-trigger is the contract's protection for
  the day the diff isn't clean.
  **CHECKABLE: no** — chat clearance before a git trigger; the clearance is a chat turn
R-S65-3: Never blind-wrap keyword lists in word boundaries. Lists contain deliberate
  stems (extremis, geopolit); use an explicit stem convention ('*' suffix) and annotate
  conservatively -- a too-greedy stem is the substring bug wearing a different hat.
  **CHECKABLE: yes** — assert no \\b wrapper is applied to entries in the stem keyword lists

R-S66-1: A keyword-level census proves kills; only an article-level comparison
  proves signal preservation. When a ruling ADDS vocabulary, the keyword census
  is structurally blind to the rescue -- verify at the article level.
  **CHECKABLE: no** — which census proves which claim - an epistemic distinction, not a byte one
R-S66-2: Substring bugs can be load-bearing. Before anchoring any matcher,
  census what REAL signal entered through the bug's side door (demonyms via
  country names, 'enforced' via 'forced', IranWire via 'iran') and re-admit it
  deliberately -- silent suppression is worse than the inflation being fixed.
  **CHECKABLE: no** — requires measuring what real signal entered through a bug - needs the corpus
R-S66-3: A proxy in a vocabulary list (brand-as-actor, source-as-signal) is
  allowed only if declared in-code AS a proxy, with the honest cost and the
  proper fix named. Undeclared proxies are future fossils.
  **CHECKABLE: no** — no in-code proxy-declaration convention exists to assert against
R-S67-1: When a change spans code and DB/live state, hand over the steps as
  NUMBERED GATES with the code push explicitly first -- commands delivered
  together get executed in paste order, and paste order becomes system state.
  **CHECKABLE: no** — numbered gates with the push first - about message structure
R-S67-2: Before trusting any statistic from an instrument, verify the
  instrument's RANGE (caps, truncation, short-circuits). A metric that cannot
  move is not evidence of stability -- the trace's 3-keyword cap censored the
  match-count deflation K-WATCH was built to observe.
  **CHECKABLE: no** — verifying an instrument's RANGE means reasoning about caps and short-circuits

R-S68-1: A model/secret swap plan is incomplete until a BARE-HARDCODE census runs -- grep call-site literals and workflow YAML, not just os.getenv defaults. The funnel L4 call and gni_adaptive.yml both hid from the secrets-only view.
  **CHECKABLE: yes** — grep workflow YAML and call-site literals for model-name strings not sourced from env
R-S68-2: GitHub Actions masks secret values as *** in CI logs -- a log can prove a secret is SET, never what it contains. Don't burn session time trying; only the keyfile ritual resolves values.
  **CHECKABLE: no** — a platform fact about log masking, not a rule the repo can violate
R-S69-1: A byte-census says what IS; only session history says which side is canonical.
  No public-copy fix ships without reading the claim's design lineage first -- the S59
  sweep and the S69 near-sweep pointed OPPOSITE directions off the same bytes.
  **CHECKABLE: no** — 'history says which side is canonical' - the evidence is conversation records
R-S69-2: Any mid-session fallback substitution ("simpler approach for now") and any
  James-deferral must leave an instrument in the same message: a queue row, a date or
  trigger, and a scheduled verify. Close docs mark "DONE (fallback: X deferred)" --
  never bare DONE. Substitution without a debt record launders itself into fact.
  **CHECKABLE: no** — requires deciding whether a queue row genuinely instruments a deferral
R-S69-3: Protections-guilty extends to WIRING: a security module's first BEV question
  is "who imports me?" A green self-test on an orphan module is a false positive.
  Run the orphan-import census at every model-change re-audit.
  **CHECKABLE: yes** — assert every module under ai_engine/analysis is imported by an entrypoint-reachable module
R-S70-1: Shared DB state gets shared-route discipline (R-S55-1 kin): any table gaining a
  new writer triggers a WRITERS census -- name every function writing each column. Two
  writers with different formulas for one column is a design review, not a merge; audit
  the seam, not the files.
  **CHECKABLE: yes** — emit writers-per-table from the tree and fail when the set changes (snapshot)
R-S70-2: Chat-generated docs get a landing gate before first commit: wc -l on disk vs
  expected, STOP on mismatch. A cat >> to a never-saved path silently creates a stub --
  the D-8 disease in commit form.
  **CHECKABLE: yes** — wc -l on disk against the expected count before first commit
R-S71-1: Dual-writer dedupe merges by OWNERSHIP, not timestamp: when two writers fought over rows,
  the owning writer's row wins even when the stomper's is fresher. "Keep freshest" enshrines
  whoever stomped last. Preview-before-delete is what catches this -- never skip the preview.
  **CHECKABLE: no** — 'the owning writer wins' requires knowing who owns a row
R-S71-2: Census the CLASS, not the named list: a spec that names 4 ghosts gets a sweep of the WHOLE
  dict against the roster (found 6); a relabel of 4 "Total X" strings gets a sweep for every
  totality-implying label over a LIMIT query (found 6). The named instances are leads, not the set.
  **CHECKABLE: no** — 'census the CLASS' - naming the class is the judgement being asked for

R-S72-1: Multi-line patch anchors join on the file's DETECTED newline ('\r\n' if '\r\n' in d
  else '\n'); an LF-joined anchor against a CRLF working copy counts 0 and dies clean but wastes
  the round. Single-line anchors are immune. Print NEWLINE=%r before asserting.
  **CHECKABLE: no** — patch-script rule; those scripts are never committed

R-S73-1: One semantic contract = ONE definition. When two sites need the same list/whitelist/
  threshold, extract a shared builder placed next to its source of truth and import it --
  hand-copies drift silently and the drift ships as divergent behavior.
  **CHECKABLE: yes** — detect the same literal list or threshold defined in two files (duplicate-constant lint)
R-S73-2: Before gating/sanitizing a value in place, census ALL its consumers first. A value
  feeding both a feedback loop and a public exhibit/metric gets a GATED COPY for the loop;
  the raw original stays for everything else. In-place gating erases exhibits silently.
  **CHECKABLE: no** — requires knowing which consumers are feedback loops and which are exhibits

R-S74-1: Registry appends assert ID-uniqueness against FILE BYTES before writing -- the next
  free ID is a read result, never a memory. (D-10 collision: assert caught a duplicate the
  handoff-informed guess would have shipped.)
  **CHECKABLE: yes** — SHIPPED C3: every repeated definition id must declare AMENDMENT/INSTANCE
R-S74-2: A frontend interface declaring DB fields is a HYPOTHESIS -- verify every field against
  information_schema before trusting any page's type. (F23: three phantom fields rendered
  fossils for weeks; the March sprint doc warned this verbatim.)
  **CHECKABLE: yes** — compare TypeScript interface fields against information_schema.columns
R-S74-3: Certifying shipped code via CI logs starts at the run's CHECKOUT SHA -- a missing
  feature line proves nothing until you know which commit executed. (Morning NULL was
  pre-GT5 state, not a failed seam.)
  **CHECKABLE: yes** — assert every cert record names the checkout SHA it was read from

R-S75-1: Counting items in a code literal (pattern lists, configs) is an AST job, never a
  regex-over-text job -- regex stops at the first nested bracket and censors the count.
  (Funnel patterns: regex said 16, AST said 81; the public claim was true all along.)
  **CHECKABLE: yes** — assert count guards over code literals derive expected values via ast, not regex
R-S75-2: A grep hit showing ONE condition of a chained query/filter is not the filter --
  read the full call site before classifying a lead. (GRAPH-S2 false alarm: the .eq
  stage2 line had two conjoined siblings just above it.)
  **CHECKABLE: no** — 'read the full call site' is an instruction to a reader, not a predicate
R-S75-3: When a sequential funnel persists per-stage flags with default-True 'not evaluated'
  semantics, every aggregate over the trace must conjoin ALL prior stage flags --
  counting one flag alone reports the default, not the funnel. (TRANS-COUNT: 360 > 262.)
  **CHECKABLE: yes** — grep funnel aggregates for counts conditioned on one stage flag only

R-S76-1: Multi-line patch anchors must derive the newline from the target file's own bytes (nl = CRLF if in file else LF) -- hardcoded \n silently matches zero on CRLF working copies. Single-line anchors are immune. (C1 first attempt: a1 count 0, zero bytes written.)
  **CHECKABLE: no** — patch-script rule; not committed
R-S76-2: A handoff oracle spec must record the exact workflow name AND the print format as bytes, not paraphrase -- 'Stage 2: X -> Y' matched nothing because the real print is 'Stage 2 (Deduplication): X -> Y articles' in a different workflow. Grep the phenomenon, not the report of it.
  **CHECKABLE: no** — an oracle spec's fidelity to bytes is judged by comparing meanings
R-S76-3: A uniform denominator across rows with varying numerators is arithmetically impossible from a per-item counting loop -- treat it as an instant fossil-or-bug tell. (39 sources, wins 28-70, every total exactly 102 = pre-fix global-count fossils.)
  **CHECKABLE: no** — an arithmetic tell about a suspicious table; needs the numbers in hand
R-S77-1: Chained build/verify/commit commands after a patch script run UNCONDITIONALLY -- a failed assert writes zero bytes but the chain proceeds on the unpatched tree. Gate the chain on the PATCHED print, or run patch and commit as separate pastes. (C5 first attempt.)
  **CHECKABLE: no** — about chaining commands in a paste block; no artifact
R-S77-2: For count claims in prose copy, removing the number beats hydrating it -- prose that names no count can never rot, and plumbing-to-prose is bad engineering. Hydrate only where a number is displayed as a stat. (Feedback SWOT: two mentions cured count-free.)
  **CHECKABLE: yes** — grep live docs for a bare numeric count that no generator emits
R-S77-3: A live-computed stat can still lie by ATTRIBUTION -- verify the label's system name against the data source, not just the number's math. ('52 correct' was live math under a GPVS label while reading debate_predictions.)
  **CHECKABLE: no** — verifying a label's ATTRIBUTION requires knowing what the system is called
R-S78-1: A UI write (secret, setting) interrupted by an auth challenge must be treated like a
  failed patch assert -- zero bytes until the "Updated now" timestamp is read back. Never
  dispatch a verify run before reading it. (GROQ_MODEL "update" that never saved; 2 dispatches burned.)
  **CHECKABLE: no** — about a UI write interrupted by auth; the platform holds no record
R-S78-2: A green run proves the pipeline completed, not WHICH path served it -- grep the
  probe/fallback prints before crediting the primary. (4 greens ran entirely on the 8b fallback
  while the primary 404'd all week.)
  **CHECKABLE: no** — 'which path served it' requires reading run logs for probe prints, per run
R-S79-1: Browser-UI steps are not executable in this partnership — every action ships as a runnable
  command; config writes go through gh CLI with byte receipts (gh secret list before/after). Never
  ship a gated command block in the same message as its gate. (S78's dispatch mistake repeated at S79.)
  **CHECKABLE: no** — about the deliverable form of an instruction in chat
R-S79-2: A deprecation list proves the list, not the runtime. Grep live logs before declaring a
  component dead or alive. (Lens-1 served HTTP 200 all week with a "shut down" model configured;
  MAD's byte-level comment beat a remembered search claiming gpt-oss adoption.)
  **CHECKABLE: no** — requires grepping live logs, which vary per run
R-S80-1: Binary patch anchors derive NL from the target file's own bytes (repo mixes LF and
  CRLF per file). A patch script that dies mid-sequence has written NOTHING — verify which
  files actually changed (git status) before staging; never commit a spec against unpatched code.
  **CHECKABLE: no** — patch-script rule; not committed
R-S80-2: An instrument certifies only the call-shape it holds. The MAD probe's arbitrator-shaped
  fixture validated a floor that 413'd on agent-shaped prompts. Budget math (prompt + max_tokens
  vs per-request ceiling, per-model quota buckets) precedes any uniform limit change.
  **CHECKABLE: no** — 'the call-shape it holds' requires comparing a fixture's shape to production's
R-S80-3: Speculation may flow but must not reach humans dressed as a finding. Label at output
  seams (estimative language), don't suppress — suppression creates its own lies. The gate acts
  on the shadow verdict; it never suppresses the recording of it.

## S81 EARNED RULES (2026-08-17)
  **CHECKABLE: no** — labelling speculation at output seams needs to know which claims are speculative

- R-S81-1 (Zero-match indicts the pattern first): A filter that returns no rows prints a BLANK
  line, which is indistinguishable from a broken filter, a bad field name, or an empty fetch.
  Prove the instrument saw data before reading silence as absence — count first
  (`gh run list -L 40 --json conclusion --jq 'length'`), then group. Born Aug 17: a cliff-survival
  check returned two spaces and was almost read as "zero failures". It was correct, but nothing
  in the output said so.
  **CHECKABLE: yes** — assert every guard proves its input was non-empty before reporting a zero

- R-S81-2 (Verify what ARRIVED, not what was fetched): Any consumer that assembles inputs under
  a budget must log what was INCLUDED against what was AVAILABLE. A guard that tests the fetched
  list passes whenever the fetch succeeds, and cannot detect its own starvation. Zero inclusion
  of a required input is a FAILURE, not a quiet loop break. Corollary: a failure that grows with
  upstream health does not look like a failure. Mirrors Lens LR-141, adopted by reference;
  GNI's own evidence pending the ROOT 1 audit.
  **CHECKABLE: yes** — grep budget assemblers for a paired INCLUDED-vs-AVAILABLE print

- R-S81-3 (Absolute allotments, never leftover budgeting): No consumer's share may be defined by
  what another consumer left over. Each tier gets an absolute allotment measured exclusive of
  every other tier; a total cap may exist as a backstop but must not be the allocator. When a
  tier drops content, log WHICH item was dropped by name — a count says the tier shrank, a name
  says which perspective was lost. Mirrors Lens's Mission Analyst finding.
  **CHECKABLE: yes** — grep budget code for a share computed from another consumer's remainder

- R-S81-4 (One load-bearing block per message; rollbacks never travel with applies): When a
  message contains a patch block, multi-block pastes get PARTIALLY executed — a commit block can
  run while its patch block does not, committing nothing and looking like success. And a rollback
  command sitting in the same message WILL eventually be pasted along with everything else.
  Offer recovery separately, on request, only after the apply is verified. Assume any block may
  run twice, out of order, or not at all. Mirrors Lens LR-140.
  **CHECKABLE: no** — one load-bearing block per message - a property of a chat turn

- R-S81-5 (A guard's expected value must be derived, not hand-counted): Any assertion whose
  expected number was counted by eye is a banked estimate living inside a tool built to stop
  banked estimates. Derive it from the same data the change is made from (sum the deltas across
  the edit list, do not count lines). Assert RELATIVE to the file's state read at the start of
  the patch, never absolutely — a hardcoded "this file must be LF" starts failing on files
  nobody touched the first time autocrlf converts them. Extends R-S80-1. Mirrors Lens LR-139.
  **CHECKABLE: yes** — SHIPPED C5: AST lint - no check function may hold a hand-written integer

- R-S81-6 (Grep the agreement, not the message): `git log --stat` proves message-vs-contents. It
  cannot prove contents-vs-agreement. Before committing a change agreed in conversation, grep ONE
  DISTINGUISHING PHRASE PER AGREED ELEMENT and report the hits; absence of a hit means that
  element did not land. The phrase must be unique by construction — a commit SHA proves nothing
  because SHAs legitimately recur in a document. Presence alone is not enough: assert UNIQUENESS
  whenever an ordered list gains an item. The trap stated plainly: producing text in conversation
  FEELS like shipping it, and the same illusion works on the reader. Mirrors Lens LR-138.
  **CHECKABLE: no** — 'contents vs agreement' requires knowing what was agreed

- R-S81-7 (Record requested time and observed time separately): The trap book recorded when crons
  FIRED and called it the schedule. YAML holds the request; run history holds reality; the delay
  is its own measurement and it drifts. S80 banked "1-3 hours late"; by Aug 17 the same crons
  fired 13-60 minutes late, and a wait anchored on the stale figure wastes a session. Requests:
  pipeline 02:13/10:13, MAD 02:43/10:43, grounding-watch 11:13 UTC.
  **CHECKABLE: yes** — assert no live doc states a cron time as a start time; the band must be emitted

- R-S81-8 (Groq refills continuously; there is no daily reset): TPD is a leaky bucket refilling at
  Limit/86400 per second — about 8,333 tokens/hour at a 200K limit, with no midnight anywhere.
  Recovering 50,000 tokens costs roughly six hours of wall clock. A live 200 carries exactly six
  x-ratelimit headers, all per-MINUTE; there is NO daily token header, so TPD is observable only
  from a 429 body or the console, and a 404 carries no rate headers at all (so any pre-flight
  reading them fails open on a dead model name). Any reasoning of the form "the quota resets and
  we start fresh" is reasoning about a fiction. Measured in Lens to the millisecond across seven
  readings; adopted here by reference, and GNI's per-account-day reservation model is unaudited
  against it (order item 4.3).

## S82 EARNED RULES (2026-08-17)
  **CHECKABLE: no** — a fact about how Groq refills; violating it means holding a wrong mental model

- R-S82-1 (To find an artifact, grep its STRUCTURE, not its name): A phrase-grep for a
  document's contents returns every file that MENTIONS it and hides the one that IS it.
  S82 ran `grep -rln "LOAD CHECK"`, got 30 handoffs back, and concluded from that noise
  that GNI's opening and closing prompts did not exist as artifacts. They existed the
  whole time, as PART C and PART D of `docs/GNI_Session_Transfer_Protocol.md`, and a
  heading-grep (`grep -nE "^#{1,4} "`) found them in one call. Sibling of R-S81-1: there
  a zero-match indicted the pattern, here a HIGH match count did. Match volume is not
  evidence in either direction; only the shape of the match is.
  **CHECKABLE: yes** — assert artifact searches grep a structural marker, not a phrase

- R-S82-2 (An instrument dumps the whole category, not the expected field): When adding
  measurement, log every member of the category under test, not the one the hypothesis
  names. S82's ARB-ARRIVAL instrument measured the article tier and skipped the four
  sibling tiers (constraint_block, R1, R2, R3, tail) that compete for the same budget --
  so when the arb prompt grows, the log will show articles shrinking without naming which
  tier ate the room, which is the very question the next item must answer. Corollary from
  Lens: a measurement that FALSIFIES the instruction that requested it is a success, not a
  failed mission. Design for that outcome.
  **CHECKABLE: no** — 'the whole category' requires naming the category under test

- R-S82-3 (A stopgap never closes a root): Capacity freed by a stopgap flows wherever the
  system routes it, not where the fix intended, so a stopgap's own cert cannot close the
  root it was aimed at. Evidence: C1 transcript-carry (S81) freed prompt room, certified
  PASS on its own terms (zero 413, zero empties, bill down) -- and the arbitrator gained
  nothing, still riding the FULL fit ladder to `ctx-trim@4983` three weeks later. A root
  closes on a measurement OF THE ROOT. Extends R-S69-2: a substitution without a debt
  record launders itself into fact; a stopgap without a root-measurement does the same.
  **CHECKABLE: no** — 'a stopgap never closes a root' - classifying a fix as stopgap is judgement

- R-S82-4 (When law changes, sweep the TEMPLATES): A template is law that executes itself
  in the next session. CONTRACT v4 moved the queue out of the handoff and into the order
  file; HANDOFF_S81 obeyed, but PART B of the Transfer Protocol still instructed the next
  session to build a `QUEUE (<=25 lines)`. Two closes would have restored the queue by
  template alone, silently undoing the change. R-S55-1's sibling sweep applies to docs:
  after any rule-of-engagement change, grep every template that encodes the old rule.
  **CHECKABLE: yes** — assert the Protocol's template fields match what the live HANDOFF contains

- R-S82-5 (Apply the law-vs-state test to the version log itself): "Law edited most
  sessions means target-level content leaked in" is a test that must be run against the
  contract's OWN edit history, not only its sections. GNI's CONTRACT reached v4 in six
  weeks; reading the log, v2 was a model roster (pure state, and already false -- it named
  Opus 4.8 while S82 ran on Opus 5) and v3 mixed a genuine rule of engagement with the
  model names that dated it. The leak was visible in the version log for three weeks and
  went unread because every review looked at the newest SECTION instead.

## S83 EARNED RULES (2026-08-24)
  **CHECKABLE: yes** — git log: count sessions in which CONTRACT was edited over a window

- R-S83-1 (A disclosed limitation is a CLAIM, not a fact): A limitation stated at ship time
  carries the same trust as any other unverified assertion, and it must be checked against
  the instrument's FIRST real output. S82 disclosed that ARB-ARRIVAL's `truncated=` would
  always read 0, reasoning that ctx-trim appends `'\n[ctx trimmed to fit]\n'` after slicing.
  It read 1 on the first run. The instrument never touches the assembled prompt -- it
  RE-DERIVES the slice as `arb_ctx_fit[:_keep]`, so the appended marker was never in the
  string the `endswith` test sees. The trap built on that disclosure said `dropped=N` means
  "at least N"; the bytes say it is EXACT and conservative-HIGH by one, because a partially
  delivered article is trimmed from `arrived` and counted as fully dropped. Carried into the
  ruling, the trap would have inverted it. A self-reported weakness is a lead like any other.
  **CHECKABLE: no** — a disclosed limitation is a claim - trust level has no byte form

- R-S83-2 (Novelty is an identity question; a content check cannot answer it): To prove an
  artifact is NEW, compare its IDENTITY against what has already been read -- never its
  contents. S83 issued a guard that accepted a fetched run if `ARB-FIT` appeared once. That
  test distinguishes the debate from the grounding-watch flavor and says nothing about
  freshness, so when `-L 1` returned the run already read that morning, every check passed
  and the block would have been logged as a second sample. Sibling of R-S81-1 and R-S82-1:
  there a zero-match and a high match count misled; here a CORRECT match on a stale artifact
  did. Compare ids, and print the id next to the claim.
  **CHECKABLE: no** — novelty is identity; no artifact records which runs have been read

- R-S83-3 (Read the clock in the block that makes the claim): Never state elapsed time, a
  schedule position, or "the next run is due about now" from turn count, from conversational
  distance, or from memory. S83 did it twice, calling a run late that was sixteen minutes
  early, and then called a run "this evening's" when six days had passed since the previous
  message. Both were resolved by one `date -u` that had not been asked for. Pair every wait
  estimate, deadline, and freshness claim with a clock read in the SAME command block --
  and the same for a repo: `gh` resolves its target from the git remote, so a `cd` out of
  the repo silently removes the world the command was meant to query.
  **CHECKABLE: no** — about reading a clock inside the block that makes a claim

- R-S83-4 (A cert that measures mechanics has not certified the instrument): Passing on
  finish_reason, absence of 413s, absence of empties, and "the output arrived" proves the
  PLUMBING survived a change; it says nothing about whether what flows through the plumbing
  is the same. Evidence from Project Lens: a July migration certified clean on mechanics, and
  three weeks later the same positions were extracting twice the actors and THREE TIMES the
  claims per row, while the headline consistency metric moved 0.834 -> 0.853 and hid it. GNI
  owns the same debt: the S80 MAD migration was certified on 413s and empties, and ROOT 2.3
  has been asking since July whether the arbitrator's verdicts changed. A behaviour cert
  needs a BAND measured before the change and re-measured after, from stored rows.
  **CHECKABLE: no** — distinguishing mechanics from instrument is the same counterfactual as R-S90-1

- R-S83-5 (A ritual document needs a path into the session that begins with a READ): A prompt,
  template, or checklist that reaches a session only by being pasted has no single source of
  truth -- the pasted copy and the repo copy drift, and nothing can detect the drift because
  nothing ever compares them. Byte evidence: `sed -n '/PART D/,/PART E/p' | grep -c
  "Transfer_Protocol"` returned 0. GNI's CONTRACT cited the prompts by path since v5, the
  protocol file existed and was correct, and no artifact in the repo ever instructed anyone
  to open it. Lens shipped the identical fix after discovering its pasted close prompt had
  silently lost two clauses present in the repo. Extends R-S82-4: sweeping templates when law
  changes is worthless if no template is ever read.
  **CHECKABLE: no** — requires the pasted opening prompt, which reaches no file

- R-S83-6 (Flow discipline does not protect a stock): Rate limits, per-minute pacers and
  per-day reservations all govern a FLOW, and a system fluent in flow control can be entirely
  blind to accumulation. Storage only grows; nothing consumes it back; and its failure is not
  a slow degradation but a hard refusal of every read at once. Project Lens ran sophisticated
  token-per-minute and token-per-day governors while its database grew unmetered to 287% of a
  free-tier quota, and went fully offline for nineteen days. GNI_Autonomous has `quota_guard.py`
  and ZERO retention code -- `grep -rn "\.delete()"` returns nothing. For every free-tier
  resource, ask whether it is spent or ACCUMULATED, and meter the accumulated ones. Corollary
  amending R-S81-6: read the METER, not the mail -- Lens missed two announcement emails a
  month apart and lost five positions to one and its whole database to the other.

## AMENDMENT TO AN EXISTING RULE (no new number -- R-S83 deliberately does not re-mint)
  **CHECKABLE: no** — flow vs stock - a modelling distinction, not a code shape

- R-S81-3 (AMENDED 2026-08-24): the existing rule says a count tells you the tier shrank while
  a NAME tells you which perspective was lost. Amended: the count must be of DISTINCT IDENTITY,
  not of rows. Project Lens's arrival check reported `s1=4/4` on a wave where all four rows
  were the same lens produced four times -- a perfect score over a single perspective. GNI's
  ARB-ARRIVAL has the identical blind spot: `arrived=20` counts lines beginning `'  - ['`, so
  fifteen geopolitical articles and five financial ones report exactly as four pillars would.
  Count the distinct category, then name the losses.
  *(This is an amendment rather than R-S83-7 on purpose: Lens re-minted a rule it already held
  and paid for the duplicate. Before minting a number, search the register for the rule that
  already says it -- and search BOTH ID schemes, `GNI-R-###` and `R-S##-#`, since a grep for
  one is blind to the other.)*

## S84 EARNED RULES (2026-08-25)

- R-S84-1 (A pure function is a free simulator -- do not derive a formula you can measure):
  Before writing a formula with a constant in it, check whether the code that produces the
  thing is PURE. If it is, call it again with the arguments you were about to model and take
  `len()`. S84 was about to size the arbitrator's context with an assumed ~138-char per-article
  overhead; the byte read gave the real cost as
  `21 + len(src) + len(title[:80]) + len(str(score)) + len(summary[:depth])`, which varies
  114-130 chars per article with source and title length -- so every fixed-overhead formula is
  wrong on every run. `_build_news_context` and `_assemble_arb` are pure, so ARB-DRYRUN
  measures four candidate depths per run at zero API cost. Satisfies R-S81-5 by construction:
  a guard value that was BUILT cannot have been hand-derived.
  **CHECKABLE: no** — 'measure instead of deriving' - the choice happens before code exists

- R-S84-2 (When two meters disagree, calibrate against the one that ENFORCES): A self-built
  meter must read the same number the platform bills and blocks on, not the number that is
  convenient to query. GNI's `pg_database_size` reports 93 MB; the Supabase panel reports
  113 MB against the 500 MB quota; the ~20 MB gap is platform-side and invisible from inside
  the database. Table-level figures agree EXACTLY (63.29 MB both ways), which is what makes the
  disagreement dangerous -- the instrument looks correct everywhere you can check it and is
  wrong precisely where it decides. A meter built on the internal number would have reported
  healthy headroom while the platform returned 402 on every read. Corollary to R-S83-6: read
  the meter -- and read the ENFORCING meter.
  **CHECKABLE: no** — which meter ENFORCES is a fact about the platform, not the repo

- R-S84-3 (A conclusion that was corrected but never WRITTEN DOWN as corrected will re-form):
  GNI-R-233 says reset to zero when corrected. S84 found the gap: a reset that lives only in a
  session's memory is not durable, and the same wrong conclusion re-forms in a later session
  with fresh confidence. S84 re-derived "the grounding gate is grounding against material the
  pipeline rejected" from `weak_articles` being in the basket -- a conclusion this project had
  already reset once, having established that score:0 -> Swan is BY DESIGN (the Johari
  weak-signal pool). Recidivism is worse than the original error because it consumes the
  correction's credibility. When a conclusion is reset, the reset itself is an artifact: write
  it where the next session will read it, or expect to pay for it twice.
  **CHECKABLE: yes** — assert every entry in a session's WRONG ledger has a home in a live doc

- R-S84-4 (PROMOTED FROM A TRAP carried unchanged twice -- `gni_mad.yml` holds two flavors):
  One workflow file runs BOTH the MAD debate and the 11:13 grounding-watch, so a run list shows
  two kinds of run under one name. Distinguish by the presence of `ARB-FIT`, never by time
  alone. S84 adds a second, WEAKER distinguisher observed 8/8: elapsed time separates them
  cleanly (~18-21s watch vs 11-14m debate), and the job list shows `grounding-watch` skipping
  in `0s` on a debate run. Use elapsed as a hint, never as the authority. Promoted rather than
  carried a third time, per CONTRACT v5: a trap copied forward unchanged twice has become an
  unregistered rule.

## AMENDMENTS TO EXISTING RULES (no new numbers -- search before minting)
  **CHECKABLE: yes** — assert MAD run classification keys on the ARB-FIT marker, never on run time

- R-S81-1 (AMENDED 2026-08-25): the rule says a zero-match indicts the pattern first, and that
  a filter returning nothing prints a blank line indistinguishable from a broken one. Amended:
  a REDIRECTED FAILURE is not silence, and is worse, because it produces a corpus.
  `gh run view --log > file 2>&1` writes the error message INTO the file, so the artifact
  exists, is non-empty, opens cleanly, and reads as valid text -- while every `grep -c` against
  it returns 0. S84 came one command away from reading "ARB-DRYRUN fired 0 times" off a
  one-line file containing a TLS handshake timeout, and would have gone looking for a bug in a
  correct instrument. `wc -l` BEFORE grep, on any cached or redirected artifact, always.

- R-S67-2 (AMENDED 2026-08-25): the rule says verify an instrument's RANGE (caps, truncation,
  short-circuits) before trusting its statistic. Amended: verify its EPOCH too. A cumulative
  counter and the data it counts can start at different times.
  `pg_stat_user_tables.stats_reset` read 2026-02-12 identically for every table in every schema
  -- the signature of a platform-side reset, not of first insert -- while `pipeline_articles`
  data began 2026-05-24, three hours after a TRUNCATE. Dividing live rows by the counter's
  192-day window instead of the data's own 92-day span understated growth by 2.1x and
  overstated the runway by 40%. A rate is rows divided by the DATA's span, never by the
  counter's.

- R-S85-1 (A lettered proposal without a lineage read is an opinion wearing a decision's clothes):
  R-S69-1 already said "read past session records before designing a fix for a lineage-bearing
  bug", and S85 skipped it TWICE in one session. The first skip cost a wrong story about a
  workflow env line. The second was worse: Claude proposed A/B/C on the arbitrator's context
  budget without reading [[gni-s83]], leaned option C (round-robin ordering), James chose C, and
  James then said in plain words that he chose it BECAUSE Claude urged it. DECISION S83-1 - which
  James himself had ruled - had already settled the direction as per-article COST and explicitly
  reasoned that ordering/allotment fixes CANNOT raise coverage because the share is already
  stable. So an unresearched lean overwrote an operator ruling, and the audit trail would have
  read "James chose C". The lesson is not "remember to read". It is that Claude's lean STEERS the
  ruling, so the read must happen BEFORE the proposal exists, and it must leave an artifact James
  can see is missing. Shipped as CONTRACT v7's LINEAGE-BEV gate with its `LINEAGE:` line.
  **CHECKABLE: yes** — grep every lettered proposal block in a close doc for a LINEAGE: line

- R-S85-2 (Grep human-facing COPY case-insensitively; grep code case-sensitively):
  The S85 census for stale model names ran `grep -rniE` on code identifiers but `grep -rn -e
  'llama'` on prose, and prose is where humans capitalise. `src/app/about/page.tsx:26` read
  `'Groq API (Llama 3)'` with a capital L, survived the census, and was the SECOND site named in
  S69 census flag F5 - a flag Claude had just finished reading. The site was fixed only because a
  re-run with `-i` found it. Identifiers are case-exact by nature; copy is not. When the target is
  something a reader will see, case-fold, and grep the SYNONYMS too (a model may be named as
  `llama-3.3-70b-versatile`, `Llama 3`, or `Llama 3 Local` on three different pages).
  **CHECKABLE: yes** — assert copy sweeps run case-insensitively and code sweeps case-sensitively

- R-S85-3 (An idempotency guard must test a string that exists ONLY in the patched state):
  An S85 patch guarded with `if replacement in data: ABORT` fired immediately - not because the
  file was patched, but because the replacement text `{ name: 'Groq API', role: 'Cloud AI` already
  existed on the NEXT LINE as pre-existing content. The guard asserted the anchor was unique and
  never asserted the sentinel was. Correct shape: the ANCHOR's absence is the proof of a completed
  patch (`if count == 0: already patched`), because the anchor is the thing the patch destroys.
  A sentinel drawn from the new text is only safe if it is asserted unique first, and if it is
  unique it is usually just the anchor's complement anyway.
  **CHECKABLE: no** — the guard string must be unique to the PATCHED state - needs both states

- R-S85-4 (A finding folded into another arc's scope DIES when that arc is declared achieved):
  S69 census flag F5 named TWO stale model-name sites and was routed with "F5 -> CLIFF scope
  (CLIFF-DOC)". The CLIFF arc was formally DECLARED ACHIEVED WITH EVIDENCE at S81. F5 was not in
  that evidence; one of its two sites was still live on the public site five weeks later, and the
  flag had no home left to be unclosed in. A phase transition audits its own definition of done,
  never the items other arcs parked inside it. Therefore: a finding folded into another scope must
  ALSO exist as a numbered item in the order, or the fold is a deletion with extra steps. At any
  ACHIEVED declaration, grep the closing arc's name across the census/register files first.
  **CHECKABLE: no** — 'folded into another arc' requires tracing a finding's routing history

- R-S85-5 (A register with no scheduled reader decays into an archive):
  `docs/DEBT_REGISTER_S69.md` was built by conversation_search archaeology across every GNI record,
  carries 131 lines, D-1..D-11, V-1..V-3 and a 13-row James-deferral ledger, received S70 and S74
  status appends - and then stopped on 2026-07-17. Ten sessions later no handoff, order file or
  contract referenced it, and S85 discovered it by accident while running a lineage grep. Its own
  text predicted this: "debt without an instrument decays into fact". The register WAS the
  instrument; nothing was the instrument for reading the register. A document that no prompt, gate
  or template ever opens is not a register, and creating one is not the same as closing the debt.
  Corollary: this is why LINEAGE-BEV greps `docs/` rather than naming files - the grep finds
  registers nobody remembered to cite.
  **CHECKABLE: yes** — assert every docs/*REGISTER*.md is referenced by a live doc or a workflow

- R-S85-6 (State the FAILURE TEST in the commit that ships the change):
  The S85 arbitrator fix went out with five pre-registered predictions and one explicit failure
  test ("GROUNDING SHADOW arb_hits must NOT rise; a rise means breadth did not buy grounding and
  the depth call was wrong") written into the commit body. This is the S82/S84 instrument
  discipline applied to a BEHAVIOUR change rather than a measurement: R-S83-4 says a cert on
  mechanics has not certified the instrument, and the only defence is to name, before the run
  exists, the observation that would refute the ruling. A cert that cannot fail is a ceremony.
  **CHECKABLE: yes** — git log: a feature commit's message must contain a FAILURE TEST line

- R-S86-1 (A baseline drawn from the most recent runs is not a baseline):
  S86 nearly banked the arb_hits baseline from the four S85 runs (mean 11.25). Widening to the
  twenty debates of Aug 17-26 gave mean 8.3, because the last four days were already running
  ~3.5 above the sixteen before them, for reasons still unknown. Had the narrow window been
  used, a post-change reading of 11 would have scored as "no rise" while sitting three points
  above the true centre. A pre-registered threshold inherits every drift inside its window:
  state the window's SPAN and check its head against its tail before the threshold is fixed.
  **CHECKABLE: no** — 'recent runs are not a baseline' - window width is a statistical judgement

- R-S86-2 (Two instruments printing the same word may not be counting the same thing):
  GNI publishes arbitrator grounding hits twice. The per-run line prints
  `len(grounding_shadow['arb_hits'])`, and `mad_protocol.py:753` extends that bucket with
  `_g['hits']` ENTIRE - dialect spans included. `check_grounding`'s own `hit_count` (L299)
  excludes dialect, and the watch digest excludes it per GT-1. S86 called the two figures'
  near-equality a cross-instrument confirmation; it was a coincidence of scales. Before
  comparing two numbers that share a name, read the code that produces each. Near-agreement
  between differently-computed numbers is a FINDING about the difference, never corroboration.
  **CHECKABLE: no** — two instruments printing one word - requires knowing what each counts

- R-S86-3 (A conditional that never evaluates False is not a conditional):
  `mad_protocol.py:989`'s `_high_escalation` gates a hard-constraint block onto the Arbitrator
  prompt "for HIGH/CRITICAL only". Escalation is pinned CRITICAL on 109/110 scored reports, so
  the branch fired 6/6 across three measured days with zero variance, and the False path has
  never executed in production - nor in the selftest, whose fixture hardcodes
  `'escalation_level': 'CRITICAL'`. A feature described as conditional must have its branch
  RATE measured before it is reasoned about as a condition, and an untaken branch is untested
  code however old it is.
  **CHECKABLE: yes** — measure over stored runs whether a conditional ever evaluated False

- R-S86-4 (A prompt is instantiated from the file's bytes, never from a chat transcript):
  S86 found the repo's PART D still headed `v3` while the file was v5, and still saying "The
  handoff is ATTACHED" while James's own paste said "The S84 close set is ATTACHED". Two agreed
  corrections from the S84 close had never reached the file, so the paste was AHEAD of the repo
  - the inverse of the drift Protocol v3 was built to stop, and invisible from either side
  alone. Therefore: at every open, PART D is copied from the highest-numbered protocol file and
  instantiated by substituting the session numbers; it is never copied from a chat, and a
  chat-authored amendment is never carried forward. Corollary of R-S82-4: when a close changes
  a prompt, the sweep is not done until the FILE holds the change.
  **CHECKABLE: no** — a prompt from bytes not transcript - about where a human read from

- R-S86-5 (A refuted prediction may be naming a missing condition, not a wrong fix):
  `228634c` shipped five predictions. The first post-change run refuted three of them; the
  second satisfied all five exactly. The two runs differed in one measured variable -
  `assembled` 43 versus 39 - so the predictions were true within a boundary they had failed to
  state. Before a refuted prediction is read as a wrong ruling, diff the runs for the variable
  that moved; if one exists and explains the split, the finding is a missing CONDITION and
  belongs in the order as a trigger, not in the wrongness ledger as a bad call. This does not
  soften R-S83-4: the failure test must still be pre-registered, and a test that cannot fail is
  still a ceremony.
  **CHECKABLE: no** — a refuted prediction naming a missing condition - interpretive

- R-S86-6 (Commit subjects carry intent that docs/ and conversation records do not):
  S86 read an always-on constraint block, found it enforced only the two pessimistic agents, and
  called it a bias defect. `git log -S 'NN-5' --oneline` returned one line - "hard correction
  channel - Black Swan + Ostrich enforced at code level for HIGH/CRITICAL" - which showed the
  asymmetry was deliberate and moved the defect to the stuck switch. `docs/` did not hold that
  design and the conversation search had not surfaced it. LINEAGE-BEV therefore has a third
  stage after `docs/` and `conversation_search`: `git log -S '<symbol>'` on the symbol about to
  be judged. Use it whenever the question is "why is this code shaped like this", because a
  commit subject is the only lineage written by the person who made the change.
  **CHECKABLE: no** — commit subjects carry intent - intent is not checkable

- R-S87-1 (An ABSOLUTE threshold cannot measure a PRE-SELECTED set):
  `escalation_scorer` counts danger words in the 22 articles the funnel already chose as the
  most escalatory available. The question "are these tense?" is answered by the selection, not
  by the world, so the score saturates whatever the weights are. Replayed over 192 stored runs,
  THREE designs failed identically: Mar-24 Fix-2 (`base=min(sum,7)`) 192/192 CRITICAL, an
  actor-word tier 0 runs changed, a rupture-word tier 187/192. Before tuning weights or lists,
  ask WHO SELECTED THE SET BEING SCORED. If selection precedes scoring, only a relative or an
  uncapped-magnitude reading can carry information.
  **CHECKABLE: no** — 'pre-selected set' requires knowing the selection that produced the set

- R-S87-2 (A cap that is always at its limit is censorship, not a safety rail):
  Production wrote `raw_score 19` and published `10`. Across 192 runs the uncapped range is
  10.3-26.8 (median 19.2) and every published value is 10.0. The correct diagnosis of a stuck
  instrument is "the outputs are too UNIFORM", not "too HIGH" - the first is repaired by
  removing the clamp, the second by lowering the scale, and S87 proved the second repair does
  nothing. A cap only earns its name if it is reached sometimes.
  **CHECKABLE: yes** — measure over stored runs: a published metric constant at its cap

- R-S87-3 (A single-regime corpus cannot be calibrated, only resolved):
  `pipeline_articles` begins 2026-05-24; the Hormuz crisis began in February. 100% of the
  measurable history sits inside one regime, so there is no pre-crisis baseline and a constant
  like "normal = 4-6" cannot be derived - hardcoding it would write the crisis in as normal and
  fail inverted when the world calms. Before fixing any constant, ask: WHAT IN MY DATA WOULD
  FALSIFY THIS NUMBER? If nothing could, it is a belief. Relative shape within the regime is
  still measurable; absolute levels are not.
  **CHECKABLE: no** — 'single-regime corpus' requires knowing the regimes in the data

- R-S87-4 (A shipped patch is not a wired feature - verify the CONSUMER CHAIN, not the edit):
  March 2026 added `score_breakdown` and `factors` to the scorer's return under GNI-R-117; the
  patch applied, `py_compile` passed, and the same session promised two front-end consumers.
  Five months later the fields were in the scorer's bytes, absent from `src/` entirely, and
  present in 0 of 191 database rows, because `main.py` copied 3 of the 7 returned fields into
  `report`. Producer + patch-applied proves nothing. Grep every consumer and check the store.
  **CHECKABLE: yes** — same detector as R-S69-3: a shipped field with no consumer in the chain

- R-S87-5 (MSYS/MINGW translates ARGUMENTS, not string literals - two proven bites):
  (a) `python - <<'PY'` with `open('/tmp/x')` inside fails while `wc -l < /tmp/x` in the same
  block succeeds: bash translates the redirect, the heredoc text is passed through untouched and
  Windows Python reads `C:\tmp`. Use paths relative to the repo (`../x.tsv`). (b) PROMOTED TRAP:
  `grep` silently ignores `--include` when the command also expands an unquoted variable of
  `--exclude-dir` flags; pass explicit PATHS on any census that matters.
  **CHECKABLE: no** — MSYS argument translation - a shell fact, not a repo predicate

- R-S87-6 (PROMOTED TRAP - scheduler lateness is a measured PROPERTY of the free tier, not an
  event): S86 recorded "the MAD schedule moved ~9.5h on Aug 27, cause unknown" and carried it as
  a trap. Measured over 133 scheduled runs since the Jun-23 cron move (`b27474e`, whose own
  subject reads "to reduce GHA scheduler drift"): median lateness 243 min in June, 177 in July,
  61 in August, tail past 10 hours - IMPROVING, not degrading - and ZERO runs missed in 67 days.
  Delivery is reliable; timing is not. Never infer run identity, novelty or ordering from the
  clock; use RUN ID, and for MAD use `ARB-FIT` to tell debate from grounding-watch.
  AMENDED 2026-08-30 (S88, promoting the S87 spacing trap on its second carry): where TWO
  schedulers lag INDEPENDENTLY, the GAP between them is a distribution, not the constant its
  cron comments claim. Measured over 8 pairs: real gap = 30 min designed MINUS (pipeline
  lateness - MAD lateness), median 15m02s, and on 2026-08-30 MAD `33318313852` STARTED at
  14:58:17Z while pipeline `33318041130` finished at 14:58:20Z - the order INVERTED by 3
  seconds with nothing raised. Pipeline duration is stable (6m02-6m35 over 12 runs), so the
  inversion law is exact: it flips whenever the lateness difference exceeds ~23m45s.
  **CHECKABLE: yes** — same check as R-S81-7: lateness must be emitted from observation, not recalled

- R-S87-7 (PROMOTED TRAP - name the DENOMINATOR at the print site):
  `_arb_asm` prints `fits=N/assembled` and never against `available`, so a ratio read from the
  log answers a different question than the reader assumes; `check_grounding` computes
  `checked_spans` and discards it at the print (F-86-2); the per-run shadow line and the watch
  digest count hits on different scales with the same word (7.4). Three instances, one defect:
  a printed ratio whose denominator is not named at the call site cannot be compared to anything,
  and near-equality between two such numbers is a coincidence, not corroboration.
  **CHECKABLE: yes** — grep ratio print sites and assert the denominator variable is named

- R-S88-1 (SQL and shell must never share a paste block - `->` IS a redirection):
  A JSON-path query pasted into bash does not fail; bash reads `->` as `> file` and `->>` as
  `>> file` and CREATES those files. S88 produced two 0-byte files named `raw_score` and
  `score_breakdown-` this way. With a real filename in the path the same paste TRUNCATES that
  file to zero, silently, with exit status 0. Every SQL block is labelled SQL EDITOR ONLY and
  is delivered in its own message, never adjacent to a runnable shell block.
  **CHECKABLE: no** — about paste blocks in chat

- R-S88-2 (A gate written for you is read LITERALLY; narrowing its scope is not judgement):
  The S87 LOAD CHECK said `design_bench.py` runs before any scorer OPINION. S88 reasoned that
  8.6 touched no threshold and therefore needed no bench - which was itself a scorer opinion.
  A gate's wording is the operator's instrument for catching exactly the reasoning that would
  skip it, so the moment a case for an exception feels sound is the moment to run the gate.
  **CHECKABLE: no** — 'read a gate literally' - narrowing scope is a reading, not a byte

- R-S88-3 (Absence from the LIVE file is not a dropped item - read the generations between):
  S88 asserted that 5.1/5.2/5.3 and a whole retire roster had been silently dropped, because
  they were missing from generation 7 and no disposition appeared in it. One grep across
  `GNI_TARGET_AND_ORDER_S8*.md` showed S84 had closed all three explicitly and PROMOTED 5.2's
  fallback half to 1.10. The order is regenerated, not cumulative: disposition lives in the
  CHANGED THIS REGENERATION of the generation that made it, and nowhere else. Never charge the
  retire clause from the live file alone.
  **CHECKABLE: no** — requires reading the generations between two files to see what moved

- R-S88-4 (Design the EXTRACTION for the question, or the command answers a different one):
  Three instrument failures in one session, all mine: `gh run view --log | head -60` returned
  60 lines of runner boilerplate and zero application output; `git log --oneline` was asked a
  question about DATES and carries none; `npm run build | tail -20` cut off the 40/40 page
  count the CONTRACT requires as the receipt. Name the FIELD the question needs and select it
  (`--json`, `--pretty='%h %ad %s'`, `grep -E 'Generating static'`); positional truncation is
  a guess about where the answer lives.
  **CHECKABLE: no** — design the extraction for the question - about command design before running

- R-S88-5 (A pillar at its CAP cannot be moved by editing its word list):
  8.7 proposed removing `ceasefire` from `GEO_SIGNALS` because it scores de-escalation as
  escalation. Replayed over 196 runs the change moved 0 runs, because GEO hits are min 8 /
  median 14 / max 19 against a cap of 5 - roughly half the 27-word list could be deleted with
  no arithmetic effect. Measure the pillar's headroom BEFORE proposing any list edit; where
  headroom is zero the only honest claims left are about the PUBLISHED evidence strings
  (`factors`, `signals_found`), not about the score. Extends R-S87-1 from thresholds to caps.

- R-S87-6 SECOND AMENDMENT (S89) — LATENESS IS MEASURED AGAINST THE SLOT, NEVER AGAINST THE
  PREVIOUS RUN. `gni_pipeline` has two crons, `02:13Z` and `10:13Z`, so consecutive runs are
  8h or 16h apart BY DESIGN. S89 read a 13h gap and called the pipeline overdue; measured
  against the slot the figure was 3h07, inside a band whose observed minimum that week was
  4h39. Compute `actual − slot`, and read the cron in the same block as the claim. The rule's
  first amendment (S88) already forbade counting by clock instead of by run id; this extends
  it to the arithmetic itself.
  **CHECKABLE: yes** — measure GEO pillar hits against its cap over stored runs

- R-S89-1 — LINEAGE-BEV APPLIES TO A FINDING, NOT ONLY TO A PROPOSAL. CONTRACT v7 requires a
  `LINEAGE:` line before PROPOSE. S89 shows the gate is one step too late: five of this
  session's seven false claims were FINDINGS asserted from bytes alone, before any proposal
  existed — "the levels table contradicts the engine" (it encoded the scheduler's bands, set
  in March), "the canary is structurally dead" (it is a regression alarm, proven to fire when
  forced), "the protection window leaves a 43-minute gap" (`BLACKOUT_WINDOWS` sits one line
  below and closes it), "adaptive has been dead 68 days" (it runs on Cerebras and logs 0 Groq,
  stated in the project's own public copy), and a cross-root diagnosis re-derived as new twenty
  turns after being read at session open. BYTES SAY WHAT IS; THE RECORD SAYS WHICH SIDE IS
  CANONICAL. Before calling two byte-level facts a contradiction, search for the decision that
  created the difference — two numbers that differ are often two different subjects.
  **CHECKABLE: yes** — same grep as R-S85-1, widened to every finding block

- R-S89-2 — "NO QUERY FILTERS ON IT" IS NOT "NOBODY NEEDS IT". Before proposing the deletion
  of stored data, find the PUBLISHED CLAIM it supports. S89 measured that ~96% of
  `pipeline_articles` rows are never selected and that every DB query filters
  `stage4_selected=True`, and proposed a retention policy on that basis. The March-2026 design
  record says those rows ARE the Explainable-AI audit trail — "every rejected article is
  visible with reason" — and eight consumers in `src/` render them. Deleting them would have
  falsified a public claim under a target named TRUTHFULNESS OF OUTPUT. The absence of a query
  is a fact about queries.
  **CHECKABLE: yes** — before a deletion proposal, assert the column has zero consumers in src/

- R-S89-3 (PROMOTED TRAP, second carry — a newly added column is indistinguishable from a
  broken one) — WHEN A COLUMN IS ADDED AND RENDERED BEFORE ITS FIRST WRITE, THE PAGE SHOWS THE
  SAME EMPTY MARKER A FAILED SHIP WOULD SHOW. `/autonomy` renders `Raw Magnitude --` after
  `ee813c0` until a pipeline run writes the first row — the identical `--` the never-written
  Lower Bound showed for months. State this in the ship note, name the run that will clear it,
  and never read the marker as evidence either way until that run exists.

---

## S90 EARNED RULES (2026-08-31)
  **CHECKABLE: yes** — DB: a rendered column must have at least one non-null row before its blank is read as a defect

**R-S90-1** — A CERT MUST DISCRIMINATE. Before reading any output as proof, ask what it would
look like if the change had NOT shipped. `/autonomy` renders `30 min` identically from the
hardcoded map and from the measured `0.5`, so the browser certified nothing; 9.9 and 9.10 are
shipped-not-certified for that reason alone. A cert whose PASS and FAIL states are
indistinguishable on live data is a ceremony. Kin of R-S85-6 and R-S89-3, and the reason 8.5
became the S91 mission: the system's own constant makes verification impossible.
  **CHECKABLE: no** — a counterfactual - what the output would look like had the change NOT shipped. No script can evaluate it, and it is the most load-bearing rule GNI holds

**R-S90-2** — An ID cited by a live document is law ONLY if the register contains it. S90
measured eight IDs cited by CONTRACT / order / handoff / protocol that appear in no
`GNI_RULES` file, and two of them — `GNI-R-037`, `GNI-R-076` — were being obeyed with each
other's meanings for 35 sessions, because both inferred meanings happened to be good practice.
A citation followed from inferred meaning is a banked pointer (R-S54-2) wearing the clothes of
law. Standing check at every close, five seconds:
`for id in $(cat <live docs> | grep -oE 'GNI-R-[0-9]+|R-S[0-9]+-[0-9]+|LR-[0-9]+' | sort -u); do grep -q -- "$id" GNI_RULES_S*.md || echo "CITED BUT NOT REGISTERED: $id"; done`
  **CHECKABLE: yes** — SHIPPED C1: cited ids diffed against registered + PART 0 manifest

**R-S90-3** — When a procedure is REVISED mid-session, re-emit its PRECONDITIONS with it. S90
wrote a keyfile rotation whose step 1 was "create the key in the dashboard and copy it", then
replaced the mechanism after finding the real ritual in the record and shipped only the three
commands — the precondition stayed in the superseded message. With no key in hand, a bare
Enter at the hidden prompt wrote an EMPTY secret, printed `✓ Set`, and took `gni_pipeline`
down. R-S79-1 forbids shipping a gate apart from its block; this is its mirror — a revision
that silently drops one.
  **CHECKABLE: no** — 're-emit preconditions' - about how a revision is communicated

**R-S90-4** — A rule invoked to DEFER one item binds every item of the same class in the same
session. S90 cited `LR-104` (production/schema/credential work needs a session opening, not a
tail) to defer item 3.2, and then, ten minutes later, urged a credential rotation that the
same rule covers. This is not forgetfulness; it is applying a rule as an argument for one
decision instead of as a constraint on all of them. When you reach for a rule to justify a
"no", check what else in view it says no to.

## AMENDMENTS TO EXISTING RULES (no new numbers — search before minting)
  **CHECKABLE: no** — binds a class of items within one session; the class is named by judgement

**R-S57-1 — SECOND AMENDMENT (S90).** The rule's own first sentence says line endings are
per-file AND PER-REGION; five later rules quietly narrowed it to per-file, and S90 read the
narrowed version. A single ten-line block in `autonomy/page.tsx` held THREE `\n` lines
followed by seven `\r\n` lines, so a multi-line anchor joined with either newline matched
zero times — twice, in two consecutive attempts. **The correct form: locate a multi-line
region STRUCTURALLY — match the first line, scan forward to the closing token — and never
join remembered text with any newline at all.** Single-line anchors remain immune and are
always preferred. This is CLUSTER A's tenth rule and its second live failure in one session;
the cluster, not the rule, is what must be read.

**R-S78-1 — AMENDMENT (S90).** The rule requires reading back the "Updated now" timestamp
before trusting a secret write. S90 did exactly that and was still wrong: the timestamp proves
a WRITE occurred, never WHAT was written, and `gh secret set` prints `✓ Set` for an empty
paste. **The discriminating check costs one dispatch: a workflow's env block prints
`GROQ_API_KEY: ***` when the secret is set and `GROQ_API_KEY: ` when it is empty, so
`gh run view <id> --log | grep -m1 'GROQ_API_KEY:'` distinguishes the two states that the
receipt cannot.** R-S68-2 said a log can prove a secret is SET but not what it contains — this
is the seam inside that rule: SET vs EMPTY is exactly what the log CAN prove, and it is the
only failure mode a rotation actually has.

**R-S81-5 — INSTANCE (S90), no amendment needed.** The rule already says a guard's expected
count is DERIVED from the edit list, never hand-counted. S90 copied `formatInterval == 3` from
the `/autonomy` patch into the `/health` patch, where one render site rather than two makes 2
correct; the assert aborted before any bytes were written. The rule worked. Recording the
instance because the same session ALSO hand-counted "62 unique item ids" for the order file
when the measured answer was 60 — same error, a document instead of a patch.

---

# S91 APPENDIX (2026-09-01) — RULES EARNED, AND AMENDMENTS TO EXISTING ONES

Five new rules, three amendments. Both ID schemes were checked before minting: highest
`R-S##-#` was `R-S90-4`, highest `GNI-R-###` was `GNI-R-242`. No gaps opened.
R-S91-5 is a TRAP PROMOTION, not a fresh lesson: it rode forward once and CONTRACT bans a
second unchanged carry.

**R-S91-1 — A WIRING COMMIT MUST SWEEP TEST CALLERS, NOT ONLY CODE CALLERS.**
`c3ce662` (S51) wired `compute_depth` into `run_mad_protocol` and swept the five
`_build_news_context` call sites INSIDE the function. It never listed the function's own
callers. Three of them were harnesses passing `all_articles=[]`, and they have raised
`ZeroDivisionError` for over two months with nobody noticing. A test that cannot run reports
nothing, so its silence is indistinguishable from success. This is R-S55-1 extended: the
sibling sweep covers code consumers, DOC consumers (R-S82-4) and now TEST consumers.
  **CHECKABLE: yes** — the harness job already runs this: a wiring commit whose test callers were not swept fails on import

**R-S91-2 — A BUNDLE CLAIM IS A CLAIM. VERIFY EACH ITEM'S CONDITION SEPARATELY.**
Generation 10 declared item 8.5 "load-bearing for FOUR items". S91 measured each condition and
found them mutually exclusive: 8.5 needs score < 7, 9.9 needs score 9.0-9.4, and 8.10 lives in
a different module entirely. A mission's declared value is an estimate made at the previous
close, when the conditions were not yet read. Read them at the open, before the mission is
worked, and say so if the bundle does not hold. Kin to Protocol 8e (a blocker is a claim).
  **CHECKABLE: no** — verifying each item of a bundle separately - the bundling is a claim in prose

**R-S91-3 — A GREP THAT ORs SEVERAL PATTERNS CANNOT BE USED AS A COUNT.**
`grep -icE 'node(js)?[ .]?(16|20)|deprecat'` returned 12 on a workflow log and was reported as
a Node-20 warning count. It was summing three unrelated things: the Node-20 banner, a
`punycode` DEP0040 notice, and pip's `deprecation` package name. The true Node-20 count was 0.
One pattern per number. If a count decides a cert, the pattern must match exactly the thing
being certified and nothing else. CLUSTER-adjacent to R-S88-4 (the instrument lies quietly).
  **CHECKABLE: yes** — lint count-producing greps: an ORed pattern may not be used as a count

**R-S91-4 — A CLASSIFICATION GREP IS A HYPOTHESIS, NOT A SAFETY GUARANTEE.**
Before running ten harnesses, S91 classified them by `grep -cE 'create_client|get_client|Groq\(|requests\.|httpx'`
and treated `net=0` as "safe to run". `dryrun_rate_governor.py` scored `net=0` and then printed
`APIConnectionError ... backoff 14.8s` — it reaches the network by a path the pattern did not
name. No harm resulted, which is luck, not method. When a classification gates an ACTION with
side effects, bound the action too (timeout, dry-run flag, offline env) rather than trusting
the classification alone.
  **CHECKABLE: no** — premise disproven at S91 (item 5.19); a classification grep's status is interpretive

**R-S55-1 — NEW AMENDMENT (S91).** The sibling sweep now has three documented classes of
consumer: code (S55), documents and templates (R-S82-4, S82), and TESTS (R-S91-1, S91). The
test class is the one that fails silently, because a dead test and a passing test are both
quiet. When a shared function's signature or preconditions change, `git grep -n '<symbol>('`
across `*.py` INCLUDING `tests/` is the sweep, and the count of callers is stated before the
grep is run.

**R-S87-6 — THIRD AMENDMENT (S91): the lateness band is WIDER than recorded and must be
re-measured, not recalled.** S87 measured median lateness 243 min (Jun), 177 (Jul), 61 (Aug)
over 133 runs; S89's order recorded a band of 4h39-6h05. On 2026-08-31, eight scheduled slots
measured against their crons gave: pipeline +6h25 and +7h24, MAD +6h11 / +6h58 / +6h46, graph
+6h03 / +6h45, selfbias +7h11 — a band of **6h03 to 7h24, entirely above the recorded one**,
with zero runs missed. Delivery stays reliable; timing is a distribution that moves. Quote the
band with the date it was measured, or re-measure it.

**R-S81-5 — THIRD INSTANCE (S91), and the rule is now a hard precondition for the close.**
The rule says an expected count is DERIVED, never hand-counted. S90 hand-counted "62 unique
item ids" when the answer was 60. S91, at its own close, stated "expected 62 unique ids" in
advance and measured **47** — the same wrong number, one session after recording that it was
wrong. The advance count exists to make a miscount visible, and it worked both times, which is
why this is an instance and not a new rule. From S92: the expected count is obtained by
grepping the PREVIOUS generation and adding the delta, never by recalling a figure.

**R-S91-5 — A SECRET'S BLAST RADIUS IS THE SET OF WORKFLOWS THAT READ IT. ENUMERATE BEFORE
ROTATING.** (Promoted from S90's standing trap at the S91 close; it had ridden forward once.)
`GROQ_GNI_NOT_MAD` feeds one workflow, so its rotation certified on one run. `GROQ_API_KEY`
feeds THREE — `gni_mad` (morning slot), `gni_adaptive` and `gni_heartbeat` — so rotating it is
not the same operation, and it is not certified until one scheduled run of EACH of the three is
green. Before any `gh secret set`, run `git grep -n '<SECRET_NAME>' -- .github/` and state the
count. Pairs with R-S78-1's amendment: a bare Enter at the hidden prompt writes an EMPTY secret
and still prints the success tick.


## S92 (2026-09-01) - EARNED THIS SESSION
  **CHECKABLE: yes** — SHIPPED C2: workflow/trigger counts derived from YAML vs section 7.1

**R-S92-1 - A DEADLINE MUST NAME THE EVIDENCE THAT SET IT.**
A deadline whose originating evidence cannot be named is not a deadline; strike it.
KEYFILE ROTATION carried "OVERDUE since Aug 9" through ELEVEN order generations. The
date's origin is in no session record. Two March policy documents disagree on the
cadence (handbook 12.1 says six months or on exposure; the SWOT's D1 says monthly)
and the order cited neither. S90 had already measured PHISH-HW clean - logs, OAuth,
PAT tabs, all three - so no exposure evidence existed either. Cost: three sessions
of attention and one outage, for zero change in posture. GRAVEYARD protects DESIGNS
from being re-minted; nothing protected a DATE. (DECISION S92-1.)
  **CHECKABLE: no** — a deadline's originating evidence lives in session history, not beside the date

**R-S92-2 - SELECTING BY POSITION INTO A GROWING COLLECTION DECAYS.**
Select on a RELATION, never on an absolute offset. Fired TWICE on 2026-09-01:
"Aug 9" above, and `limit(332)` in `api/health/route.ts` - chosen because SQL put
the discriminating row at position 332, stale within hours when the next pipeline
run pushed it to 333. Fixed by selecting rows where the stored interval DIFFERS
from the published band, which cannot go stale. Same shape, two layers apart.

**AMENDMENT to R-S91-4** (a classification grep is a hypothesis): match the pattern's
CHARACTER CLASS against the real identifier before trusting a miss. `[A-Z0-9_]` cut
`TELEGRAM_QSChannel_ID` at the lowercase `h`, producing `TELEGRAM_QSC` and a reported
"missing secret" that did not exist. The system was healthy; the instrument was not.

**AMENDMENT to R-S90-1** (a cert must discriminate): the discriminating evidence must
be VISIBLE ON THE SURFACE THAT ITEM IS ABOUT. `416a2fb` widened the API window and the
proof appeared only in the JSON while the page still rendered ten identical rows - a
cert that exists only in a payload has not been published. `9d2dba8` closed it.

---
  **CHECKABLE: no** — position-decay lives in HOW the constant was derived, not in the call site. limit(1000) and limit(332) are byte-identical in shape and both carry .order(). Three check designs died against measurement this session

## R-S93-1 - AN INSTRUMENT'S EXPECTED OUTPUT IS CHECKED BY THE SCRIPT, NOT BY THE EYE.
S93 wrote a verification script whose own probes were wrong twice in one session:
`b"\\n"` searched for a backslash and an `n` rather than a newline, so the line-ending
test could only ever answer "LF" - the answer arrived by DEFAULT, not by measurement -
and a hand-counted expectation of 3 was really 2. Both were invisible while a human
compared the printed numbers to a sentence written minutes earlier. The fix is
mechanical: state every expectation as data (`want`), let the script compute `got`,
print `OK`/`BAD` per probe and one `ALL PASS`/`ALL FAIL` verdict. Include at least one
CONTROL probe that MUST match, so a silent instrument failure cannot masquerade as a
clean result (R-S81-1 extended from greps to verification scripts).

## AMENDMENT to R-S82-4 (a sibling sweep must cover DOCUMENT consumers)
Extend the sweep to the JUDGMENT A TEMPLATE ENCODES, not only the names, paths and
version strings it mentions. Protocol Part D has required distinguishing the MAD debate
from the 11:13 grounding-watch by `ARB-FIT` presence since v6; Part B's STATE line asked
for `L2 MAD: {one line}` and every close filled it with a bare count. The law was right
and the template quietly deleted it, so the same mis-read happened at the S92 close and
again at the S93 open. A blank in a template is a place where a rule can be lost.
Fixed in Protocol v11: the field is now `{N debate + M watch, by ARB-FIT}`.

## AMENDMENT to R-S91-4 (a classification grep is a hypothesis) - THE PREMISE WAS WRONG
R-S91-4 cited `dryrun_rate_governor.py` as a harness that "reaches the network by a path
the pattern did not name", on the evidence of a printed
`APIConnectionError ... backoff 14.8s`. S93 ran that harness in CI with NO secrets and no
reachable Groq endpoint: the identical line printed and the harness reported
`RESULT: 30/30 checks passed`, exit 0. The line is section (f) of its own test plan -
`getattr` guard, exceptions without `.response` - a STUB it constructs itself. The
`net=0` classification was correct; the log line was mis-read. **The rule's CONCLUSION
stands and is unchanged** - bound the action with a timeout and an offline environment
rather than trusting a classification - but it now rests on the argument, not on that
specimen. A rule whose evidence is withdrawn must say so; otherwise the next session
cites a fact that has been disproven.


---

## S94 (2026-09-02) — EARNED RULES

Each rule below carries a **CHECKABLE** marker, which is S95's mission format used one
session early. CHECKABLE means a script can decide it without a model reading prose.
  **CHECKABLE: yes** — assert every tool in tools/ has a control-probe or selftest path

- **R-S94-1 — A REVIEW FROM ANOTHER SESSION IS A LEAD, AND SO IS ITS CHECKING COMMAND.**
  Protocol 6 already says handoff claims are leads; this extends it to the COMMAND a
  reviewer hands you. BEV the instrument, not only the assertion. S94 was given
  `grep -c '^## '` to prove the architecture document was intact; that command returns 13,
  not the 12 the reviewer expected, because `## ROADMAP TO LAYER 2` is also a heading — it
  would have read as breakage in a healthy file. The check actually run was an `awk` strip
  of section 7 followed by `diff`, which answers the real question by bytes.
  **CHECKABLE: no** — it governs judgement about instruments.

- **R-S94-2 — COMPARE AN IDENTIFIER IN THE FORM THE PLATFORM STORES IT.** GitHub folds
  secret names to upper case. `tools/gni_state.py` compared them by bytes and reported
  `TELEGRAM_QSChannel_ID` as **NOT STORED** in the same table where `TELEGRAM_QSCHANNEL_ID`
  sat stored and unused — one secret rendered as two rows, one of them a phantom defect a
  later session would have hunted. Fold before comparing; keep the spelling the source uses
  for display. **CHECKABLE: yes** — assert no two rows of a generated inventory differ only
  by case.

- **R-S94-3 — A CLI'S OUTPUT SHAPE DEPENDS ON WHETHER IT IS A TTY.** `gh secret list`
  prints a header to a terminal and NONE through a pipe, so a parser that always drops
  line 1 silently under-counted 22 stored secrets as 21. It did not crash; it just lost
  one row, and the lost row would have read as "this secret is not stored". Detect the
  header, never assume it. Verify a parsed count once against the count seen by eye.
  **CHECKABLE: yes** — assert the parsed count equals the row count of the raw output.

- **R-S94-4 — BUILD AN INSTRUMENT AGAINST A FIXTURE BEFORE THE REAL TREE.** S94's
  generator was run against a four-workflow fixture that mimicked the real shapes before it
  ever touched the repo. The fixture caught FOUR bugs the real tree would have hidden: the
  script counted itself as a consumer of every secret it names; a substring match let
  `GROQ_MODEL` swallow `GROQ_MODEL_FALLBACK`; a second job's `pip` list overwrote the
  first's, erasing the exact evidence item 6.9 exists to hold; and the entrypoint filter
  dropped `adaptive_pipeline.py` because the word "pipeline" contains "pip".
  **CHECKABLE: no** — it governs how work is sequenced.

**Note on R-S93-1, unchanged but now load-bearing.** S94's control probe fired for real:
breaking one regex on purpose produced `EXIT=2` with nothing written, and two of its seven
probes encode errors made during S94 itself, so they are regression tests rather than
hypotheticals.

# S95 APPENDIX (2026-09-03) — RULES EARNED

Five rules, all earned from instrument errors made inside this session. Six of
the seven were caught before the real tree; two reached the operator's terminal.

**R-S95-1 — VERIFICATION IS COMPUTED BEFORE THE WRITE, NEVER AFTER IT.** A patch
  script whose report runs after the mutation is not a report. S95's YAML patcher
  crashed on a `%`-precedence bug in its own `print` — AFTER the file was already
  written. The mutation succeeded and the verification died; had the mutation been
  wrong, the same crash would have hidden it. Compute the expected delta, compare
  it, refuse on mismatch, and only then open the file for writing. Kin to R-S55-3,
  which required confirming a patch RAN before trusting a verify; this requires
  confirming it will be CORRECT before it runs.
  **CHECKABLE: yes** — AST-lint patch scripts: no write call may precede the last assert

**R-S95-2 — ACCEPTING A CORRECTION REQUIRES READING A BYTE, NOT THE CORRECTOR'S
  CONFIDENCE.** S95 accepted a review's correction about `sort -V`, wrote a
  self-criticism, and was then told the correction had itself been a misreading.
  Four times in one session a review reasoned from an assumed tree rather than the
  live one — and each time it also carried something true, so neither deference nor
  dismissal was safe. R-S94-1 says a review is a lead; this says its CORRECTION is
  a lead too. Over-confession is as false as over-confidence and is harder to catch
  because it wears good manners.
  **CHECKABLE: no** — whether a byte was read before agreeing leaves no trace in any artifact

**R-S95-3 — A DOCUMENT THAT RECORDS A DEFECT IS INDISTINGUISHABLE, TO A DETECTOR,
  FROM ONE THAT COMMITS IT.** Item 9.16 records the wrong workflow count as a
  finding; a grep hunting wrong counts cannot tell it from a document making the
  claim. CONTRACT names `GNI-R-064` while describing the citation defect; a grep
  hunting dangling citations flags it. Every check that runs over DOCUMENTS needs a
  citation escape, or its remedy becomes "delete the record of the defect" — and
  GNI is built entirely on records of past defects. The escape must not be an
  inline convention: backticks were proposed and disproven within the hour, because
  `GNI-R-114` is backticked AND load-bearing. The escape is a MANIFEST with a
  status per id, in the register.
  **CHECKABLE: yes** — assert every document-scanning check declares an escape source

**R-S95-4 — A CONSTANT COUNT IS NOT A CONSTANT STATE.** S90 measured eight rule ids
  cited but unregistered. S95 measured eight. Four of S90's eight were fixed and
  four new ones accrued: the number held while HALF the membership rotated. A
  metric compared across sessions must be compared as a SET, not as an integer, or
  a fully-rotated population reads as stability. Kin to R-S54-2: the live byte beats
  the banked number, and here even a live number that MATCHES the banked one is
  concealing a change.
  **CHECKABLE: yes** — store the members, not the count, and diff the sets between generations

**R-S95-5 — THE TOOL THAT WRITES A FILE BECOMES THE INPUT TO EVERY TOOL THAT READS
  IT.** S95's marker script wrote `\r\r\n` on every line of the register. All five
  new checks stayed GREEN, `git status` said nothing, markdown rendered identically
  — and `tools/gni_state.py` died with an `IndexError` that took three probes to
  trace back. One reader's green proves nothing about another reader's input. After
  any write to a shared artifact, run every tool that consumes it, not only the one
  that motivated the write.
  **CHECKABLE: yes** — CI runs every tool in tools/ against the tree after any docs/ change

## S96 EARNED RULES (2026-09-03)

- R-S96-1 - A GENERATED ARTIFACT IS NOT BOUND BY A NAMING LAW ITS GENERATOR DOES NOT KNOW.
  `tools/gni_macro_map.py` names its output after the register generation it read, so the
  artifact landed as `GNI_MACRO_MAP_S95.md` at the S96 close. Renaming it by hand is undone by
  the next run, so the fix is an argument to the generator, never a `git mv`. Until a generator
  takes the session number, its output sits OUTSIDE "highest number = live" and the exception
  must be written down where the next session will read it.
  **CHECKABLE: yes** - assert every file in `docs/` matching `_S[0-9]+\.` was produced under
  the current session number, or is named in a written exception list.

- R-S96-2 - A CHECKSUM PUBLISHED WITHOUT THE COMMAND THAT REPRODUCES IT VERIFIES NOTHING.
  The S95 LOAD CHECK ordered the graveyard carried with md5 `203d371bc1d5522cd259ed1daf4bb0ab`.
  S96 tried fourteen spans of the live file - section, table, rows, with and without the
  heading, LF and CRLF - and reproduced none of them. The same LOAD CHECK line says, two
  clauses later, that the METHOD is written beside the number. The checksum broke the rule
  standing next to it. Any figure a handoff asks a later session to VERIFY ships with the
  literal command, or it is decoration.
  **CHECKABLE: yes** - assert every md5/sha in a handoff or order file has a fenced command
  within three lines of it.

- R-S96-3 - A REGISTER WITH MORE THAN ONE ENTRY SHAPE CANNOT BE PARSED BY AN ANCHORED PATTERN.
  `GNI_RULES` uses at least six shapes for a rule entry (`- **ID** -`, `**ID** -`, `ID: text`,
  `- ID (Title):`, `## ID - TITLE`, `- **ID - Title:**`) and some CHECKABLE markers sit BELOW
  the heading that follows their rule (`:289`, `:589`, `:1305`, `:1347`). A first parser bound
  103 of 159 markers to ONE rule and reported no error. Count the markers first, bind each to
  the nearest entry-start above it, and report what cannot be bound as AMBIGUOUS - never
  attribute by guess and never let a silent collapse look like a parse.
  **CHECKABLE: yes** - assert marker count equals bound + ambiguous + unbound, and that no
  single id claims more than one marker without appearing in the ambiguous table.

- R-S96-4 - A PLATFORM PATH SEPARATOR INSIDE A GENERATED ARTIFACT MAKES ONE INPUT PRODUCE TWO
  FILES. `os.path.join` wrote `docs\...` on Windows and `docs/...` on Linux. Byte COUNT,
  marker count, bound count, session count and the Z ratio were all identical - every figure in
  the summary line agreed - and the md5 differed. An acceptance test built from the summary
  line could not see it; the reviewer's own `head -25` did. Generated text is built with `/`,
  and the artifact asserts no backslash reached it before the write.
  **CHECKABLE: yes** - assert no generated file under `docs/` contains a backslash path.

- R-S96-5 - AN ADVISORY SESSION LEAVES NO NUMBERED ARTIFACT, AND ITS ABSENCE IS DECLARED.
  S97 was held in a separate chat: no commits, no `*_S97.md`. A gap in the session numbers is
  indistinguishable from a lost close set, and the completeness check is "re-read the END of
  the previous record" - which would find nothing. The handoff that skips a number says so in
  its title and in one line at the top, or the next session pays to search for a session that
  never existed.
  **CHECKABLE: no** - requires knowing that a session happened outside the repo; no byte in the
  tree records it.


## S98 EARNED RULES (2026-09-04)

- R-S98-1 - A ONE-LINE RESTATEMENT CAN INVERT THE RULING IT SUMMARISES. Generation 16's
  phase-transition re-classification compressed item 5.17 into "Allowlist, paired with 5.14".
  Generation 13 had said the opposite in full: build the allowlist ONLY if 5.14 is deferred
  again, because an allowlist legitimises the red rather than clearing it (DECISION S93-1).
  S98 opened, read the compressed line as a thing to ship, and would have built it had the
  session record not been searched first. When an item's text is compressed, the compression
  carries the DECISION id that governs it, or the item keeps its full disposition.
  **CHECKABLE: yes** - assert every order item whose text names a `DECISION S##-#` in
  generation N still names that id in generation N+1.

- R-S98-2 - A COUNT IN A HANDOFF IS PERISHABLE; THE COMMAND IS NOT. The S96 close wrote
  "L2 MAD: 2 debate + 1 watch" as a STATE field. By the next morning it was six unread runs,
  because 2 debate + 1 watch is the DAILY UNIT, not a state - one line of `gni_mad.yml`
  produces it every day. An integer that a cron changes is a photograph presented as a fact.
  Any L1-L5 field a schedule can move ships the COMMAND that re-measures it, and the reader
  runs it at open before quoting it.
  **CHECKABLE: yes** - assert every numeric L1-L5 field in a handoff STATE section has a
  fenced command inside its own bullet.

- R-S98-3 - A HASH A GENERATOR PUBLISHES IS EOL-INVARIANT OR IT IS PLATFORM NOISE.
  `tools/gni_macro_map.py` printed `hashlib.md5(raw)` over the register. `read()`'s docstring
  claimed CRLF immunity, and that immunity covered `splitlines()` only. `git ls-files --eol`
  shows the register alone at `i/lf w/crlf`, so the same content hashed to two values
  depending on which machine ran the generator - and item 5.26's check was about to compare
  them. Strip the BOM, fold CRLF to LF, then hash. Anything a later check will compare must
  be computed from what the content IS, not from how git handed it over.
  **CHECKABLE: yes** - assert no generator under `tools/` calls `hashlib.*` directly on the
  return of a raw file read without normalising first.

- R-S98-4 - A PATH COPIED OUT OF A TRACEBACK IS NOT A PATH. Python prints the frame as
  `ai_engine/tests/../analysis/mad_protocol.py`; the `..` is unresolved and the string opens
  from nowhere the tool chain stands. Four commands in one block failed on it. The traceback
  names the SYMBOL correctly and the path only incidentally: resolve with
  `grep -rn '<symbol>' --include='*.py'`, never by transcribing the frame.
  **CHECKABLE: no** - a transcription error in a chat leaves no byte in the tree.

- R-S98-5 - A PLACEHOLDER INSIDE A FENCED BASH BLOCK IS AN INSTRUCTION TO THE SHELL.
  `<newest_id>` and `<id_of_the_new_run>` were both pasted and both became redirect errors,
  the second AFTER the first had already been logged as wrong in the same session. A block
  fenced as `bash` is a promise that it runs as written. If it needs a value the writer does
  not have, the block COMPUTES it (`id=$(gh run list ... --jq ...)`), or it is not fenced as
  bash.
  **CHECKABLE: yes** - assert no ```bash block in `docs/` contains an unquoted `<...>` token.

- R-S98-6 - A COUNTING COMMAND COUNTS WHAT IT MATCHES, NOT WHAT YOU MEANT. Generation 16
  published `grep -oE '\*\*[0-9]+\.[0-9]+' | sort -u | wc -l` beside the number 36, after
  S96 had already corrected 41 (counted by LINES) to 36 (counted by this grep). Both were
  wrong: the grep counts BOLD-PREFIXED heads, and eleven items ride inside grouped lines such
  as `**5.22 / 5.23 / 5.24 / 5.25**` where only the first id follows a `**`. The file held 47.
  Publishing the method does not make the method right - run it against a second,
  differently-shaped scan of the same span and reconcile the difference before publishing.
  **CHECKABLE: yes** - assert the order's stated item count equals the count returned by its
  own printed command AND that every `N.N` id in the ORDER span is immediately preceded by `**`.

## AMENDMENT to R-S90-1 (a cert must DISCRIMINATE) - WHERE THE NEGATIVE ARM MAY LIVE

S98 shipped item 5.26 (C6) without pushing a deliberate break to `main`. The negative arm lived
in `tools/gni_rule_checks_fixture.py` as three new families - `12-map-stale-count`,
`13-map-stale-md5`, `14-map-missing` - which exercise the SAME function through the SAME entry
point and run as the first step of the same CI job. DECISION S98-4: a fixture family satisfies
R-S90-1's negative arm when it (a) drives the identical code path, (b) is executed by CI on
every push, and (c) asserts its own expected verdict. A break pushed to `main` remains required
when no such harness exists - which is why 5.14's cert did push one (`447ce55` RED, `328be08`
GREEN, `git diff HEAD~2` empty).

## S99 APPENDS (2026-09-04)

- R-S99-1 - AN INSTRUMENT BOUNDED BY THE THING IT MUST BE INDEPENDENT OF REPORTS ITS SMALLEST
  ANSWER EXACTLY WHERE THE TRUTH IS LARGEST. Section 6 needed cron lateness. The obvious
  measure - distance back to the nearest declared slot at or before the run - is bounded by the
  slot SPACING, so on a 30-minute cron a run 365 minutes late reads as 5 minutes late. The
  number is small, confident and wrong in the direction that hides the problem. Before trusting
  a measure, ask what its maximum possible output is; if that ceiling is set by the quantity
  being measured, the measure is an artefact. The fix here was ordered matching, which has no
  ceiling, and which refuses when the pairing cannot be defended.
  **CHECKABLE: no** - the defect is in a measure's algebra, not in a byte pattern.

- R-S99-2 - A DELIVERY GUARANTEE AND A TIMING GUARANTEE ARE DIFFERENT GUARANTEES, AND MEASURING
  ONE SAYS NOTHING ABOUT THE OTHER. R-S87-6 records "delivery stays reliable; timing is a
  distribution that moves", measured over 133 runs at S87 and 8 slots at S91. Every one of those
  slots belonged to a cron firing 1-3 times a day. S99 measured the two crons firing 48 times a
  day and found 282 and 292 of 768 declared slots delivered over 16 complete days. The recorded
  claim was true of the workflows that were checked and false of the two that were not. When a
  property is asserted of a system, name the population it was measured over.
  **CHECKABLE: yes** - assert every published reliability claim in `docs/` names the workflows
  or runs it was measured over.

- R-S99-3 - A RUN IS EVIDENCE ABOUT THE SLOT IT SERVED, NOT ABOUT THE DAY IT STARTED ON. Counting
  runs by creation day published a per-day delivery of 114 percent for `gni_market.yml`: with 12
  hours of lateness a Friday 20:00 slot lands on Saturday and is counted against a day that
  declared it nothing. A ratio above 100 percent is not noise, it is incoherent, and it reads as
  a defect in the system rather than in the arithmetic. Attribute by the paired slot wherever a
  pairing exists; where none does, say which fallback was used inside the output.
  **CHECKABLE: yes** - assert no generated document under `docs/` publishes a percentage above
  100 in a delivery or coverage column.

## AMENDMENT to R-S98-6 (a counting command counts what it matches) - FOUR MORE INSTANCES

S99 committed the same error four times in one session, which makes it a standing hazard rather
than a series of accidents: `grep -c $'\r'` reported 0 CR bytes for a file holding 1556, and was
proven broken against a control file holding exactly one; `python tool.py | tail -2; echo $?`
reported the exit code of `tail`, not of the tool, in the very block written to prove the tool
refuses; a flip test removed the NEWEST run from a snapshot, which is always outside the trimmed
window, so only the hash moved and no measured figure did; and `grep -c '1[0-9][0-9]%'` returned
6 while looking for values above 100 percent, because `100%` matches it.
**THE AMENDMENT: run the check against a case it must CATCH and a case it must MISS before
believing its result.** One control input costs a line and closes all four. In a pipeline, the
exit code of the command under test is read directly or with `PIPESTATUS`, never through `$?`.
**CHECKABLE: no** - the failure is in a command typed into a chat, not in a stored byte.

## AMENDMENT to R-S87-6 (scheduler lateness) - FOURTH AMENDMENT (S99)

The band is now MEASURED BY A TOOL IN THE REPO rather than recalled: `tools/gni_runtime.py`
derives it from the workflows whose delivery was complete, and at 2026-09-04 over a 16-day
window it is **744 minutes (12.4 hours)** - above every band this rule has carried (S87 medians
243/177/61 min; S89 4h39-6h05; S91 6h03-7h24). Two further constraints travel with it. The band
can only be derived from crons whose slots are far enough apart to be paired, so it has never
been measured on the 30-minute crons and cannot be. And the band is a property of a WINDOW: quote
it with the window and the snapshot that produced it, or re-derive it.
**CHECKABLE: yes** - assert any lateness figure in `docs/` sits beside the window it came from.

## AMENDMENT to R-S84-4 (distinguish the MAD debate from the grounding-watch)

The rule says to distinguish them by the presence of `ARB-FIT`, which requires downloading a run
log. `gh run view <id> --json jobs` separates them without reading a log at all: the debate shows
`run-mad success` with `grounding-watch skipped`, the watch shows the reverse. Measured on three
runs at S99. Prefer the job-level read; keep `ARB-FIT` as the fallback when job data is absent.
Trap that travels with it: a `skipped` job reports `completedAt` BEFORE `startedAt`, so any
duration arithmetic must exclude skipped jobs or it computes a negative.
**CHECKABLE: yes** - assert no document instructs distinguishing the two by TIME alone.
