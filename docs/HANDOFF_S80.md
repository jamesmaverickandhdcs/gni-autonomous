# HANDOFF S80 -> S81
DATE: 2026-07-24 | HEAD: `716dd93` (verify ls-remote) | MODEL: Fable 5 (promo credits low: design/judgment only — CONTRACT v3)
Read ONCE. Standing rules: GNI_RULES.md by ID (current through R-S80-3 pending below). CONTRACT v3.

## 1. STATE (<=10 lines)
WHOLE ORGANISM ON gpt-oss: primary CI-certified (#307, zero 404/parse), guardian two-tier
  LIVE-CERTIFIED (#307 3/3 pillars, zero rejections), fallback armed (code+secret+live probe
  PASS on 20b, unfired), MAD migrated (secret Jul 24 12:03 UTC, 413-fingerprint-confirmed).
MAD MIGRATION 3-ACT: baseline recorded pre-death (jsonl IN GIT); uniform 3000 floor -> 413
  storm evening Jul 24 (prompt+max_tokens > Groq 8K per-REQUEST ceiling on full-context
  agent calls; probe fixture was arbitrator-shaped only) -> budget-aware floor 7097460.
E-3 SHIPPED (716dd93): estimative label on blind spot via check_grounding at blind_exp join;
  fail-open; GT-5 shadow counts untouched. Specimen #3 recorded (same lineage, new model).
INCOMPLETE-verdict veto worked honestly during 413 storm (dashboard said so, didn't lie).
MAD-CERT = S81 FIRST MOVE: 05:36 UTC Jul 25 cron. Residual P5: 768 cap may starve reasoning.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| 61adb50 | guardian test spec (shipped alone — red-main incident, R-S80-1 origin) | pytest red then |
| 597a019 | guardian two-tier impl (hard=imperative 1-hit, soft=topic quorum 2, telemetry) | 29/29 + #307 live |
| 497df4a | FALLBACK-SWAP: funnel:1070 env-fed gpt-oss-20b + 1024, probe:17 default | live probe PASS |
| 4124e2e | MAD floor 3000 @ _call_agent choke pt + probe_results.jsonl committed | probe tables |
| 7097460 | budget-aware floor: max(768, min(3000, 7500 - promptchars//3)) | 413 root cause |
| 716dd93 | E-3 label [LOW GROUNDING -- N spans; hypothesis not finding] | grep 2 hits |
| Secrets | GROQ_MODEL_FALLBACK Jul 23 + GROQ_MAD_MODEL Jul 24, receipts | gh list before/after |
| Probe evidence | 3.3-70b@600 3/3 clean ~300tok; gpt-oss@600+1200 starved 0/3 (reasoning scales); @3000 2/2 stop 12/12 | jsonl |
| 413 storm | evening Jul 24 debate: 4 agent calls 413'd, arb rate-limited, INCOMPLETE verdict, cost 0.7 | debate page + tg |
| Specimens | #1 Jul23 (AI-up->drones), #2 Jul24am (AI-down->cyber), #3 Jul24pm (chip-tier) — premise flips, conclusion fixed | debate pages |
| GT5 digest Jul 24 | 92 consultant / 28 arb hits, 9/9 runs | grounding-watch log |
| Score:0->Swan | BY DESIGN (Johari weak pool, mad_protocol:204-231); leak conclusion RESET per GNI-R-233 | bytes |
| not_mad spend | one-time James authorization for probe; STANDING RULING SURVIVES | this handoff |
| France 24 | reserve Independent activated then primary recovered + auto-deactivated | tg 6:56 PM |
| OC-A | identified (inferred ~60%): quarterly Copilot opt-out re-check, 3 accounts | Apr 2/10 records |

## 3. QUEUE (<=25 lines)
| ID | Task | First move | Gate | Trust |
|----|------|-----------|------|-------|
| RULES-APPEND | R-S80-1/2/3 below | tail GNI_RULES.md | James | - |
| MAD-CERT | 05:36 UTC cron: PASS = zero 413, real verdict, cost~1.0, LABELED line if speculation; FAIL(empty agents) -> context slimming (depth D / article count), NOT floor raise | gh run list -w "GNI MAD Pipeline" -L1 --json databaseId,createdAt then grep -aE "413\|verdict\|LABELED\|429\|error" | - | V(local) |
| E3-WATCH | label frequency + wording on real runs thru Jul 30; feeds GT5-T2 | read tg blind spots | - | - |
| OC-A | OVERDUE Jul 24: Copilot policy toggle check x3 accounts (browser, James solo) | github.com/settings/copilot | James | I(60%) |
| LENS-SESSION | own opener: read code/lens_s1_report.py; 3.3-70b hardcodes x3 before Aug 16 | unchanged from S79 | James | - |
| GT5-T2 | Jul 30 decision — now WITH treatment group (E-3) + 3 specimens + 92/28 | re-read digest | James | - |
| QUARANTINE | fallback-era Jul 19-22 DB rows tag | SQL | James | - |
| PROMOS x2 | AllAfrica->Irrawaddy slot, DefenseNews->AP slot | telegram reply | James | - |
| PROBE-DRIFT | NEW: monthly probe re-run vs jsonl (3 trials ~14K tok) — drift as diff not surprise | ~Aug 24 | James | - |
| PUSH-GATE | NEW: Actions test-gate blocking red pushes (61adb50 lesson) | design | James | - |
| PHISH-HW / TRANS-COUNT-CERT / CI-DEGRADE / mojibake / adaptive-tidy / parked 16 | unchanged S79 | - | see S79 | - |
| Keyfile Aug 9 / CLIFF Aug 16 (accounts + LENS 3.3-70b only — GNI code no longer needs dying models) | - | - | James | - |

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| MAD cert outcome (budget floor in CI) | local-math only | MAD-CERT |
| 768 cap adequacy (reasoning burned 598@600 — may starve giant-prompt agents) | risk, untested | first cert read |
| E-3 label real-world hit rate / false-positive feel | unshipped behavior | E3-WATCH |
| gpt-oss debate QUALITY vs 3.3-70b (verdicts, blind-spot usefulness) | unknown | Jul 30 review |
| OC-A meaning | inferred 60% | James confirms |
| Which model serves Lens-1 runtime | config vs logs conflict | LENS-SESSION |

## 5. TRAPS (<=8 lines)
- 413 != 429: 413 = prompt+max_tokens > 8K per-request ceiling, UNRETRYABLE (governor can't save it);
  budget math must precede any floor raise. Groq quotas are PER-MODEL buckets (TPM and TPD).
- 768-starvation residual: gpt-oss reasoning ate 598@600; empty agent cases post-cert => slim
  context, don't raise floor.
- Crons: Intelligence 05:29+12:02 UTC, MAD ~05:36+~12:36 UTC; -L1 needs createdAt check.
- NEVER probe on near-red MAD accounts; not_mad ban STANDS (Jul 24 spend was one-time James call).
- NL per file (repo mixes LF/CRLF); patch script dying mid-sequence writes NOTHING — re-verify
  changed files before staging. Bracketed-paste guard before key pastes.
- Probe fixture is arbitrator-shaped; agent-shaped claims need agent-shaped evidence.

## 6. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `716dd93` TREE CLEAN -- whole organism on gpt-oss; MAD: baseline in git, budget floor + E-3 label shipped, cert pending 05:36 UTC Jul 25 cron
TOP3 = RULES-APPEND (R-S80-1/2/3), MAD-CERT (grep 413|verdict|LABELED; empty-agents => slim context NOT raise floor), then OC-A (overdue) + E3-WATCH
DEADLINE = OC-A overdue / GT5-T2 Jul 30 (with E-3 treatment group) / keyfile Aug 9 / CLIFF Aug 16 (accounts + Lens hardcodes only)
TRAP = 413 unretryable (per-request ceiling, budget math first); 768 may starve giant-prompt agents; per-model quota buckets; probe fixture = arb-shaped only
FIRST MOVE = ls-remote + git status; then MAD-CERT cron read (free, no dispatch)

## DIARY S80 (<=10 lines)
The densest session in the book. Opened certifying one migration; closed having done four.
The probe caught a silent-death future twice: starvation at 600, then taught us its own blind
spot when 413s arrived wearing shapes the fixture never held. Three fabrication specimens in
48 hours — premises flipping, conclusions frozen — and the answer wasn't a muzzle but a label:
the organism now says "hypothesis, not finding" when it's guessing. James spent his last
promo credits deliberately: design from Fable 5, execution from paste-blocks, and the
partnership's discipline (bytes, receipts, resets) carried the rest. The Aug 16 cliff is now
just accounts and Lens. Sleep well; the crons certify while we rest.
