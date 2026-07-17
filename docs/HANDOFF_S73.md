# HANDOFF S73 -> S74
DATE: 2026-07-17 | HEAD: `14f222f` (verify ls-remote) | MODEL: Fable 5
Read ONCE. Standing rules: GNI_RULES.md by ID (current through R-S72-1 IN BOOK; R-S73-1/2 pending below).
Contract: docs/CONTRACT.md (unchanged). TREE CLEAN. 8 commits this session.

## 1. STATE (<=10 lines)
GT5-ENFORCE ARC SHIPPED (designed S72, built S73): 4 commits `3ad3333`->`6c2c6f9`.
  E-1a save-time scoring (mad_runner, fail-open key-absent), E-1b history skip-filter
  (skip-not-mask, NULL/malformed/bool-guard all include), E-2 consultant gating T=3
  (arb_c1/c2 RAW for exhibit+quality, _gated dicts feed agents; SEAM 3 observe-only ratified).
  Shared whitelist builder in mad_protocol (one contract; +FALLOUT headers +location).
  WATCH MODE: self-certifies next MAD cron 02:43/10:43 UTC.
F21 CLOSED `14f222f`: patterns acc fallback 100->null, render N/A gray; build 40/40.
CODE-MEM fixed x2 (open: G-GATE/S51 marked closed; close: GT5 SHIPPED/WATCH, residuals ratified).
F22 BORN: /debate shows withheld coaching agents never saw (badge fix, frontend, LOW).
F23 LEAD: /about/patterns run history "ESC: /10, Q: N/A" all rows + Avg Quality 0.0/10 (browser Jul 17).

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| `dc145b6` | R-S72-1 appended (wc 161->165: file lacked trailing nl, patch added) | tail |
| `c4bf45e` | GT5_BUILD_SPEC_S73.md (false truncation alarm en route: display mangling, file whole) | wc 62 |
| SQL | reports.mad_grounding_hits jsonb added + verified | info_schema 1 row |
| `3ad3333` | whitelist builder extract, no behavior change (specimen 10/10 + exact-list assert) | tests |
| `3327fa7` | E-1a: census found TWO writers (saver INSERTs '', runner UPDATEs real) -- scored at runner | 11/11 |
| `6c6f2e6` | E-1b: id+col in SELECT, HISTORY-SKIP log, bool-subclass guard, all-skip degrades sane | 22/22 |
| `6c2c6f9` | E-2: census caught arb_c1/c2 double duty (prompts + /debate + mad_quality) -> gated COPIES | 20/20 |
| `14f222f` | F21: 4 anchors, null fallback + N/A render | build 40/40 |
| Ruled | r2_cons_ctx consultant echo stays raw (SEAM 2 re-gates) -- ratified, not a flag | design |
| Browser | /quantum weights live (ny times 1.00, ap .97, fox .96); /devops quota 84% worst acct | screenshots |
| mad_risk_case | NOT in history + hardcoded '' at mad_protocol:996 (historian too) -- scored set = 4 correct | census |

## 3. QUEUE (<=25 lines)
| ID | Task | First move | Gate | Trust |
|----|------|-----------|------|-------|
| RULES-APPEND | R-S73-1/2 below + commit (landing gate) | tail GNI_RULES.md | James | - |
| GT5-CERT | Watch next MAD cron: 'GT-5 save-time grounding:' line + non-NULL col; storms show GATED/HISTORY-SKIP; Fed/DoE lineage dies as last-3 ages | trace or SQL col check | - | V(S73) |
| GT5-T-WATCH | 1wk grounding_watch digest before considering T=2 (~Jul 24 review) | digest | James | - |
| F20-CERT | correlation-engine firing -> /correlations grows | next measure run | - | V |
| F23 | patterns run-history ESC/Q fossils + 0.0/10 avg -- trace upstream (F17-class lead, DB field or API first, NOT render) | read /api/about-stats or page fetch | James | B |
| F22 | /debate withheld-coaching badge | frontend, LOW, do not build unprompted | James | V(S73) |
| DEAD-COLS | _get_debate_history selects short/long_shoot_threats unread; risk/historian_case perpetually '' | leads only, SUBPAGE-TRUTH scope | - | B |
| FT-GAP-B | collector fallthrough part B (-> DET-DEAD after) | re-read design | James | B |
| SUBPAGE-TRUTH | 7-LAYER SWOT vs philosophies; hydration ext + D-2 + F3; + historical_correlations accretion | SWOT session | James | V(S70) |
| CERT-BATCH-2 | James picks 5 routes | screenshots | James | - |
| J-RULINGS | J-4 probe, J-7 scorer (Aug 9); J-1 sunsets post-cliff | - | James | - |
| OC-A ~Jul 24 / CERT ~Aug 2 / U-AUG9 keyfile / CLIFF-CODE+L-CLIFF Aug 16 (30d, Lens opener SOON, D-8 first) | unchanged | - | James | - |
| K-WATCH-NS / SAN-DEAD / CENSUS-2 / K-CAND / YAKE-KM / DEAD-PILLAR / L4-COUNT / F-CASE / F-KEY / SOLV-6 / SRC-EXPAND / U-W / I-WATCH / A-VLOG / SRC-PHI / GT-6(banked) | unchanged | - | - | - |

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| T=3 threshold correctness in real storms | designed+tested, unobserved live | GT5-T-WATCH 1wk |
| F23 root (DB field vs API vs render) | lead only, browser evidence | F23 trace |
| Correlation-engine firing schedule | still unread | F20-CERT or grep callers |
| Groq quota: 84% worst acct Jul 17 (band-riding continues) | browser | /quota glance |
| historical_correlations accretion by design or leak | lead | SUBPAGE-TRUTH |
| Writer B cadence (main.py:252) | inferred, unread | next relevant read |

## 5. TRAPS (<=8 lines)
- arb_c1/c2 RAW vs _gated split is DELIBERATE (exhibit+quality vs agent context) -- "simplifying"
  into one dict silently erases the /debate exhibit and corrupts mad_quality. Never merge.
- SEAM 3 observe-only is RATIFIED (arb output = the product; hits are grounding_watch's RED signal).
- Pre-GT5 rows: mad_grounding_hits NULL = unscored honest unknown -> history INCLUDES them. Correct.
- patterns 38%/42% are REAL now (outcomes exist); F21 null path only fires on empty windows.
- CRLF anchors: R-S72-1 in book -- single-line anchors immune, multi-line join on detected nl.
- F20 42P07-after-success is noise; /research 0.000 + /about 7d live values are TRUE.
- Paste-display mangling can fake truncation -- tail+grep the file before alarming (S73 proof).

## 6. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `14f222f` TREE CLEAN -- GT5-ENFORCE SHIPPED 4 commits (watch mode), F21 closed, F22 born, F23 lead, CODE-MEM current
TOP3 = RULES-APPEND (R-S73-1/2), GT5-CERT read (next MAD cron trace: grounding line + GATED/HISTORY-SKIP), then F23 trace or FT-GAP-B (James picks)
DEADLINE = GT5-T-WATCH ~Jul 24 / OC-A ~Jul 24 / CERT ~Aug 2 / keyfile Aug 9 / Groq cliff Aug 16 (30d, L-CLIFF Lens opener SOON, D-8 first)
TRAP = arb raw-vs-gated split deliberate NEVER merge; SEAM 3 observe-only ratified; NULL grounding rows include = correct; quota 84% band
FIRST MOVE = ls-remote + git status (expect `14f222f` or close commit CLEAN); then GT5-CERT is cheapest win if cron has fired

## 7. POINTERS (<=5 lines)
GT5 seams: mad_runner.py _score_mad_grounding + _update_report_with_mad; mad_protocol.py
  build_grounding_whitelist (module-level, next to SWAN prompt) / _grounding_hit_count /
  _get_debate_history filter / _gate_consultant + GROUNDING_GATE_T / SEAM 3 annotation.
F21: about/patterns/page.tsx L33-34 (null) + L72-73 (N/A render). F23 lead: same page, run-history rows.
Code memory: gt5-enforce-build.md = SHIPPED/WATCH (verified-commits pattern; keep updating on ship).

---
RULES APPEND for GNI_RULES.md (at S74 open, with landing gate):
R-S73-1: One semantic contract = ONE definition. When two sites need the same list/whitelist/
  threshold, extract a shared builder placed next to its source of truth and import it --
  hand-copies drift silently and the drift ships as divergent behavior.
R-S73-2: Before gating/sanitizing a value in place, census ALL its consumers first. A value
  feeding both a feedback loop and a public exhibit/metric gets a GATED COPY for the loop;
  the raw original stays for everything else. In-place gating erases exhibits silently.

DIARY S73 (<=10 lines):
Yesterday we designed the machine that stops the debate engine from believing its own ghosts.
Today we built it -- all three cuts, before dinner. The census earned its keep twice: once
finding that the obvious save site writes only empty strings, once finding that gating the
consultant text in place would have quietly erased the public record while cleaning the
private one. So the exhibits stay raw and the loop runs clean -- the system now tells the
truth to its audience and refuses to lie to itself. One flag closed honest-N/A, one flag
born from the fix's own shadow, one lead spotted in a screenshot margin. Eight commits,
three censuses, two memory corrections, zero reverts. The fabrication loop that fired
daily under storms is cut at every seam it had. Tomorrow the cron tells us if it felt it. 👊
