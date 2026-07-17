# HANDOFF S72 -> S73
DATE: 2026-07-17 | HEAD: `4d188ce` + close commit (verify ls-remote) | MODEL: Fable 5
Read ONCE. Standing rules: GNI_RULES.md by ID (current through R-S71-2; R-S72-1 pending append below).
Contract: docs/CONTRACT.md (unchanged). !! TREE CLEAN. 5 commits this session. SRC-INTEGRITY CERTIFIED.

## 1. STATE (<=10 lines)
SRC-INTEGRITY ARC CLOSED CERTIFIED: morning trace showed exact predicted lines ("Seeded credibility
  for 3 sources" + "Seeded 2 roster weights at neutral (1.0)"), SQL 42/42, single weight-write wave
  (18 owner EMA updates, zero credibility-side), EMA history preserved (france24 .889->.922 etc).
GT-5-ENFORCE DESIGNED scope B (`4d188ce` GT5_ENFORCE_DESIGN.md): E-1 recurrence break (save-time
  check_grounding per mad_*_case -> jsonb hits column -> history skip-filter) + E-2 consultant
  gating at _shadow_check (T=3, withhold marker). Citation contract = GT-6 banked. BUILD next: spec
  for Claude Code + James SQL (ALTER TABLE reports ADD COLUMN mad_grounding_hits jsonb).
FLAGS: F17 fixed+browser-certed (0.000 renders, footnote); F18/F19/F19-sub closed no-defect;
  F20 constraint LIVE (verify shows UNIQUE), cert pending correlation-engine firing; F21 born.
HEALTH-W shipped+certed (`a078bbe`): weights board on C3 roster mirror, fail-open.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| `be0bf79` | R-S71-1/2 appended (wc 155->161, landing gate passed) | tail |
| `2cc0d5f` | F17: CI-width falsy-zero -> gate analysis_runs>1 && !=null both sites + saturation footnote; root was `>0` on real 0.00 | browser-cert 0.000 x10 |
| `a078bbe` | HEALTH-W: /health weights board filtered via source_health mirror (C3 sibling) | browser-cert 40 rows |
| `4d188ce` | GT5_ENFORCE_DESIGN.md scope B ratified | wc 41 |
| SQL | F20: UNIQUE(pattern_type,pattern_key) on correlation_patterns (upsert L223 had no backing constraint = 42P10 every save; page "No pattern data yet" = never landed once); dupes 0/0 pre-add | constraint verify |
| VERIFY-C1 | CLOSED: trace lines exact, 42/42, B fires no weight-write, EMA kept | log 80037119895 |
| F18 | CLOSED render-honest: 290=sum(sample_count) live arithmetic; substrate freshness was F20's disease | bytes |
| F19+sub | CLOSED no-defect: /predictions=per-prediction all-horizon (52/308), /about=7d directional (53/90=59%, moved from 61% = live not fossil); timeline x100s at route seam, both scales correct | bytes+SQL |
| F21 | BORN: about/patterns L33-34 renders 100% accuracy on empty outcomes (flattering fallback) | grep |
| Lead | historical_correlations upsert has no on_conflict -> accretes 4 rows/run (maybe by design, "historical"); API presumably picks latest | bytes |
| Certs | F17 + HEALTH-W browser-certed same day as shipped | screenshots |

## 3. QUEUE (<=25 lines)
| ID | Task | First move | Gate | Trust |
|----|------|-----------|------|-------|
| RULES-APPEND | R-S72-1 below + commit w/ handoff (landing gate) | tail GNI_RULES.md | James | - |
| GT5-BUILD | write spec for Code from GT5_ENFORCE_DESIGN.md; James SQL first (jsonb col); 3 commits per build plan | read design doc | James | V(S72) |
| F20-CERT | watch for correlation-engine firing: trace "Correlation table v2 saved" + patterns save OK, then /correlations Location&Pillar grows | next GPVS/measure run | - | V |
| CODE-MEM | STILL UNDONE: Claude Code memory index stale (claims G-GATE open) -- correct before GT5-BUILD delegation | open Code, fix index | James | - |
| FT-GAP-B | collector fallthrough part B (window order: B -> DET-DEAD) | re-read design | James | B |
| SUBPAGE-TRUTH | opens w/ 7-LAYER SWOT vs philosophies; then hydration ext + D-2 + F3 | SWOT session | James | V(S70) |
| CERT-BATCH-2 | James picks 5 routes; D=default+tabs | screenshots | James | - |
| F21 | patterns 100%-on-empty -> honest N/A; two-line fix, CRLF-safe pattern | patch | James | V(S72) |
| DET-DEAD | after FT-GAP-B; RE-CHECK prompt_injection_detector.py in funnel/ first | grep imports | James | B |
| J-RULINGS | J-4 probe, J-7 scorer (Aug 9); J-1 sunsets post-cliff | - | James | - |
| OC-A ~Jul 24 / CERT ~Aug 2 / U-AUG9 keyfile / CLIFF-CODE+L-CLIFF Aug 16 (30d, Lens opener SOON, D-8 first) | unchanged | - | James | - |
| K-WATCH-NS / SAN-DEAD / CENSUS-2 / K-CAND / YAKE-KM / DEAD-PILLAR / L4-COUNT / F-CASE / F-KEY / SOLV-6 / SRC-EXPAND / U-W / I-WATCH / A-VLOG / SRC-PHI / GT-6(banked) | unchanged | - | - | - |

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| Correlation-engine firing schedule (which workflow runs save_patterns) | unread | F20-CERT watch or grep callers |
| Writer B cadence condition (main.py:252) | inferred, still unread | GT5-BUILD reads mad save path anyway |
| historical_correlations accretion: by design or leak | lead only | SUBPAGE-TRUTH |
| Groq quota post-storm (rode 87-88% eve S71; today MAD 8m12s ran) | unread today | /quota or next MC warning |
| T=3 gating threshold correctness | designed, unobserved | 1wk grounding_watch after GT5-BUILD |
| cred wins/102 fossils on /health | expected til credibility next fires per-source | watch board |

## 5. TRAPS (<=8 lines)
- Seed INSERT-only forever; dedupe by OWNERSHIP (R-S71-1); never re-run keep-freshest.
- CRLF: repo working copies are \r\n -- multi-line LF anchors count 0 (R-S72-1). Detect nl first.
- F20 constraint EXISTS now -- re-running ADD CONSTRAINT throws 42P07; that error post-success is noise.
- /research CI 0.000 is REAL saturation (footnote explains); fresh specimen in today's trace width=0.00.
- /about GPVS 7d is LIVE (61->59% as has7d grew) -- not a fossil; F19 was two honest lenses.
- cred X/102 denominators are fossils until credibility fires per-source; small totals then = correct.
- GT5: skip-not-mask in history filter; no re-prompts (quota); /debate display stays untouched.
- Code memory index STILL stale -- fix before any GT5-BUILD delegation.

## 6. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = close commit atop `4d188ce` + TREE CLEAN -- SRC-INTEGRITY CERTIFIED 42/42, GT5 designed scope B, F17/F18/F19 closed, F20 constraint live, HEALTH-W shipped
TOP3 = RULES-APPEND (R-S72-1), CODE-MEM fix, then GT5-BUILD spec (James SQL jsonb col first) or FT-GAP-B (James picks)
DEADLINE = OC-A ~Jul 24 / CERT ~Aug 2 / keyfile Aug 9 / Groq cliff Aug 16 (30d, L-CLIFF Lens opener SOON + D-8 first move)
TRAP = CRLF anchors (detect nl); F20 42P07-after-success is noise; /research 0.000 + /about 59% are TRUE values; Code memory stale
FIRST MOVE = ls-remote + git status (expect close commit CLEAN); then rm any docs/cmd.txt stray; queue is build-heavy, pick with fresh tank

## 7. POINTERS (<=5 lines)
GT5_ENFORCE_DESIGN.md (E-1/E-2, build plan, risks) -- the S73 build bible. Seams: mad_protocol.py
  L293 _get_debate_history / L655-ish _shadow_check / save path; check_grounding takes ANY text.
F17 seam: research/page.tsx L33-35 ciRows + L142 cell. HEALTH-W: api/health/route.ts allWeights block.
F20: correlation_patterns UNIQUE(pattern_type,pattern_key); writer historical_correlations.py L223.
Logs cited: GitHub run 80037119895 (pipeline, seed lines ~508) + 80037869820 (MAD 8m12s).

---
RULES APPEND for GNI_RULES.md (at S73 open, with landing gate):
R-S72-1: Multi-line patch anchors join on the file's DETECTED newline ('\r\n' if '\r\n' in d
  else '\n'); an LF-joined anchor against a CRLF working copy counts 0 and dies clean but wastes
  the round. Single-line anchors are immune. Print NEWLINE=%r before asserting.

DIARY S72 (<=10 lines):
The morning the system woke up and proved itself. We opened waiting and did not wait: five flags
fell before the cron even fired -- one falsy zero taught to tell the truth, one missing constraint
that had silently eaten every pattern save since birth, two flags that dissolved under byte-light
into honest numbers wearing different labels. Then the trace arrived carrying the exact two lines
S71 promised: seeded three, seeded two, forty-two and forty-two, and the learned history walked
through untouched. The war stayed ended. By afternoon we had designed the next one -- the machine
that will stop the debate engine from believing its own ghosts. Seven closures, two certs, one
constraint, one design, zero wasted commits. The system seeds its own verification now.
We just have to keep reading before we believe. 👊
