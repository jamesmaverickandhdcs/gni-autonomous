# GNI SESSION TRANSFER PROTOCOL v2
**Purpose:** lossless session-to-session transfer at ~25-35% of the old token cost.
**Principle:** every fact lives in ONE file (SSOT); the handoff carries STATE only; the ORDER carries work; caps force density.
**This file is a TEMPLATE, and a template is law that executes itself next session.** v1 said it was "written once and never regenerated" and then sat unread for 27 sessions while the contract changed underneath it. It is regenerated whenever a rule of engagement changes (R-S82-4).

---

## PART A — THE FILE ARCHITECTURE (what lives where)

| File | Role | Written | Cap |
|------|------|---------|-----|
| `docs/CONTRACT.md` | LAW — roles, gates, workflow, tone, discovery policy | Only when a rule of engagement changes; log every edit | no line cap, but see the law-vs-state test below |
| `docs/GNI_RULES.md` | LEARNED — all rules by ID (GNI-R-###, R-S##-#) | Append-only; 1-3 lines per rule; never leave a number gap | n/a |
| `docs/GNI_TARGET_AND_ORDER.md` | WORK + DECISIONS — current target, definition of done, ranked order | REGENERATED every close, dated, superseding. NEVER appended | n/a |
| `docs/HANDOFF_S{N}.md` | STATE — what is true right now. NO QUEUE | Every close, from the Part B template | 120 lines |
| `docs/DIARY.md` | Feelings/reflection (optional) | Append <=10 lines, only if the session earned it | 10/entry |
| `docs/AUDIT_S{N}.md` | Deep archive | ONLY milestone sessions | n/a |

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
L1 Pipeline: {one line}  L2 MAD: {one line}  L3 GPVS: {one line}
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

## PART C — STANDARD CLOSING PROMPT (paste at session end)

**This prompt is the highest-leverage object in the protocol.** A close that folds items
forward without regenerating an order grows the list BY CONSTRUCTION — that is the loop.

```
CLOSE S{N}, my buddy.
1. MISSION: did we complete the DECLARED mission? Yes or no, in one line. Not "did we fix
   everything we found" — a session that ships one thing and logs six is a SUCCESS.
2. FINDINGS: list every weak point found this session with its evidence, whatever the
   mission was. Suppressing a finding is worse than acting on it out of order.
3. WRONG: list every claim that turned out false this session, and what caught it.
4. ROOTS: re-analyse. Is each finding an existing root or a NEW root? A new root may
   re-rank everything above it.
5. REGENERATE docs/GNI_TARGET_AND_ORDER.md — dated, superseding, NEVER appended. Include
   CHANGED THIS REGENERATION: one line per item closed / merged / retired / re-ranked,
   plus a DECISION line for every ruling made this session (what we chose, over what, why).
   Apply the retire clause: below the line for three regenerations = closed as accepted or
   promoted with a written reason. Dropping one silently is neither.
6. DECLARE next session's mission, from the TOP of the regenerated order.
7. Build docs/HANDOFF_S{N}.md from Protocol Part B. Caps are HARD. STATE ONLY, no queue.
8. TRAPS: promote each durable trap into docs/GNI_RULES.md with an ID, or give it an expiry
   condition and keep it. No trap rides forward unchanged twice.
9. RULES: append only what S{N} EARNED (1-3 lines each, with ID, no number gaps).
10. CONTRACT.md: edit ONLY if a rule of engagement changed. Log it in the version log.
11. Diary: <=10 lines, only if the session earned it.
12. End by printing the LOAD CHECK block. Then stop — no summary essay after it.
```

## PART D — STANDARD OPENING PROMPT (paste at session start)

```
OPEN S{N+1}, my buddy — warm as always, lean on tokens.
0. The handoff is ATTACHED (container is empty; repo is private — never try to clone).
1. Read docs/HANDOFF_S{N}.md ONCE, carefully. Then read docs/GNI_TARGET_AND_ORDER.md —
   that file holds the declared mission and the ranked order. If this is a new model's
   first GNI session, also read docs/CONTRACT.md (attached in that case).
2. Echo ONLY the LOAD CHECK block. Max 12 lines total.
3. Do NOT re-explain history, re-audit closed items, or re-derive a queue — the order file
   IS the queue. Handoff claims are LEADS; BEV before acting on any of them.
4. WORK THE TOP OF THE ORDER. Not the newest finding, not the most interesting one.
   FRESHNESS CONFERS NO PRIORITY. If you believe the order is wrong, say so and propose a
   re-order — do not silently work something else.
5. Then wait for my go.
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

## PART F — EXPECTED SAVINGS
Old: close ~8-12K output + open ~30-40K input + ~2-3K re-explanation.
New: close ~3-4K output (handoff + regenerated order) + open ~4-5K input + ~0.3K echo.
Transfer overhead drops roughly 60-70%. The regeneration costs slightly more than v1's fold —
and buys the only thing that stops the list growing by construction.

## VERSION LOG
- v1 — S55 (2026-07-06). Born with the Transfer Protocol; queue lived in the handoff.
- v2 — S82 (2026-08-17). Rebuilt against CONTRACT v4/v5 after a full read showed the prompts
  had never been updated: Part B's `QUEUE (<=25)` removed (it contradicted v4 and would have
  restored the queue by template alone) and replaced by an ORDER pointer, plus new WRONG and
  expiring-TRAPS sections; Part C rewritten from 4 steps to 12, now the order-regenerating
  close the loop-hole diagnosis calls for; Part D now reads the order file and states
  work-the-top / freshness-confers-no-priority; Part A gains the order file, fixes the
  `GNI_RULES.md` path to `docs/`, and marks `STATUS.md` a fossil. Mirrored from Project Lens
  by reference-and-mirror, never blind copy; logged on both sides.
