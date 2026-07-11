# HANDOFF S65 -> S66
DATE: 2026-07-11 | HEAD: `e2f92ad` + ONE docs commit (this file, authored James, msg "S65 close" -- verify ls-remote; S64 predicted one and shipped two, count don't assume) | MODEL: Fable 5
Read ONCE. Standing rules: GNI_RULES.md by ID (current through R-S65-3). Contract: docs/CONTRACT.md (unchanged).

## 1. STATE (<=10 lines)
W-AUTO 3 of 4 SHIPPED: schema (fetch_ok bool + served_by text on source_health),
  writer persists both + WARNs on gate-eaten slots (raw>0,yield=0), route derives
  5-state (reserve-masked > transport-down > silent > stale-gated > degraded/healthy;
  NULL columns = legacy 3-state fallback for ~10 runs). Commit 4 (consumers) PENDING proof.
REHEARSAL 4/5 PROVEN: alert rendered exactly 7 GEO options; James replied 5 (not 1) ->
  Defense News activated correctly; Stimson->NYT survived roster change; NYT promotion
  proposal fired (C4 live). C2 recovery-retire fired ORGANICALLY (Crisis Group) -- but on
  fetch-based recovery with yield=0: C2's criterion inherits FT-GAP blindness (R-S65-1).
Remaining proof: next run must show Defense News serving + STALE-GATED warns + populated columns.
MAD fabrication CONFIRMED LIVE at arb level: today's 8f967654 is an ARB HIT (invented
  Goldman Sachs + FT attributions, Bear R2/R3). G-TUNE agenda frozen. L-CLIFF with Lens. Aug 16 cliff.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| `e19fba7` | W-AUTO-2: writer persists fetch_ok+served_by, raw_val_guard WARN (FT-GAP write-time) | grep L257/283-291/304-305; SQL census 2 cols |
| `7293060` | W-AUTO-3: route 5-state, priority order reserve-masked first, legacy NULL fallback verbatim | diff reviewed; build 40/40 |
| `e2f92ad` | W-AUTO-3b: degraded check restored INSIDE fetchOk===true only, below stale-gated | 1-line diff; build 40/40 |
| Route indictment | Old status = article_count alone; page innocent (renders verbatim); legend documented bug as feature ("0 articles = down") | route.ts read + page.tsx read |
| Serve-path in code | counts key off art["source"] = primary name; funnel logged Stimson:1 while NYT served -- RESERVE-MASKED invisible pre-fix | save_source_counts read + trace |
| KEY-MAP convicted | 'if kw in text' at ~14 funnel sites + sensor Layer 4; 'eu' in 'europe' double-counts -> inflates stage1_match_count/S38 bonus; list has DELIBERATE stems (extremis/geopolit/sanction/strait) -- blind \b breaks them | L49-80 + L195-215 + sensor full read |
| L984 bug | _classify_content_type L3b: ("by "+title[:3]) in title -- precedence bug, dead on real bylines; intent = startswith("by ") (S64 GN author-page class) | L936-1000 read |
| G-TUNE triage | Class A extractor-miss (us-iran x19, fed-alias) vs Class B consultant dialect (hidden-pattern x25, silo-gap) -- 2 levers: alias whitelist + consultant prompt scrub, THEN enforce | digest + transcript |
| Fossils banked | F-TILES (health page infra tiles hardcoded green), F-CASE (source_weights case-dup rows split learning), F-KEY (NEXT_PUBLIC_GNI_API_KEY ships in client bundle) | health page read + screenshots |
| MAD side-data | Metered 94591 vs solver est 84995 (~11% under); 7x 429s one run -> SOLV-6 point. Quota 82% warns | mad_runner log |
| MC Check 4 read | Counts literal 'healthy' vs 50%/80%; post-fix must count healthy+stale-gated+silent as healthy-class | L140-170 read |

## 3. QUEUE (<=25 lines)
| ID | Task | First move | Gate | Trust |
|----|------|-----------|------|-------|
| R-VERIFY-2 | TOP: proof run -- GH log: Defense News [RESERVE for AP GN] serves + WARNING [STALE-GATED] lines; SQL: fetch_ok/served_by populated; deployed /source-health renders honest states | read newest GH run log | - | B |
| W-AUTO-4 | After proof: page STATUS_CONFIG +4 states (reserve-masked blue/transport-down red/silent orange/stale-gated yellow); tiles -> healthy / attention(silent+stale-gated+degraded) / down(transport-down+reserve-masked+down); legend rewrite (kill "0=down"); dev-hub L26 check; MC Check4 filter healthy-class = healthy+stale-gated+silent, thresholds unchanged | Claude Code brief (spec above is complete) | James | V(spec) |
| KEY-MAP | 4 commits: (1) ai_engine/matching.py kw_match, '*' suffix = stem \bstem\w*, else \bkw\b, lru_cache, selftest; (2) funnel sweep ~14 sites incl IRRELEVANT_KEYWORDS (read that list first), annotate ONLY 4 self-evident stems; (3) sensor Layer 4 same helper; (4) L984 -> title_lower.startswith("by "). CENSUS GATES MERGE: old-vs-new matcher diff on one day's articles, every kill must be phantom | AFTER W-AUTO-4 lands, never interleaved | James | V(design) |
| G-TUNE | ~Jul 15: (1) alias whitelist (fed<->federal reserve; US-Iran variants; share/import sensor KNOWN_ACTORS -- anti-L-CLIFF) + G-GAP-1 normalization; (2) consultant prompt scrub of Class-B dialect; (3) re-measure shadow, THEN enforce | grounding_watch digest | James | B |
| FT-GAP | Design widened: fall-through AND C2 recovery criterion must consult yield/serve-path (Crisis Group false-recovery proof). WARN already live | collector L470-510 + reserve_lifecycle read | James | V(diagnosis) |
| F-TILES / F-CASE / F-KEY | Fossil sweep candidates: hardcoded infra tiles; weight-row case dedupe census; NEXT_PUBLIC key is not auth | James picks | James | B |
| L-CLIFF | With Lens session (LENS_TRANSFER_LCLIFF.md) | Lens opener | James | V(scope) |
| SRC-EXPAND | DVB SEA reserve candidate unverified; FIN adds per FRIENDS Sec 4 | verify feeds | James | B |
| OC-A/B | Fabricated 14d prediction matures ~Jul 24 GPVS | roadmap Pt 2 | James | B |
| L4-COUNT | _GNI_L4_CALLS env counter: is it ever incremented? (classifier L990+, unread tail) | read L990-1035 | - | unread |
| U-AUG9 / U-W / SOLV-6 / I-WATCH / A-VLOG | unchanged S63 (+SOLV-6 got the 94591 data point) | - | - | - |

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| Defense News serves + headers hold when activated live | 85% | proof run |
| Writer's served_by populates correctly (code verified, never executed) | 90% | proof run SQL |
| avg mixes gate-eaten runs -> degraded flag quieter post-recovery (accepted, self-healing) | V | watch only |
| IRRELEVANT_KEYWORDS contents (substring false-kill risk unknown) | unread | KEY-MAP c2 |
| L4 LLM counter increment | unread | L4-COUNT |
| GROQ secret values (GNI 4 + Lens 11 key names) | 50%/unknown | Aug 9 keyfile FIRST |

## 5. TRAPS (<=8 lines)
- Webhook numeric reply hits MOST RECENT pending row; Defense News row now ACTIVE --
  stray numbers in admin chat still dangerous. Stimson->NYT row remains LOAD-BEARING.
- Dashboard stays ~inverted until W-AUTO-4 AND legacy-NULL window (~10 runs) drains;
  raw GH log remains sole serve-path authority (R-S64-2).
- W-AUTO-4 and KEY-MAP are STRICTLY SERIAL -- KEY-MAP shifts selection; two-cause anomalies otherwise.
- KEY-MAP will DROP S1 pass counts + shift Top-22 day one. Expected, census-verified, don't panic-revert.
- Executor diffs get chat clearance BEFORE the git trigger (R-S65-2 -- slipped once this session, benign).
- W-AUTO-4 brief lives ONLY in S65 chat + this queue's compressed spec -- queue line is authoritative.

## 6. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `e2f92ad` + one S65-close docs commit (verify ls-remote, count don't assume)
TOP3 = R-VERIFY-2 (proof run: Defense News serves, STALE-GATED warns, columns populated), W-AUTO-4 (fire Claude Code brief from queue spec after proof), KEY-MAP (4 commits, census-gated, strictly after W-AUTO-4)
DEADLINE = G-TUNE ~Jul 15 window / Aug 9 marathon / Groq cliff Aug 16
TRAP = webhook hits most-recent pending; dashboard inverted until W-AUTO-4 + NULL window; W-AUTO-4 and KEY-MAP never interleave
FIRST MOVE = ls-remote verify HEAD; read newest GH pipeline log for proof-run evidence; James picks R-VERIFY-2 debrief or W-AUTO-4 fire

## 7. POINTERS (<=5 lines)
5-state derivation: src/app/api/source-health/route.ts ~L66-85 (priority order sacred).
Writer + WARN: ai_engine/analysis/source_health_monitor.py L257 (raw_val_guard), L283-305.
KEY-MAP targets: funnel L195-215 (S1), L49-80 (list+stems), L936-1000 (classifier L984 bug).
Sensor Layer 4 substring bug: ai_engine/analysis/keyword_sensor.py _extract_event_signature.
MC Check 4: src/app/api/mission-control/route.ts L145-164 (healthy-class filter target).

---
RULES APPENDS for GNI_RULES.md:
R-S65-1: Fetch-based "recovery" is not recovery. Any auto-retire/auto-activate criterion
  must consult yield or serve-path, not transport alone -- C2 retired a reserve for a
  primary that fetched fine and served zero.
R-S65-2: Executor (Claude Code) diffs get chat clearance BEFORE the git trigger, every
  time, however clean they look. Review-then-trigger is the contract's protection for
  the day the diff isn't clean.
R-S65-3: Never blind-wrap keyword lists in word boundaries. Lists contain deliberate
  stems (extremis, geopolit); use an explicit stem convention ('*' suffix) and annotate
  conservatively -- a too-greedy stem is the substring bug wearing a different hat.

DIARY S65 (<=10 lines):
The session the system started confessing. The rehearsal proved four of five claims
and the fifth deviation (reply 5, not 1) proved MORE -- numbering works anywhere.
C2 fired on its own and immediately showed us its blind spot: it retired a reserve
for a primary that fetches perfectly and serves nothing. Then we read four files
and found the same lie at every layer -- a route inventing status from yield, a
legend documenting the bug as a feature, a classifier line dead on its own target
class, and 'eu' hiding inside 'europe' at fourteen scoring sites. Three commits
later the DB tells transport truth and the route repeats it honestly. Claude Code
executed two clean briefs; my buddy ran every gate, caught my placeholder, and
pulled one trigger early -- we made it a rule instead of a wound. 👊
