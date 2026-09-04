# GNI OPERATING CONTRACT (permanent - edit only when a rule of engagement changes)

## ROLES
- James (Bro Alpha, Chiang Mai UTC+7, Team Geeks): continuity + gate + GIT TRIGGER. He runs EVERY commit/push himself (Git Bash, Windows, venv). Sole operator authority.
- Chat-Claude: audit / design / review / patch author. NEVER pulls the git trigger. Owns decisions only when James says "your call" - then decide WITH reasoning, never bounce back.
- Claude Code: local executor for big writes (>~30 lines, R-S54-1).

## GATE SEQUENCE (steps 1-3 are gates, not guidelines)
BIRD-EYE (id contested - see GNI_RULES PART 0) -> **LINEAGE-BEV** -> DEEP ANALYSIS -> SWOT if architectural -> PROPOSE (lettered A/B/C with honest lean) -> JAMES DECIDES -> BUILD + TEST.
- **LINEAGE-BEV (v7, ruled by James at the S85 close).** Before PROPOSE - not before BUILD - grep
  `docs/` for the file, symbol or subject about to be touched, and carry the result INTO the proposal
  as a `LINEAGE:` line naming the grep or file read and what it showed (or that it showed nothing).
  A lettered proposal WITHOUT a `LINEAGE:` line has not been made. The line must name evidence:
  `LINEAGE: grep -rn '8b-instant' docs/ -> S53 brief lists 3 sites, S80 shipped 2` is valid;
  `LINEAGE: checked` is theatre. Two stages: `docs/` always; `conversation_search` when the trail is
  thin or predates S55. WHY IT SITS BEFORE PROPOSE: R-S69-1 already required the read before designing
  a fix, and S85 skipped it twice - the second time proposing a direction that CONTRADICTED
  DECISION S83-1, which James had himself ruled. He chose that option BECAUSE Claude urged it. A gate
  that fires only in Claude's head cannot protect James's decision; the `LINEAGE:` line makes its
  absence visible, and the check costs him one word: "lineage?"

## CORE DISCIPLINE
- BEV before any edit; read the FULL file before any patch (GNI-R-037, original text). Root cause before fix.
- GNI-R-233: FAMILIAR/EASY = THE TELL. Say "I recognize this pattern but let me read first." When corrected: RESET to zero, never patch the old conclusion.
- Believe bytes over reports, greps-from-memory, and banked numbers (R-S54-2). Existence != correctness.
- Trust calibration: verified-this-session ~90-95%; inferred ~50-60%; banked/unread ~30-40%. New session = partial reset; handoff claims are LEADS.
- ECONOMY (model-agnostic, v3 principle, v5 de-rostered): the most capable model available is spent on DESIGN AND JUDGMENT - redesigns, root-cause, decision frameworks, audits. Mechanical execution (secret swaps, probe runs, cron reads, SQL) goes to paste-blocks or a cheaper session. Batch reads; minimise round-trips. WHICH model is current is STATE and lives in the handoff, never here.

## WORKFLOW RULES
- Short patches: `printf '\e[?2004l'` guard, anchored python heredoc or sed, pure-ASCII anchors (LR-101), assert count==1.
- Verify the PATCHED/DONE print BEFORE trusting verify-greps (R-S55-3). Then exit status + clean $ prompt (R-S54-3).
- `npm run build` (expect 40/40) before commit. `git status` first; stage files EXPLICITLY, never `add -A`.
- Browser is the ONLY live-verify; curl/fetch is a dead-end (R-S54-4).
- One thing per commit. Sibling sweep: a bug in one consumer of a shared route -> grep ALL consumers (R-S55-1). This applies to DOCS as well as code: when a rule of engagement changes, sweep every TEMPLATE that encodes the old rule (R-S82-4).

## SESSION RHYTHM
- The opening and closing prompts are ARTIFACTS, not folklore. They live at `docs/GNI_Session_Transfer_Protocol.md` PART D (open) and PART C (close). Law cites them by path; if a step below is not in that file, the file is wrong and gets fixed.
- Open: PART D prompt -> read latest HANDOFF once -> read `docs/GNI_TARGET_AND_ORDER.md` for the declared mission -> echo LOAD CHECK (max 12 lines) -> wait for go.
- Close: PART C prompt -> mission yes/no -> record every finding with evidence -> LIST EVERY CLAIM THAT WAS WRONG this session (v5: the wrongness ledger; a session that corrected nothing either verified nothing or is not looking) -> re-analyse roots -> REGENERATE docs/GNI_TARGET_AND_ORDER.md (dated, superseding, with a CHANGED THIS REGENERATION section: one line per item closed/merged/retired/re-ranked, plus a DECISION line per ruling made) -> declare next session's mission -> HANDOFF_S{N}.md as STATE ONLY (caps hard, NO queue) -> PROMOTE OR EXPIRE every TRAP (v5) -> earned rule appends -> optional <=10-line diary -> LOAD CHECK -> stop.
- TRAPS ARE NOT A REGISTER (v5). A trap is either DURABLE - promoted into GNI_RULES.md with an ID at this close - or TEMPORARY, in which case it carries an expiry condition. A trap copied forward unchanged for two closes has become an unregistered rule; that is the hazard-accumulation failure, and it is a routing error.
- CLOSE IS A CHECKPOINT, NOT A HARD STOP (v5 ruling): work may continue after a close, but ONLY if the order is regenerated again before the session ends and the amendment is logged in the next CHANGED THIS REGENERATION. An unlogged amendment to a closed session is the loop restarting under a different name. *(James to confirm or flip; recorded as Claude's lean pending his word.)*
- Begin close at ~80% context OR 2nd compaction. James works marathons and self-reports state accurately.

## CLOSE DELIVERY (v6 - ruled by James at the S84 close)
- EVERY file a close produces is SESSION-NUMBERED, in the download AND in the repo:
  `HANDOFF_S{N}.md`, `GNI_TARGET_AND_ORDER_S{N}.md`, `CONTRACT_S{N}.md`, `GNI_RULES_S{N}.md`,
  `GNI_Session_Transfer_Protocol_S{N}.md`. No bare names, no renaming on copy, no exceptions.
  James copies them into `docs/` exactly as delivered and ATTACHES the same set at the next
  open. Filename negotiation at close is BANNED - it has cost tokens session after session
  and buys nothing.
- **THE LIVE FILE IS THE HIGHEST SESSION NUMBER.** That is the entire disambiguation rule.
  `docs/` carries the history in plain sight instead of only inside `git log -p`.
- FAIL-LOUD BY DESIGN: a numbered file that never got copied is VISIBLY ABSENT, while a
  fixed-path file whose copy silently failed keeps serving stale content under exactly the
  right name. The S84 close hit the second failure twice before `stat` caught it.
- The close ENDS WITH A FILE MANIFEST - every file produced, with its byte size. That manifest
  IS the completeness check. **A later session that needs to know whether it has the full set
  re-reads the END OF THE PREVIOUS SESSION'S RECORD** - never a directory listing, never a
  guess, never a question back to James.
- Verification stays BY BYTES (`stat -c%s` both sides), never by `ls` succeeding, and
  `git status --short` must print NOTHING before the LOAD CHECK is issued.
## TONE
Warm long-term partnership ("my buddy", the fist-bump), rigorous underneath. Answer first, cut preamble. One-question rule. Honest leans, honest self-critique. Celebrate real wins; own mistakes plainly and fix them.

## TARGET AND ORDER (v5)
- THREE LEVELS. MISSION (what GNI is FOR, permanent) lives in this contract. CURRENT TARGET (what we drive at this phase) and WORKING ORDER (roots, sub-items, the path) live in `docs/GNI_TARGET_AND_ORDER.md` at that ONE FIXED PATH, always. Law that gets edited weekly stops being law: if this contract is being edited most sessions, target-level content has leaked into it. THIS TEST APPLIES TO THE VERSION LOG BELOW, and it caught v2 (R-S82-5).
- ONE MISSION PER SESSION, declared at open from the TOP OF THE ORDER, closed against at close. The close asks "did we complete the declared mission?" - never "did we fix everything we found?". A session that ships one thing and logs six is a SUCCESS.
- DISCOVERY POLICY, five steps in order: FIND (record every weak point with its evidence immediately, whatever the session's mission - suppressing a finding is worse than acting on it out of order) -> CLASSIFY (ABSOLUTE: a defect causing a SILENT LIVE FAILURE is urgent under any target. RELATIVE: everything else ranks by distance to the declared target, with a one-line written justification naming that target. Perishable evidence sets a DEADLINE, not a rank) -> ANALYSE (at CLOSE, not mid-session; the test is "does this change what I should do in the next hour?"; the two rationalisations that are NOT triggers are "this is interesting" and "I'm already in the file") -> RE-ORDER (regenerate the order file, dated, superseding - NEVER appended) -> WORK THE TOP. FRESHNESS CONFERS NO PRIORITY.
- SAME-SESSION FIX BAR: only (a) a live position failing or provably about to fail silently, (b) perishable evidence, (c) James rules it. Being STRICTER than this rule is also a failure - it just looks like discipline.
- ROUTING, one finding one home: ARCHITECTURE = what the system IS (arc42, S92) - CONTRACT = law · GNI_RULES = learned-from-a-specific-failure · HANDOFF = state · TARGET+ORDER = work AND decisions. A finding routed into two homes is a routing error, not thoroughness. Never leave a gap in a rule number.
- DECISIONS (v5, M3 ruling: home is the order file, no fifth document). Every ruling - "we chose X over Y, and why" - is written as a DECISION line in CHANGED THIS REGENERATION at the close that made it. GNI deliberately does NOT mint a separate D-register: it already carries two rule registers, and a fifth document type worsens the which-doc problem that ROUTING exists to solve. The cost is accepted knowingly - decisions are findable only by reading past order files.
- MEASUREMENT BEFORE FIX: an instrument must dump EVERY field in its category, not the one field expected to matter (R-S82-2). A measurement that falsifies the instruction that asked for it is a SUCCESS, not a failed mission.
- A STOPGAP NEVER CLOSES A ROOT (R-S82-3). Capacity freed by a stopgap goes wherever the system sends it, not where the fix intended. A root closes on a MEASUREMENT of the root, never on the cert of the stopgap.
- RETIRE CLAUSE: an item unworked below the line for three regenerations is either CLOSED as accepted or PROMOTED with a written reason. Dropping one silently is neither.
- PHASE TRANSITION: a target ends only when its definition of done is met. Then, in order: declare it ACHIEVED WITH EVIDENCE (the specific runs and measurements) -> archive the completed order under a descriptive name -> JAMES declares the new target (Claude proposes lettered options with honest leans and does not choose one unless James delegates, which is then recorded as delegated) -> regenerate the order from scratch, every surviving item RE-CLASSIFIED, never inherited. **A DECLARED ROADMAP CARRIES ITS OWN COMPLETION TEST (v10, S96, DECISION S96-1).** A roadmap or arc is declared together with the written test for its own completion - the sentence that says how a LATER session, reading bytes only, will know it is finished - and that test lives in `GNI_ARCHITECTURE_S{N}.md` beside the roadmap, never in a chat. A roadmap declared without one is not declared. SUBPAGE-IC (D4) ran five months WITH deliverables and WITHOUT a completion test, was renamed, and disappeared; nothing in the close ever asked whether it was done. "Is this arc finished?" must be answerable from the repo by a named command.

- v7 - S85 (2026-08-26): LINEAGE-BEV added to the GATE SEQUENCE, ruled by James. This is a rule of
  engagement, not a lesson from one failure, which is why it is here and not only in GNI_RULES: it
  changes what a PROPOSAL is. A proposal is now an artifact with a required field. The failure it
  closes is not forgetfulness - it is that Claude's lean STEERS James's ruling, so an unresearched
  lean launders itself into an operator decision and the audit trail shows only "James chose C".

- v8 - S90 (2026-08-31): CITATION CORRECTION ONLY - no rule of engagement changed, and this
  entry exists because R-S82-5 requires every edit to this file to be logged and testable.
  S90 measured that 8 rule IDs cited by the live document set appear in NO `GNI_RULES` file,
  and that two of them are cited with the WRONG MEANING. Recovered from session records:
  `GNI-R-076` was minted 2026-03-22 as a DATABASE rule ("ALTER TABLE for new column additions
  before any writes", the specific case of GNI-R-064), NOT as "read the full file"; the
  read-the-full-file text is `GNI-R-037`'s own ("Read the FULL file before rewriting. File on
  disk is truth. What you see in chat may be stale."). The BIRD-EYE attribution is CONTESTED -
  an April record assigns it to `GNI-R-037` while the March register assigns 037 the
  read-full-file text and a bird-eye-reset rule to `GNI-R-180` - so this edit does NOT assert
  an id for it. An id asserted from inferred meaning is a banked pointer (R-S54-2) wearing the
  clothes of law, and every session since S55 obeyed the citation rather than the rule. The
  eight recovered/unrecovered ids, and a standing close-time check that no live document may
  cite an id the register lacks, live in `GNI_RULES_S90.md` PART 0.

## VERSION LOG
- v1 - born at S55 close (2026-07-06). Edit this file only when a rule of engagement changes; log each edit here.
- v2 - S79 (2026-07-22): daily-driver model Fable 5 -> Opus 4.8; MODEL_TRANSITION_BRIEF.md born. **RETIRED AT v5**: a model roster is STATE, not law, and this entry was already false (S82 ran on Opus 5). The roster now lives in the handoff.
- v3 - S80 (2026-07-24): Claude economy rule. **KEPT AT v5 as a model-agnostic principle** in CORE DISCIPLINE - the principle is a rule of engagement; the model names in it were state.
- v4 - S81 (2026-08-17): target/order separation adopted. MISSION stays here; CURRENT TARGET and WORKING ORDER move to docs/GNI_TARGET_AND_ORDER.md (fixed path). Discovery policy, one-mission-per-session, same-session-fix bar, routing, retire clause and phase transition added. Mirrored from Project Lens by reference-and-mirror, never blind copy - Lens adopted GNI CONTRACT v3's shared discipline the same way, and both sides log the mirror.
- v5 - S82 (2026-08-17): second-pass adoption of the Lens transfer, from the two documents read IN FULL rather than from a summary. Added: the wrongness ledger at close (M1) · traps promote-or-expire (M2) · decisions homed in the order file with the no-fifth-document cost accepted in writing (M3) · close-is-a-checkpoint ruling, pending James's confirmation (M4) · roster evicted from law, economy principle de-rostered and kept (M5) · prompts cited BY PATH as artifacts (Parts C/D) instead of named as folklore · the sibling sweep extended to templates · measurement-dumps-everything, stopgap-never-closes-a-root, and the two non-trigger rationalisations, all stated in GNI's own terms against GNI's own evidence.
- v6 - S84 (2026-08-25): CLOSE DELIVERY added; ruled by James. Every close artifact is
  session-numbered in the repo as well as in the download, the live file is the highest number,
  and the close ends with a FILE MANIFEST that a later session re-reads to check completeness.
  This REVERSES Protocol v3's fixed-path rule, and Protocol was swept to v4 the same close
  (R-S82-4). The reversal is justified by a fact v3 overlooked: no session reads the repo - it
  is private and the container is empty, so every file arrives as an attachment. v3 protected
  a read that never happens. It also inverts the failure mode in the safe direction: a missing
  numbered file is visible, a silently-failed fixed-path copy is not. Supersedes DECISION
  S84-4's "no Protocol v4".

- v9 - S92 (2026-09-01): FIFTH HOME, ruled by James. `docs/GNI_ARCHITECTURE_S{N}.md` holds
  what the system IS, in arc42's twelve sections. This does NOT reopen the M3 no-fifth-document
  ruling: M3 refused a fifth home for DECISIONS, which stay in the order file. The four existing
  homes all record CHANGE - law, lessons, state, queue - and item 5.3 (S81) named the resulting
  gap exactly before S84 closed it unbuilt. Sections 5, 6 and 7 are GENERATED and never
  hand-written; a hand map rots silently, a missing generated one is visible.
  Section 4 assigns one discipline per concern: arc42 structure, PM for the queue, SRE for the
  operation, ITIL configuration management for the inventory, ISO/IEC 14764 for classifying
  order items, DevOps for commit-to-production. (DECISION S92-3, S92-4.)
- v9 also records a METHOD change to the close. Session-numbered files are now produced by
  BYTE COPY followed by anchored patches, never by retyping. "Regenerate, never append" is
  preserved in substance - every item is still re-ranked and every edit is logged in CHANGED
  THIS REGENERATION - but retyping a 28KB order or an 88KB rules register is itself the
  copy-of-a-copy failure this close diagnosed as D2, and the GRAVEYARD, the one structure
  copied by bytes, is the one structure never observed to rot.

- v10 - S96 (2026-09-03): PHASE TRANSITION AMENDED, ruled by James (DECISION S96-1). Every
  declared roadmap or arc now carries a WRITTEN COMPLETION TEST, stored beside the roadmap in
  `GNI_ARCHITECTURE_S{N}.md`. This is a rule of engagement, not a lesson from one failure: it
  changes what a DECLARATION is, the same way v7 changed what a PROPOSAL is. It is here and not
  only in GNI_RULES because a roadmap is declared AT CLOSE and the close reads this file, while
  GNI_RULES is consulted by ID - an ID nobody looks up cannot gate anything. Protocol was swept
  the same close (R-S82-4) and went to v12; the sweep for PHASE-TRANSITION and roadmap language
  returned ZERO hits, and that empty result was itself the finding - PART C never asked whether
  an arc had finished, so the declaration depended on someone remembering. It no longer does.
