# GNI SESSION TRANSFER PROTOCOL v11
**Purpose:** lossless session-to-session transfer at ~25-35% of the old token cost.
**Principle:** every fact lives in ONE file (SSOT); the handoff carries STATE only; the ORDER carries work; caps force density.
**This file is a TEMPLATE, and a template is law that executes itself next session.** v1 said it was "written once and never regenerated" and then sat unread for 27 sessions while the contract changed underneath it. It is regenerated whenever a rule of engagement changes (R-S82-4).
**v3's core change: THIS FILE IS NOW READ FROM THE REPO AT EVERY OPEN.** Before v3 the closing prompt reached a session only by James pasting it from outside — a prompt living in two places is a dual source of truth, and the pasted copy is free to drift from the repo copy with nothing able to detect it. Mirrored from Project Lens, which shipped the identical fix after its own pasted close prompt was found to have silently lost two clauses.

---

## PART A — THE FILE ARCHITECTURE (what lives where)

| File | Role | Written | Cap |
|------|------|---------|-----|
| `docs/CONTRACT.md` | LAW — roles, gates, workflow, tone, discovery policy | Only when a rule of engagement changes; log every edit | no line cap, but see the law-vs-state test below |
| `docs/GNI_RULES.md` | LEARNED — all rules by ID (GNI-R-###, R-S##-#) | Append-only; 1-3 lines per rule; never leave a number gap | n/a |
| `docs/GNI_TARGET_AND_ORDER.md` | WORK + DECISIONS — current target, definition of done, ranked order | REGENERATED every close, dated, superseding. NEVER appended | n/a |
| `docs/GNI_Session_Transfer_Protocol.md` | THE PROMPTS — Part C (close) and Part D (open) as artifacts | Regenerated when a rule of engagement changes | n/a |
| `docs/HANDOFF_S{N}.md` | STATE — what is true right now. NO QUEUE | Every close, from the Part B template | 120 lines |
| `docs/DIARY.md` | Feelings/reflection (optional) | Append <=10 lines, only if the session earned it | 10/entry |
| `docs/AUDIT_S{N}.md` | Deep archive | ONLY milestone sessions | n/a |

**EVERY CLOSE ARTIFACT IS SESSION-NUMBERED (v4) - this REVERSES v3's fixed-path rule.**
- `HANDOFF_S{N}.md`, `GNI_TARGET_AND_ORDER_S{N}.md`, `CONTRACT_S{N}.md`, `GNI_RULES_S{N}.md`,
  `GNI_Session_Transfer_Protocol_S{N}.md` - all of them, download and repo alike, copied under
  the name they were delivered with. No renaming step exists any more.
- **THE LIVE FILE IS THE HIGHEST SESSION NUMBER.** That is the whole disambiguation rule.
- WHY v3 WAS WRONG HERE: it forbade numbering because "the opening prompt names these paths
  literally, so a numbered copy leaves the STALE file where the next session will read it."
  But NO SESSION READS THE REPO. It is private, the container is empty, and every file reaches
  a session because James ATTACHES it. v3 protected a read that never happens, and charged a
  filename negotiation at every close for the privilege.
- The failure v3 feared INVERTS under numbering: a numbered file that was never copied is
  VISIBLY ABSENT, while a fixed-path file whose copy silently failed keeps serving stale
  content under exactly the right name - which happened twice at the S84 close.
- COMPLETENESS IS CHECKED BY RE-READING THE END OF THE PREVIOUS SESSION'S RECORD, where the
  close printed its FILE MANIFEST. Not by a directory listing. Not by asking.
**LAW-VS-STATE TEST:** if CONTRACT.md is edited most sessions, target-level or state-level content has leaked into it. Run this against its VERSION LOG, not only its sections — that is where the leak hid until S82 (R-S82-5).

**Retired as separate files:** Next_Session_Brief (-> HANDOFF), collaboration file (-> HANDOFF + CONTRACT), FILE_UPDATES bundles (-> each file updated directly, once). `STATUS.md` was retired at v1 but still sits in `docs/` frozen at S46 (2026-06-21) — a fossil, not a source. Delete or archive it; never read it as state.

**Nothing is lost:** history = git-tracked handoffs and superseded order files. Rules = permanent append-only ledger. Decisions = the DECISION lines in each close's CHANGED THIS REGENERATION section. Deep detail = repo bytes (BEV is ground truth; a handoff claim is a LEAD until re-verified).

---

## PART B — HANDOFF TEMPLATE (copy for each close; CAPS ARE HARD)

```markdown
# HANDOFF S{N} -> S{N+1}
DATE: {date} | HEAD: `{hash}` (verify ls-remote) | MODEL: {model at close}
Read ONCE. Standing rules: docs/GNI_RULES.md by ID (current through {last ID}). CONTRACT v{n}.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER.md`. This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: {one line}  L2 MAD: {N debate + M watch, by ARB-FIT}  L3 GPVS: {one line}
L4 Quota: {one line}     L5 Public: {one line}
Live watch: {anything hot right now}
Target declared: {current target}

## 2. DELTA (<=15 lines) - what THIS session shipped/learned
| Item | What | Proof |
|------|------|-------|
| `hash` | ... | build 40/40 + browser / grep / log |

## 3. ORDER
**MOVED.** See `docs/GNI_TARGET_AND_ORDER.md` — dated, ranked, regenerated at every close.
Do not re-derive a queue from this file. Do not fold items forward without re-ranking.
NEXT SESSION'S MISSION is declared at the top of that file.

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|

## 5. WRONG THIS SESSION (<=6 lines) - claims that turned out false
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
(A session with an empty table either verified nothing or is not looking. Say which.)

## 6. TRAPS (<=8 lines) - TEMPORARY ONLY, each with an expiry
- {trap} — expires when {condition}
(Durable traps are NOT listed here; they were promoted to GNI_RULES.md at this close.
 A trap copied forward unchanged twice has become an unregistered rule — routing error.)

## 7. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `{hash}` {tree state} -- {one-line situation}
TARGET = {current target}; MISSION = {next session's declared mission}
ORDER = `docs/GNI_TARGET_AND_ORDER.md` is the queue -- regenerate at close, never fold forward
TRAP = {the one most dangerous trap}
FIRST MOVE = {the literal first action}

## 8. POINTERS (<=5 lines)
Deep detail if needed: {file:line / audit doc / past-handoff}
```

---

## PART C — STANDARD CLOSING PROMPT (v3: INVOKED BY NAME, READ FROM THE REPO)

**PART D IS INSTANTIATED FROM THESE BYTES, NEVER FROM A CHAT (v6, R-S86-4).** James copies the block below out of the HIGHEST-NUMBERED protocol file and substitutes the session numbers for `{N+1}` and `{N}` -- nothing else. He does not copy it from a chat transcript, and an amendment proposed in chat is not carried forward until it lands in THIS FILE. S86 found the heading still reading `v3` and step 0 still saying "The handoff is ATTACHED" while James's own paste had said "The S84 close set is ATTACHED" since S85 -- his paste was AHEAD of the repo, which no single side can detect. The prompt is a TEMPLATE: if it needs editing most sessions, state has leaked into it (LAW-VS-STATE TEST).

**From v3, James does not paste this text.** He says **"CLOSE S{N}, my buddy"** and the session reads these steps from `docs/GNI_Session_Transfer_Protocol.md`, which Part D already had it open. A pasted prompt drifts from the repo copy and nothing can detect the drift; that is the dual-source-of-truth failure this whole protocol exists to prevent.

**This prompt is the highest-leverage object in the protocol.** A close that folds items forward without regenerating an order grows the list BY CONSTRUCTION — that is the loop.

```
CLOSE S{N}, my buddy.

0. READ THIS FILE'S PART C FROM THE REPO before doing anything else. If what you are
   about to run differs from these bytes, the bytes win, and the difference is a FINDING.

1. MISSION: did we complete the DECLARED mission? Yes or no, in one line. Not "did we fix
   everything we found" — a session that ships one thing and logs six is a SUCCESS.

2. FINDINGS: list every weak point found this session with its evidence, whatever the
   mission was. Suppressing a finding is worse than acting on it out of order.
   For every LETTERED PROPOSAL made this session, state whether it carried a `LINEAGE:`
   line (CONTRACT v7). A proposal made without one is a WRONG-ledger entry even if the
   option chosen turned out fine.

3. WRONG: list every claim that turned out false this session, and what caught it.
   Include claims made by CLAUDE about its own instruments and its own commands, not only
   claims about the system.

4. ROOTS: re-analyse. Is each finding an existing root or a NEW root? A new root may
   re-rank everything above it.

5. REGENERATE docs/GNI_TARGET_AND_ORDER.md — dated, superseding, NEVER appended, and
   delivered as `GNI_TARGET_AND_ORDER_S{N}.md` -- SESSION-NUMBERED like every other close
   artifact (CONTRACT v6). The LIVE order is the HIGHEST session number. Include CHANGED THIS
   REGENERATION: one line per item closed / merged / retired / re-ranked, plus a DECISION
   line for every ruling made this session (what we chose, over what, why).
   Apply the retire clause: below the line for three regenerations = closed as accepted or
   promoted with a written reason. Dropping one silently is neither.
   CARRY THE GRAVEYARD FORWARD (v8, DECISION S88-2). The order's GRAVEYARD section - the
   directions RULED OUT with the measurement that killed them - is COPIED INTO EVERY
   REGENERATION verbatim, never rewritten from memory and never dropped. It is the one
   exception to 'regenerate, never append', and it exists because a design falsified at
   S87 was first proposed in June and survived five sessions inside prose that nobody
   re-read. A regeneration that loses it re-opens the graveyard by construction.
   ASSERT ITEM NUMBERS ARE UNIQUE before delivering — a presence-only check has shipped a
   duplicate before. State the expected count IN ADVANCE, then grep.

6. DECLARE next session's mission, from the TOP of the regenerated order.

7. Build docs/HANDOFF_S{N}.md from Protocol Part B. Caps are HARD. STATE ONLY, no queue.
   This file is session-numbered like EVERY close artifact (CONTRACT v6), not uniquely so.

8. TRAPS: promote each durable trap into docs/GNI_RULES.md with an ID, or give it an expiry
   condition and keep it. No trap rides forward unchanged twice.

9. RULES: append only what S{N} EARNED (1-3 lines each, with ID, no number gaps).
   BEFORE claiming a gap or a count, check BOTH ID schemes — GNI_RULES.md carries
   `GNI-R-###` and `R-S##-#`, and a grep for one scheme is blind to the other. A count that
   sees only half the register has invented a hole. And before minting a NEW number, search
   the register for an existing rule that already says it — amend that one instead. Lens
   paid for re-minting a rule it already had.

10. CONTRACT.md: edit ONLY if a rule of engagement changed. Log it in the version log.
    One earned rule does not justify a version bump; RULES is its home.

11. PROTOCOL: if a rule of engagement changed, sweep THIS FILE too (R-S82-4) and regenerate
    it. A template that still encodes the old rule will restore it by itself.

12. Diary: <=10 lines, only if the session earned it.

13. DELIVERY (v4): long documents go out as DOWNLOADS, never heredocs - they contain literal
    backticks. EVERY file carries the session number, in the download and in the repo alike
    (`GNI_TARGET_AND_ORDER_S{N}.md`, `CONTRACT_S{N}.md`, ...). Do NOT rename on copy, do NOT
    negotiate filenames, do NOT emit `cp` with an unverified source path. James copies them
    into `docs/` as delivered; Claude then verifies BY BYTES (`stat -c%s` both sides), never
    by `ls` succeeding, and requires an EMPTY `git status --short`.
14. FILE MANIFEST, then the LOAD CHECK block, then STOP - no summary essay after either. The
    manifest lists EVERY file this close produced with its byte size, because it is what a
    later session re-reads to confirm it has the full set.
```

---

## PART D — STANDARD OPENING PROMPT (paste at session start; v7)

```
OPEN S{N+1}, my buddy — warm as always, lean on tokens.

0. The S{N} close set is ATTACHED (container is empty; repo is private — never try to clone).

1. FIRST BLOCK, before any reading: establish WHEN and WHERE you are.
   `date -u` AND `date` · `git status --short` · `git rev-parse HEAD` ·
   `git ls-remote origin -h refs/heads/main`.
   Never state a clock position, an elapsed time, or "the next run is due about now" from
   turn count or from memory. Read the clock in the same block as the claim.

2. The whole S{N} close set is ATTACHED - handoff, order, rules, contract, protocol, every one
   session-numbered. Read this protocol first (Part C is the close; it is invoked BY NAME and
   never pasted), then the handoff ONCE, carefully, then the order file, which holds the
   declared mission and the ranked order. **THE LIVE FILE IS THE HIGHEST SESSION NUMBER.** If
   the set looks incomplete, re-read the END of the previous session's record, where the close
   printed its file manifest - do not ask James to hunt for it.
3. The handoff's HEAD line is STALE BY CONSTRUCTION — it was written before its own close
   commit existed. `ls-remote` is the truth; a mismatch is expected, not a loss.

4. COUNT WHAT RAN WHILE NOBODY WAS WATCHING. List MAD runs since the handoff's date and say
   how many carry unread evidence. A gap is a GIFT: it converts a two-sample ruling into a
   distribution, and it has already done so once.
   `gni_mad.yml` carries BOTH the debate and the grounding-watch — distinguish them by
   the presence of `ARB-FIT`, never by time alone.
   Judge NOVELTY BY RUN ID against the ids already read. A content grep proves the log has
   content, not that the run is new; `-L 1` will hand back a run you have already read and
   every content check will pass.

5. Echo ONLY the LOAD CHECK block. Max 12 lines total.

6. Do NOT re-explain history, re-audit closed items, or re-derive a queue — the order file
   IS the queue. Handoff claims are LEADS; BEV before acting on any of them.

7. WORK THE TOP OF THE ORDER. Not the newest finding, not the most interesting one.
   FRESHNESS CONFERS NO PRIORITY. If you believe the order is wrong, say so and propose a
   re-order — do not silently work something else.

8. ANALYTICAL STANCE -- evidence first, authority never. No persona is granted
   here on purpose: a role title makes assertion feel earned, and confident
   recall is exactly what hallucination looks like from the inside.

   a. NEVER assert a fact about the world -- events, dates, who did what --
      from training memory. State the knowledge cutoff, then reason ONLY from
      what the repo, the DB, or James supplies. If a date or event is
      load-bearing, question it before building on it.

   b. BEFORE designing any change to a DETERMINISTIC component (keyword
      scorers, gates, filters, math), SIMULATE it over stored history first.
      IMPORT the real function; never re-implement it. A design that cannot be
      simulated has not been evaluated. Report the distribution, not one number.

   c. WRITE PREDICTIONS BEFORE READING RESULTS. Numbered, falsifiable. Then say
      plainly which ones failed.

   d. LABEL EVERY FINDING: [NEW] measured this session - [RE-CONFIRMED] already
      in the records, restated - [PROPOSED] my idea, not yet measured. An
      unlabeled finding reads as discovery and steals credit from the record.

   e. A BLOCKER IS A CLAIM, NOT A FACT. Before accepting "X is impossible until
      Y", spend one measurement testing it. Blockers copied forward unchecked
      are how a five-minute measurement stays undone for months.

   f. WHOLE SYSTEM, NOT ONE STEP. Before proposing a fix, list every consumer of
      the thing being changed and what each one actually needs. A fix that
      serves one consumer and breaks another is not a fix.

   g. RUN THE SWOT TWICE, from opposite premises -- "the instrument is broken"
      and "the instrument is right and the world is bad". Report both. Where
      they converge is the finding; where they diverge is the open question.

   h. ASK WHAT IS MISSING FROM THE DATA. Absent evidence -- never-firing
      keywords, never-taken branches, a regime with no counterexample -- is
      evidence.

9. Then wait for my go.
```

---

## PART E — WHY THIS IS LOSSLESS (the guarantees)

1. **Rules can't be lost** — permanent append-only file, referenced by ID forever.
2. **History can't be lost** — every handoff and every superseded order file is git-tracked.
3. **Decisions can't be lost** — every ruling is a DECISION line in the order file that made it.
4. **Nuance can't silently rot** — trust tags force each claim to declare its reliability, and
   the opening prompt mandates BEV-before-acting.
5. **The list can't grow forever** — the close REGENERATES rather than folds, and the retire
   clause forces every below-the-line item to be closed or promoted, never dropped in silence.
6. **Comprehension is verified, not assumed** — the LOAD CHECK echo proves the next AI loaded
   the right state in 5 lines.
7. **Being wrong is recorded** — the WRONG section makes correction a normal artifact of a
   session instead of something quietly overwritten.
8. **The prompts can't drift (v3)** — they live in ONE place and are read from the repo, so a
   remembered or pasted variant can be compared against the bytes and the difference caught.

## PART F — EXPECTED SAVINGS
Old: close ~8-12K output + open ~30-40K input + ~2-3K re-explanation.
New: close ~3-4K output (handoff + regenerated order) + open ~4-5K input + ~0.3K echo.
Transfer overhead drops roughly 60-70%. The regeneration costs slightly more than v1's fold —
and buys the only thing that stops the list growing by construction.

- v8 - S88 (2026-08-30). PART C step 5 gains CARRY THE GRAVEYARD FORWARD. Swept under
  R-S82-4: DECISION S88-2 added a section to the ORDER that must survive regeneration,
  and step 5's own words ('NEVER appended', 'regenerated from scratch') would have
  deleted it at the next close. A template that still encodes the old rule restores it
  by itself. No CONTRACT bump: this changes what a close PRODUCES, not a rule of
  engagement, and CONTRACT stays v7 in CONTENT. **The parenthetical that stood here --
  `CONTRACT_S85.md` carries forward -- is RETRACTED AT v9; see the v9 entry.**
- v9 - S89 (2026-08-31). NO template step changed. The VERSION LOG itself was swept under
  R-S82-4, because v8's own closing parenthetical encoded a file-naming rule that CONTRACT
  CLOSE DELIVERY v6 does not contain. v6 enumerates all five artifacts with `S{N}` --
  `HANDOFF`, `GNI_TARGET_AND_ORDER`, `CONTRACT`, `GNI_RULES`,
  `GNI_Session_Transfer_Protocol` -- and ends the clause with NO EXCEPTIONS. PART C step 13
  already says the same. The 'carries forward' habit was a DEVIATION at S88 that S89 cited
  back as precedent, which is exactly the self-restoring template R-S82-4 warns about.
  RULED BY JAMES at the S89 close: EVERY close ships all five files session-numbered, even
  when a file's content is byte-identical to the previous one. Only the VERSION LOG entry
  changes when a rule of engagement actually changes. Verify sameness by md5, not by name.
- v7 - S87 (2026-08-29). ANALYTICAL STANCE added as PART D step 8; the old step 8
  ("wait for my go") becomes step 9. Born from a session in which SIX of Claude's
  own claims were killed by measurement and none by argument. The eight clauses are
  not style advice: (a) closes the confident-recall hole a persona would widen --
  the session's own trigger question rested on a date that does not exist in 2026;
  (b) is the session's largest single win, a read-only replay of a deterministic
  scorer over 191 stored runs that falsified a five-month-old design in one command;
  (c) and (d) close the discovery-theatre hole James named directly -- restating a
  filed fact in the voice of a finding hides that no work was done; (e) is the
  S74-to-S86 blocker ("unprovable by SQL until score_breakdown is stored") that was
  copied forward three times unchecked and was false; (f), (g) and (h) are James's
  own moves this session, written back as law. NOT A CONTRACT CHANGE: this is how
  a session reasons, not a rule of engagement, and PART D is where the reasoning
  posture already lives.
- v6 - S86 (2026-08-28). SWEEP REPAIR + THE INSTANTIATION RULE. Part D's heading still said `v3` two versions after the file left it, and step 0 still said "The handoff is ATTACHED" although the S84 close had agreed on "the close set" and James had been pasting that corrected wording ever since. Both are fixed here, and the class of failure is recorded as R-S86-4: the paste had drifted AHEAD of the file, so neither copy alone was evidence of anything. Part D also loses the literal "11:13" from step 4 -- the MAD schedule moved ~9.5 hours on Aug 27 with no change of ours, and a clock written into a template is state pretending to be law. The `ARB-FIT` test that step 4 already mandates is unaffected by any schedule. DECISION S86-4 (delegated) rejected the alternative of shrinking the pasted prompt to four delegating lines, with a trigger recorded in the S86 order: a second independent paste-vs-file divergence reopens it.
- v5 - S85 (2026-08-26). TWO FIXES. (a) SWEEP MISS REPAIRED: v4 moved every close artifact to
  session-numbered names in Part A and step 13, but Part C step 5 still ordered the order file
  "written to the FIXED PATH with NO session number" and step 7 still called the handoff "the one
  filename that carries a number". Both were v3 rules that v4 itself reversed; two closes run from
  this template would have silently restored the fixed path. Found at the S85 OPEN by reading the
  template that was about to be executed - which is what R-S82-4 is for. (b) Part C step 2 now asks
  whether each lettered proposal carried its `LINEAGE:` line (CONTRACT v7), so the new gate has a
  reporting step and cannot decay into an unread rule the way R-S69-1 did.

## VERSION LOG
- v11 - S93 (2026-09-01): ONE TEMPLATE STEP CHANGED. Part B's STATE line said `L2 MAD: {one
  line}`, and every close filled it with a bare count. Part D step 4 already REQUIRES the
  debate/grounding-watch split by `ARB-FIT` presence - so the law was correct and the
  template erased it. S92's handoff said "2 unread MAD runs"; the pair was one debate plus
  one 11:13 watch, and S93 mis-read the same field a second time before checking. The field
  is now `{N debate + M watch, by ARB-FIT}`: a judgment converted into a format
  (ARCHITECTURE 8.3). Recorded as the AMENDMENT to R-S82-4 - a sibling sweep must reach the
  JUDGMENT A TEMPLATE ENCODES, not only the names and paths it mentions.
- v10 - S90 (2026-08-31): VERSION LOG SWEPT ONLY; no step changed. Recorded because CLOSE
  DELIVERY v6 ships all five files session-numbered with NO EXCEPTIONS, and because S90 checked
  whether CONTRACT v8's citation correction obliged a sweep here (R-S82-4): `grep -n
  'GNI-R-037|GNI-R-076|BIRD-EYE'` over this file returns NOTHING, so the template does not
  encode the drifted citations and cannot restore them. The check is the entry.
- v1 — S55 (2026-07-06). Born with the Transfer Protocol; queue lived in the handoff.
- v2 — S82 (2026-08-17). Rebuilt against CONTRACT v4/v5 after a full read showed the prompts
  had never been updated: Part B's `QUEUE (<=25)` removed and replaced by an ORDER pointer,
  plus new WRONG and expiring-TRAPS sections; Part C rewritten from 4 steps to 12; Part D now
  reads the order file and states work-the-top / freshness-confers-no-priority; Part A gains
  the order file, fixes the `GNI_RULES.md` path to `docs/`, and marks `STATUS.md` a fossil.
- v3 — S83 (2026-08-24). **The close stops being pasted.** Part D step 2 now reads THIS FILE,
  and Part C is invoked by name, closing the dual-source-of-truth hole that let Lens's pasted
  close prompt silently lose two clauses. Part A gains the FIXED PATH vs SESSION-NUMBERED
  rule (Lens shipped a numbered order to its fixed path and would have opened on the stale
  one). Part D gains a clock-and-HEAD first block (S83 twice stated a schedule position from
  turn count, and mistook a six-day gap for minutes), an unread-run count with the
  debate-vs-grounding-watch distinction, and NOVELTY BY RUN ID (S83's content-grep guard
  passed on a run already read). Part C gains: wrongness covers Claude's own instruments;
  the order goes to the FIXED path; item numbers asserted unique with counts stated in
  advance; the register's TWO ID schemes must both be checked before claiming a gap, and an
  existing rule amended rather than re-minted; one rule does not justify a CONTRACT version;
  a protocol sweep step; and delivery-by-download with byte verification.
- v4 - S84 (2026-08-25). **Every close artifact is session-numbered; v3's fixed-path rule is
  REVERSED.** Ruled by James after filename negotiation at close proved to be a recurring token
  sink. Part A's FIXED PATH section replaced; Part C step 13 rewritten and step 14 gains a FILE
  MANIFEST; Part D step 2 now says the close set is ATTACHED and the live file is the highest
  number. The reversal rests on a fact v3 missed: no session reads the repo, so the literal
  paths v3 protected are never read by anyone. Born from S84's own close, which reached its
  LOAD CHECK with `docs/` holding a stray `GNI_TARGET_AND_ORDER_S83.md`, a byte-identical
  duplicate Protocol, and a CLOSED handoff overwritten in the working tree by a pre-cap draft
  (restored from git).
