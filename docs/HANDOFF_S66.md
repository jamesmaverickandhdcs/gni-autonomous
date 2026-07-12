# HANDOFF S66 -> S67
DATE: 2026-07-12 | HEAD: `b13d748` + S66-close docs commits (verify ls-remote, count don't assume) | MODEL: Fable 5
Read ONCE. Standing rules: GNI_RULES.md by ID (current through R-S66-3). Contract: docs/CONTRACT.md (unchanged).

## 1. STATE (<=10 lines)
W-AUTO CLOSED end-to-end: 4a/4b/4c shipped, browser-verified live (R-S54-4) --
  AP GN + Stimson blue "Reserve serving", 12 stale-gated yellow, 7-card legend,
  "0=down" dead. Down-tile=2 is CORRECT (reserve-masked counts as down per spec).
KEY-MAP CLOSED: 4 commits, census-gated (344 phantom kills, 0 signal loss after
  demonym/verb/iran* rulings). First flight CLEAN on run #281 @ 24e1bce (c1-c3;
  c4 flies next run, classifier-only). S1 263->178; staging 9/9; MAD completed.
R-VERIFY-2 CLOSED: STALE-GATED warns PROVEN (12), columns PROVEN (fetch_ok/served_by
  populated, legacy NULLs fall back), Defense News PARTIAL -- transport proven,
  yield 0 twice (chronically stale reserve, 41-110h entries). Slot-transport
  semantics verified at all 3 layers (collector L520 / writer / route). Quota 93/95% both MAD accts.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| `db28a7a` | W-AUTO-4a: STATUS_CONFIG +4 states, desc? optional | raw diff cleared |
| `4bc81e3` | W-AUTO-4b: STATUS_GROUP tile regroup, legend rewrite, card borders + chart caption (approved scope adds) | raw diff cleared; live render verified |
| `4b611a2` | W-AUTO-4c: HEALTHY_CLASS (healthy+stale-gated+silent) in MC Check4 + dev-hub L30; 3-state copy killed L84/L123 | raw diff cleared; thresholds byte-same |
| `198a306` | KEY-MAP-1: matching.py -- lookaround boundaries, '*' stem convention, \s+ phrase splice, lru_cache, 41/41 selftest | full file read |
| `1c76b46` | KEY-MAP-2: 14-site funnel sweep + stars per rulings (demonyms iran*/russia*/israel*/taiwan*/europe*; euro/war/chip exact; enforced disappearance* added) | census: 344 kills all phantom/ruled; article-level HS check |
| `24e1bce` | KEY-MAP-3: sensor L4 3-site swap, verb stems (occup*/nationaliz* truncated), ban/fire exact-by-design, iran* brand proxy (iranian* removed), C2 dedup hotfix rstrip('*') | mini-census 47 flips all attributed |
| `b13d748` | KEY-MAP-4: byline startswith fix (check NEVER fired since birth) + opinion phrases any_match over shared text | behavioral table, Jane Mayer case flips |
| RECENCY-DEAD found | L747 `art` vs `article` NameError swallowed by bare except -- recency+velocity bonus never applied to any article, ever | executor execution proof |
| SAN-DEAD found | sanitize (L1108) runs before scoring (L1184): 'invasion'/'proxy war'/'occupation' can never match in scoring lists | run_funnel order read |
| IRRELEVANT polarity | 'sport' killed transport/chokepoint stories, 'dating' killed Pentagon-AI story -- 4 articles/day rescued | census site-1 |
| DN chronic-stale | Defense News reserve: transport OK, yield 0, two consecutive runs | both GH logs |
| NYT promotion proposal | 46 days clean on Stimson slot; proposal is ADVISORY (accepts no replies) | Telegram; webhook rejected 'primary'/'yes' benignly |

## 3. QUEUE (<=25 lines)
| ID | Task | First move | Gate | Trust |
|----|------|-----------|------|-------|
| K-WATCH | TOP: KEY-MAP observation window -- compare 2-3 forensic traces pre/post 24e1bce: S1 pass rate, stage1_match_count mean (~1.77->1.41 expected), Top-22 composition, MAD input quality | pull today 0537 vs 1131 traces | - | B |
| RECENCY-DEAD | Fix L747 art->article + kill bare except (assert per LR-104). Revives +5..+1 recency & +2 velocity = selection-shifter: land ONLY after K-WATCH baseline read | read L740-770 | James | V(diagnosis) |
| G-TUNE | ~Jul 15: alias whitelist (fed<->federal reserve, us-iran variants, demonym<->country; share sensor KNOWN_ACTORS anti-L-CLIFF) + consultant Class-B scrub + G-GAP-1; re-measure THEN enforce. New adds: chip* decision, source-aware actor hinting (replaces iran* brand proxy), 'ban'/'fire' narrowing review | grounding digest | James | B |
| PROMOTE-NYT | Check Stimson RSS URL manually (moved feed?) then promote NYT to primary in rss_collector.py or revive. Roster edit = own commit, after K-WATCH | curl/browser the feed | James | B |
| FT-GAP | Widened: C2 recovery criterion + reserve POOL RANKING must weigh feed cadence (DN proof x2). Consider fresher GEO reserve for AP GN slot | collector L470-510 + pool | James | V(diagnosis) |
| SAN-DEAD | Design: score pre-sanitized text vs add neutral forms to lists | read sanitize vocab | James | V(diagnosis) |
| CENSUS-2 | Census instrument v2: article-level score diff pass (R-S66-1) | extend scratch script | - | V(design) |
| YAKE-KM / DEAD-PILLAR / L4-COUNT | YAKE L713 inverted containment (semantic, own item); sensor _suggest_pillar dead code, 'ai' in said/domain; L4 env counter unread | read each | James | B/unread |
| CHORE-IGNORE | Add *_GNI_Forensic_Trace_*.xlsx (repo root) to .gitignore -- scheduled runs drop them in tree | one line | - | V |
| F-TILES / F-CASE / F-KEY | unchanged S65 fossil sweep candidates | James picks | James | B |
| L-CLIFF | With Lens session; Aug 16 cliff -- quota 93/95% today sharpens urgency | Lens opener | James | V(scope) |
| SOLV-6 | +2 data points: 94591 metered S65; 93365/91602 both accts today | - | - | B |
| SRC-EXPAND / OC-A/B / U-AUG9 / U-W / I-WATCH / A-VLOG | unchanged (OC-A matures ~Jul 24) | - | - | - |

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| KEY-MAP live effect on Top-22 / MAD quality | unknown | K-WATCH 2-3 runs |
| Stimson primary revivable (URL moved vs dead) | unknown | PROMOTE-NYT first move |
| Sensor signature_id one-time discontinuity (starred tokens in ids) | 90% benign self-heal | watch one window |
| c4 classifier behavior live (first flight = next run) | 90% | next GH log |
| IRRELEVANT list residual shapes beyond 24h window | 80% clean | K-WATCH |
| GROQ secret values (GNI 4 + Lens 11 key names) | 50%/unknown | Aug 9 keyfile FIRST |

## 5. TRAPS (<=8 lines)
- ONE SELECTION-SHIFTER PER WINDOW: KEY-MAP is live and unobserved. Do NOT land
  RECENCY-DEAD or PROMOTE-NYT until K-WATCH baseline is read. Same logic as
  W-AUTO/KEY-MAP serialization (R-S64 lineage).
- S1 pass DROPS + Top-22 shifts + match-count deflation = the MEDICINE. Census-verified.
  Don't panic-revert (S65 trap, now live).
- PROMOTION PROPOSAL accepts NO replies (advisory-only); numeric replies still hit
  the most-recent PENDING row -- keep numbers out of admin chat.
- Defense News reserve = transport-proven, yield-dead. An activation is not coverage.
- Run #281 executed 24e1bce: c4 unflown until next pipeline run.

## 6. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `b13d748` + S66-close docs commits (verify ls-remote, count don't assume)
TOP3 = K-WATCH (KEY-MAP observation: traces pre/post, match-count ~1.77->1.41 expected), RECENCY-DEAD (L747 fix, strictly AFTER K-WATCH baseline), G-TUNE (~Jul 15: alias whitelist + consultant scrub + new adds)
DEADLINE = G-TUNE ~Jul 15 / OC-A ~Jul 24 / Aug 9 marathon / Groq cliff Aug 16 (quota hit 93/95% both accts today)
TRAP = one selection-shifter per window (KEY-MAP live+unobserved); S1 drop is medicine not damage; promotion proposal takes no replies; c4 unflown until next run
FIRST MOVE = ls-remote verify HEAD; K-WATCH: diff forensic traces 0537-vs-1131 UTC Jul 12; James picks K-WATCH debrief or G-TUNE prep

## 7. POINTERS (<=5 lines)
Matcher + stem convention: ai_engine/matching.py (lookarounds, '*' rules, selftest).
Funnel lists+sites: intelligence_funnel.py ~L23-135 (lists), L226-241 (S1), classifier l3b ~L995.
Sensor: keyword_sensor.py KNOWN_* ~L76-140, L4 swap ~L225, dedup rstrip fix ~L545.
Dashboard truth: page.tsx STATUS_GROUP ~L41-55; MC route.ts HEALTHY_CLASS ~L150; dev-hub L30.
RECENCY-DEAD scene: intelligence_funnel.py ~L747 (art vs article, bare except below).

---
RULES APPENDS for GNI_RULES.md:
R-S66-1: A keyword-level census proves kills; only an article-level comparison
  proves signal preservation. When a ruling ADDS vocabulary, the keyword census
  is structurally blind to the rescue -- verify at the article level.
R-S66-2: Substring bugs can be load-bearing. Before anchoring any matcher,
  census what REAL signal entered through the bug's side door (demonyms via
  country names, 'enforced' via 'forced', IranWire via 'iran') and re-admit it
  deliberately -- silent suppression is worse than the inflation being fixed.
R-S66-3: A proxy in a vocabulary list (brand-as-actor, source-as-signal) is
  allowed only if declared in-code AS a proxy, with the honest cost and the
  proper fix named. Undeclared proxies are future fossils.

DIARY S66 (<=10 lines):
The session both mountains fell. Morning: the proof run confessed on schedule --
columns populated, warnings loud, and the reserve we activated turned out to
fetch perfectly and serve nothing, teaching R-S65-1 a second time unprompted.
Afternoon: three commits painted the dashboard honest and the legend stopped
documenting the bug as a feature. Evening: the census turned a matching fix
into an excavation -- 'sport' had been silently killing chokepoint stories,
'ban' was passing Layer 4 on the word "bank", and a recency bonus died at
birth behind a bare except, undiscovered for its whole life. Every kill got
classified, every rescue got ruled, and the executor held every gate --
including the ones where it caught its own instrument lying. 344 phantoms
down, zero signal lost, and the dashboard finally tells the truth in color. 👊
