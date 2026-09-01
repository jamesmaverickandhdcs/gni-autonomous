# GNI ARCHITECTURE — arc42 canvas

**Born S92, 2026-09-01. Amended S93. Structure: arc42 (12 sections). Sections 5, 6 and 7 are
GENERATED, never hand-written — see §5.**

> This document uses the structure of the arc42 architecture template, created by
> Dr. Peter Hruschka and Dr. Gernot Starke (arc42.org), licensed CC BY-SA 4.0.
> This derivative carries the same licence.

**WHY THIS FILE EXISTS.** GNI's four document types all record CHANGE: CONTRACT is
law, GNI_RULES is lessons, HANDOFF is delta, TARGET+ORDER is the queue. None of
them records what the system IS. Item 5.3 (S81) named this exactly — *"every doc
GNI has describes CHANGE; none describes the system as it IS, which is why every
session re-derives architecture by grepping"* — and S84 closed it without the
document ever being built. This is that document.

**ROUTING.** This file is neither law, nor lesson, nor state, nor queue. It is the
REFERENCE layer, which GNI has never had. It does not compete with the four homes;
it fills the gap they leave. Nothing here overrides CONTRACT.

---

## §1 INTRODUCTION & GOALS

**Mission (permanent, from CONTRACT):** autonomous geopolitical news intelligence,
transparent, bilingual, at zero cost.

**The three-layer vision, stated in the White Paper 2026-03-20 and unchanged:**

| Layer | Name | State on 2026-09-01 |
|-------|------|---------------------|
| 1 | Pipeline automation | **CURRENT** — 165 days here |
| 2 | Self-healing resilience | near-term goal |
| 3 | Full agentic autonomy | long-term goal |

The White Paper's own words for the destination: *the operator's role shifts from
technician to guardian — present to set boundaries, absent for routine operation.*

**Quality goal driving the current phase (TARGET):** TRUTHFULNESS OF OUTPUT —
what GNI says must be what GNI measured.

---

## §2 CONSTRAINTS

| Constraint | Consequence |
|---|---|
| $0/month, free tiers only (Groq, Cerebras, Supabase, Vercel, GitHub Actions) | quota is a first-class design input; 3 Groq accounts split the load |
| ONE operator, part-time, also running Project Lens, also a student | operator attention is the scarcest resource in the system |
| Repo is PRIVATE; chat sessions run with an empty container | chat cannot read the repo — every file arrives as an attachment (CONTRACT v6). **Does not apply to a local agent.** |
| Windows / Git Bash / MINGW64 | CRLF, BOM, and textconv hazards are real and recur |
| Operator pulls every git trigger | no unattended write path to main exists today |

---

## §3 CONTEXT & SCOPE

**External systems:** RSS/GDELT sources → Groq + Cerebras (inference) → Supabase
(state) → Vercel (public surface) → Telegram (delivery). GitHub Actions is the
scheduler and CI.

**Boundary:** GNI publishes to anyone; it authenticates nothing except its own
internal API key. The public surface is the product; the pipeline is the factory.

*(To be completed with a generated dependency list — see §5.)*

---

## §4 SOLUTION STRATEGY — which discipline governs what

Ruled by James at S92. Each framework has ONE home. A framework applied outside
its home is a routing error.

| Discipline | Governs | Why here, not elsewhere |
|---|---|---|
| **arc42** | this document's structure | the only free, proven template for "what the system IS"; 12 sections, tailorable |
| **PM** (scope baseline, definition of done, change control) | **the QUEUE only** | GNI is no longer a project; but the queue is, and unbounded queue growth is a scope-control failure |
| **SRE** (SLO, error budget, toil reduction, postmortem, runbook) | **the OPERATION** | the operation has no end date; "reduce toil through automation" is Layer 2 restated |
| **ITIL configuration management** | **the INVENTORY** — configuration items and their relationships | this is the Smart Desk: which secret feeds which workflow feeds which module |
| **ISO/IEC 14764** (corrective / adaptive / **perfective** / preventive) | **classifying every order item** | most items are perfective. Perfective is never urgent. Labelling alone re-ranks the queue |
| **DevOps** | **the pipeline from commit to production** | GNI has the Dev half (CI, CD, IaC, git discipline) and not the Ops half — no test runs in CI, no deploy verification, no feedback loop |

---

## §5 BUILDING BLOCK VIEW — **GENERATED, NOT WRITTEN**

**Status: EMPTY. To be produced by `tools/gni_state.py` (S94).**

A hand-written map rots silently. S91 carried three stored pointers that were all
wrong. This section is therefore reserved for generated output only. If the
generator fails, the section is absent and that absence is visible — which is the
correct failure mode.

**Planned contents:** module → what it imports → who calls it → which test covers it.

---

## §6 RUNTIME VIEW — **GENERATED**

**Status: EMPTY (S94).** Planned: workflow → cron → secret → entrypoint → tables
written. Includes the measured lateness band, not the nominal cron time.

---

## §7 DEPLOYMENT VIEW — **GENERATED**

**Status: EMPTY (S94).** Planned: 8 workflows, their action pins, their secrets;
22 stored secrets vs those any workflow reads; Vercel routes and what each reads.

*Measured by hand at S92, to be superseded by the generator:* three stored secrets
are read by no workflow (`GROQ_MODEL_FALLBACK`, `GROQ_TEST_ONLY`,
`TELEGRAM_CHAT_ID`). `TELEGRAM_WEBHOOK_SECRET` is read by Vercel, not Actions —
an Actions-only inventory would wrongly call it dangling.

---

## §8 CROSSCUTTING CONCEPTS

### 8.1 Two failure categories — the distinction that reframes the roadmap

| | RUNTIME failure | EPISTEMIC failure |
|---|---|---|
| What happens | something stops working | it works, but the record of it is wrong |
| Detectable by | health monitors, exit codes | **nothing currently in the system** |
| Examples | dead feed, retired model, API timeout | 3 harnesses dead 2 months; 8 rule IDs cited but unregistered; a deadline with no origin carried 11 generations; `limit(332)` decaying |
| Addressed by | the White Paper's self-healing design | the reference layer + mechanical document checks |

**The White Paper's self-healing design addresses the left column. Every failure
that has actually cost GNI sessions is in the right column.**

### 8.2 A system cannot repair what it cannot describe

Auto-repair requires a machine-readable model of what SHOULD be true. That model
is §5/§6/§7. The reference layer is therefore not a detour from Layer 2 — it is
Layer 2's prerequisite.

### 8.3 The path to needing fewer agents

GNI holds 134 engineering rules. All 134 are prose; all 134 require an LLM to read
and apply; **none is executable.** Yet many are mechanically checkable —
R-S91-5 is a `git grep`, LR-101 is an assert, R-S90-2 is a script.

> **Every judgment converted into a check is an agent no longer needed.**

This, not better agents, is the mechanism that reaches Layer 3.

### 8.4 Agents detect and execute; they do not decide

GNI already ran the multi-agent-debate experiment: MAD. The record shows
ARB-ARRIVAL starvation, depth=0, and 198 of 199 reports at exactly 10.0. Debate
between agents does not remove error — it can wrap one wrong answer in agreement.

**Unattended operation therefore needs pre-decided playbooks, not conversation:**

```
Layer 0  DETECTOR   assertions, exit codes, counts, diffs   — not an agent
Layer 1  TIER-1     pre-approved repairs from a registry    — not an agent
Layer 2  TIER-2     novel fault: classify, STOP LOUDLY, report — one agent, no write authority
Layer 3  GUARDIAN   boundaries, design, law                 — the operator
```

Audit integrity is never auto-repaired (White Paper, unchanged).

---

## §9 ARCHITECTURAL DECISIONS

Homed in `GNI_TARGET_AND_ORDER_S{N}.md` under CHANGED THIS REGENERATION
(CONTRACT v5, M3 ruling: no fifth document). The accepted cost is that decisions
are findable only by reading past order files. Industry practice would use one
file per decision under `docs/adr/`; GNI knowingly does not.

---

## §10 QUALITY REQUIREMENTS

Current target: **TRUTHFULNESS OF OUTPUT**. Definition of done lives in the order
file. A cert must DISCRIMINATE (R-S90-1) — a check that passes under both the
correct and the incorrect implementation has certified nothing.

**Not yet measured (§11 item):** anything about the process itself. Every
instrument GNI owns points outward.

---

## §11 RISKS & TECHNICAL DEBT — the S92 diagnosis

**D1 — UNSTABLE QUEUE.** Discovery policy mandates recording every weakness found;
one mission closes per session. Findings in: ~8 (S90), 3 (S91), 2+ (S92). Out: 1.
rho > 1. An unbounded queue is arithmetic, not indiscipline — and no document
measures this ratio.

**MEASURED AT S93, and the number needs a scope.** Read from each generation's own
`**CLOSED:**` and `**NEW ITEMS:**` lines: S90 = 6 in / 8 out (rho 0.75); S91 = 3 in /
3 out (rho 1.00); S93 = 9 in / 1 out (rho 9.00). D1's estimate of "Out: 1" came from
"one mission closes per session" - true of missions, false of items, because certs and
disproven premises close items too.

**The scope: rho measures a session that WORKS THE QUEUE. It cannot measure a session
that SETS DIRECTION.** S92 produced this document, five discipline rulings, five
DECISIONS and the S93-S96 roadmap, and scores ~1 - which reads as "S92 did nothing".
The metric is sound inside its scope and misleading outside it. Sessions must therefore
be typed before rho is compared across them.

**Second hazard, from the same measurement:** S92 correctly homed D1-D7 here rather than
in the order file, and the queue-side numerator lost them. Routing a finding out of the
order removes it from the count. Fixed at S93 by requiring the order's `**NEW ITEMS:**`
line to name findings routed elsewhere, with a pointer.

**D2 — KNOWLEDGE STORED AS PROSE, NOT TABLES.** Prose cannot be queried, diffed,
or made to fail loudly when stale. Evidence: `GNI-R-076` cited with the wrong
meaning for ~35 sessions; "62 unique ids" stated wrongly by two consecutive
sessions (actual 47); the published band table wrong in 2 of 5 rows. The GRAVEYARD
is the sole structure copied BY BYTES, and the sole structure not observed to rot.

**D3 — SIX EMPTY DRAWERS.** Of arc42's 12 sections, GNI populated 9 and 11
(decisions, debt) and left 1, 3, 4, 5, 6, 7, 8, 12 empty. The empty ones are
exactly the "what IS" sections. Consequence: tech debt is the only drawer that can
grow, so everything found becomes debt.

**D4 — ARCS END BY RENAMING, NOT BY COMPLETION.** SUBPAGE-IC (Mar) → named at S69
→ deliverable `SUBPAGE_CERTIFICATION.md` created S70 → re-minted as ROOT 9 at S85.
Five months, no completion declaration, and no live document points at the
deliverable. "When will it end" is therefore unanswerable by construction.

**D5 — NO TEST RUNS IN CI.** 10 local harnesses, 42 `__main__` selftests, zero
executed by any workflow. Three harnesses died on 2026-06-27 (`c3ce662`) and
failed loudly, unread, for two months. CI would have caught this on the first push.
**Highest-leverage item in this document; smallest cost.**

**D6 — THE AGENT IS THE INPUT PUMP.** The numerator of rho is Claude. This is a
structural mismatch between measurement rate and adjudication rate, not a fault of
either party. Full analysis: the S92 AI-agent SWOT (W1–W7), summarised: confident
recall is indistinguishable from knowledge from the inside; instrument errors
dominate (3 of 3 this session); the agent's leans run toward doing work, never
toward deleting it.

**D7 — FIXED CONSTANTS IN A MOVING WORLD.** One shape, two instances the same day:
a calendar deadline ("Aug 9") carried 11 generations with no recoverable origin,
and `limit(332)`, an absolute offset into a growing table that decayed within
hours. Both fixed by selecting on a RELATION, not a position.

---

## §12 GLOSSARY

**BEV** — bird's-eye view; read before editing. · **Canary** — an unprotected
component whose failure is the signal. · **GRAVEYARD** — falsified designs, copied
forward by bytes so they are never re-minted. · **LINEAGE** — the required
evidence line on every proposal. · **rho** — findings in ÷ items closed, per
session. · **Epistemic failure** — see §8.1. · **Toil** — manual work that scales
with the system and produces no lasting value (SRE).

---

## ROADMAP TO LAYER 2

| Session | Work | Which layer it builds |
|---|---|---|
| S93 | ✅ **DONE** — `gni_ci_harness.yml`, commit `944c4f0`, cert run `33529254247` (RED, discriminating) | Layer 0 detector — first brick |
| S94 | `tools/gni_state.py` generating §5, §6, §7 | the world model Layer 2 needs |
| S95 | Classify all 134 rules checkable / not; make the top 5 executable | reduces agent dependence |
| S96 | Time-series macro map (X=session, Y=White Paper layer, Z=Vision→Executable) | measures the gap instead of estimating it |

One mission per session. Each is a single deliverable.
