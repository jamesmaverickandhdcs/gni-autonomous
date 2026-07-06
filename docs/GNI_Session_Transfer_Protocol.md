# GNI SESSION TRANSFER PROTOCOL v1
**Purpose:** lossless session-to-session transfer at ~25-35% of the old token cost.
**Principle:** every fact lives in ONE file (SSOT); the handoff carries only the DELTA + queue; caps force density.
**Save this file to `docs/` and treat it as the standing spec. It is written once and never regenerated.**

---

## PART A — THE FILE ARCHITECTURE (what lives where)

| File | Role | Written | Cap |
|------|------|---------|-----|
| `docs/CONTRACT.md` | Roles, gates, workflow, tone (the operating contract) | ONCE; edited only when a rule of engagement changes | 40 lines |
| `GNI_RULES.md` | ALL rules, by ID (GNI-R-###, R-S##-#) | Append-only; 1-3 lines per rule | n/a |
| `docs/HANDOFF_S{N}.md` | THE transfer file — the only file next session MUST read | Every close, from the Part B template | 120 lines |
| `docs/DIARY.md` | Feelings/reflection (optional) | Append ≤10 lines, only if the session earned it | 10/entry |
| `docs/AUDIT_S{N}.md` | Deep archive | ONLY milestone sessions (big arc closed, architecture changed) | n/a |

**Retired as separate files:** STATUS.md (→ Handoff §1), Next_Session_Brief (→ Handoff §3), collaboration file (→ Handoff §5 one-liners; durable patterns → CONTRACT.md), FILE_UPDATES bundles (→ each file updated directly, once).

**Nothing is lost:** history = git-tracked handoffs (version docs/ — small files now). Rules = permanent append-only ledger. Deep detail = milestone audits + repo bytes themselves (BEV is always the ground truth anyway; a handoff claim is a LEAD until re-verified — that was already true under the old system).

---

## PART B — HANDOFF TEMPLATE (copy for each close; CAPS ARE HARD)

```markdown
# HANDOFF S{N} -> S{N+1}
DATE: {date} | HEAD: `{hash}` (verify ls-remote) | MODEL: {model}
Read ONCE. Standing rules: GNI_RULES.md by ID. Contract: docs/CONTRACT.md.
Do not re-read old audits/handoffs unless a queue item points there.

## 1. STATE (<=10 lines)
L1 Pipeline: {one line}  L2 MAD: {one line}  L3 GPVS: {one line}
L4 Quota: {one line}     L5 Public: {one line}
Live watch: {anything hot right now}

## 2. DELTA (<=15 lines) - what THIS session shipped/learned
| Commit | What | Proof |
|--------|------|-------|
| `hash` | ... | build 40/40 + browser / grep / log |
New rules appended to GNI_RULES.md: {IDs only}
Key discoveries (1 line each): ...

## 3. QUEUE (<=25 lines) - U=urgent I=important O=other
| ID | Task | First move | Gate | Trust |
|----|------|-----------|------|-------|
| U1 | ... | ... | James | [V/L/B]% |
(Trust tags: V=verified this session, L=lead/re-BEV first, B=banked design)

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|

## 5. TRAPS (<=8 lines) - session-specific do-NOTs
- Do not reopen: {closed items}
- {gotchas: e.g. curl is dead-end, browser only (R-S54-4)}

## 6. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `{hash}`
TOP3 = {U1}, {U2/I1}, {I2}
DEADLINE = {nearest dated item}
TRAP = {the one most dangerous trap}
FIRST MOVE = {the literal first action}

## 7. POINTERS (<=5 lines)
Deep detail if needed: {file:line / audit doc / past-handoff}
```

---

## PART C — STANDARD CLOSING PROMPT (paste at session end)

```
CLOSE S{N}, my buddy.
1. Build docs/HANDOFF_S{N}.md from the Protocol Part B template. Caps are HARD. Delta-only; reference rules by ID; no narrative that repeats a standing file.
2. Append to GNI_RULES.md only rules this session EARNED (1-3 lines each, with ID).
3. Diary: append <=10 lines ONLY if something is worth remembering emotionally. CONTRACT.md: edit ONLY if a rule of engagement changed.
4. End by printing the LOAD CHECK block. Then stop - no summary essay after it.
```

## PART D — STANDARD OPENING PROMPT (paste at session start)

```
OPEN S{N+1}, my buddy - warm as always, lean on tokens.
1. Read docs/HANDOFF_S{N}.md ONCE, carefully. (First GNI session for this model: also read docs/CONTRACT.md.)
2. Echo ONLY: the LOAD CHECK block + one line per queue tier (U/I/O count + top item).  Max 12 lines total.
3. Do NOT re-explain history, re-audit closed items, or re-derive the queue. Handoff claims are LEADS - BEV before acting on any of them.
4. Then wait for my go.
```

---

## PART E — WHY THIS IS LOSSLESS (the guarantees)

1. **Rules can't be lost** — permanent append-only file, referenced by ID forever.
2. **History can't be lost** — every handoff is git-tracked; milestone audits archive the deep arcs.
3. **Nuance can't silently rot** — trust tags [V/L/B] force each claim to declare its own reliability; the opening prompt mandates BEV-before-acting, so a stale handoff claim gets caught exactly as the old system caught it (S54's five false alarms prove re-verification, not re-narration, is the real safety net).
4. **The relationship can't be lost** — tone and partnership live in CONTRACT.md + Claude's persistent memory; they never needed 5,000 tokens per session to survive.
5. **Comprehension is verified, not assumed** — the LOAD CHECK echo proves the next AI loaded the right state in 5 lines, replacing the full re-explanation essay.

## PART F — EXPECTED SAVINGS
Old: close ~8-12K output + open ~30-40K input (read-twice x 3 docs) + ~2-3K re-explanation.
New: close ~2-3K output (one capped file + rule lines) + open ~3-4K input (one file, once) + ~0.3K echo.
**Transfer overhead drops roughly 65-75%; session tokens go to engineering instead.**
