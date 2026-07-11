# HANDOFF S63 -> S64
DATE: 2026-07-11 | HEAD: `d0b2b45` + this handoff commit (ONE docs commit follows -- verify ls-remote, expect ONE commit past d0b2b45, authored by James, msg "S63 close") | MODEL: Fable 5
Read ONCE. Standing rules: GNI_RULES.md by ID (current through R-S63-3). Contract: docs/CONTRACT.md (unchanged).

## 1. STATE (<=10 lines)
L1 Pipeline: healthy (Jul-10 both green). G-GATE shadow window closes ~Jul 15 (G-TUNE).
Reserve system: WHOLE LIFECYCLE REBUILT S63 -- fall-through fix (220f477) + C1-C5
  (d0b2b45): escalation, recovery-retire, flag-gated auto-activation (DORMANT,
  env GNI_AUTO_RESERVE_AFTER_HOURS unset), promotion proposals, option annotations.
  LIVE BEHAVIOR UNVERIFIED -- first proof due in Jul-11/12 run Telegram.
Reserve pool verdicts (verify_reserves.py, Jul-11): ALIVE 10/13 current (WaPo ALIVE --
  banked "dead" claim was WRONG); DEAD: Mail&Guardian, Stimson[PRIMARY-DUP];
  STALE: WSJ (529d). Candidates ALIVE: Diplomat, Defense News, MIT TR, TechCrunch,
  MarketWatch, Investing.com. 4 DEADs share "2:1326 invalid token" = bot-block lean.
L-CLIFF: SCOPED (Lens repo is public -- fetched+read in full). Decision moved to Lens session.
MC truthful; source-health dashboard still renders FOSSIL yield-logic (leg of W-AUTO).

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| `f0fc657` | S62 rules append landed (GNI_RULES.md at ROOT, not docs/) | grep -c R-S62 = 3 |
| `220f477` | Reserve fall-through: valid-but-EMPTY primary (Google News wrapper class) now falls to activated reserve; old break fired on TRANSPORT success | RFE epiqq verified alive Jul-11 while Irrawaddy slot sat 0/0 post-activation; Stimson/NYT contrast |
| `d0b2b45` | C1-C5 lifecycle, 213 ins: mute-button hole killed (reserve-active previously silenced slot FOREVER), recovery bookkeeping, gated auto-activate, proposal-only promotion, webhook-safe annotations | selftest held 5/8; compile OK; 2 files exactly |
| L-CLIFF scoped | 19 files (not 15); root cause reframed: DUAL SOURCE OF TRUTH (guard keys private model-string copies; live drift specimen: call-site "qwen/qwen3-32b" vs guard "qwen3-32b"); design: lens_models.py role registry; NO SQL migration needed | full 778-line read + repo tarball grep; LENS_TRANSFER_LCLIFF.md delivered |
| SRC-32 closed as bug-class | Dashboard 32/42 was 3 diseases: dead feeds + quiet-but-alive (dashboard fossil) + reserve-never-served (220f477) | Telegram Jul 6/8/9 alerts + dashboard |
| Friends' 4 docs analyzed | Headline: Specimen #5 domain (rare-earth/semis) = exact basket gap (zero commodity/semi/energy sources) -- source expansion IS grounding-quality fix; FIN pillar acute (5 aggregators, no institutional) | FRIENDS_SOURCES_ANALYSIS_S63.md |
| Doc-#4 integrity | crisisbrief.org / geopoliticsmonitor.org = fabrication signatures (near-name trick vs real geopoliticalmonitor.com) | never adopt unverified |

## 3. QUEUE (<=25 lines)
| ID | Task | First move | Gate | Trust |
|----|------|-----------|------|-------|
| POOL-FIX | TOP: commit new reserve pool from verdicts -- drop Mail&Guardian/WSJ, fix Stimson+GlobalVoices PRIMARY-DUPs, add 6 ALIVE candidates (pillar-balanced: FIN needs depth); probe 2:1326 DEADs with UA header first | retry 4 DEADs with requests+UA before dropping | James | V(verdicts) |
| W-AUTO | Site-wide auto-update census (James ask): every page/subpage -- fossil logic (dashboard yield-legend = leg 1), non-noStore routes (R-S62-3 class), stale client fetches | read source-health page+route TS IN FULL | James | B |
| C-VERIFY | Confirm lifecycle live: Jul-11/12 Telegram -- expect Irrawaddy slot serving RFE articles (fall-through proof); no false recoveries/escalations | next run Telegram + dashboard | - | B |
| G-TUNE | ~Jul 15 window closes: whitelist + "US-Iran" normalization + G-GAP-1 (agenda unchanged S62) | grounding_watch digest | James | B |
| KEY-MAP | keyword_sensor.py read -> map friends' keyword clusters (critical-minerals #1); TRAP: "hidden-pattern connection" watchwords ARE gate-flagged MAD prompt vocab -- coordinate with G-TUNE | read keyword_sensor.py full | James | B |
| L-CLIFF | Scoped; James drops LENS_TRANSFER_LCLIFF.md into Lens repo; A/B/C decided in Lens session | Lens session opener | James | V(scope) |
| SRC-EXPAND | Primary-roster adds post-cliff (FIN 1-2 pre-cliff allowed: IMF/EIA/Fed class); per FRIENDS analysis Sec 4 | verify candidate feeds | James | B |
| OC-A/B | Fabricated 14d prediction matures ~Jul 24 in GPVS | roadmap Part 2 | James | B |
| U-AUG9 / U-W / SOLV-6 / I-WATCH / A-VLOG etc. | unchanged from S62 | - | - | - |

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| 2:1326 DEAD signature = bot-block (UA-fixable), not dead feeds | 60% lean | POOL-FIX probe |
| C1-C5 live behavior (esp. no false recovery-retire on reserve-served slots) | untested | Jul-11/12 runs |
| Fall-through serves RFE for Irrawaddy slot | 85% | next run dashboard |
| No-store sweep multi-day survival (from S62) | 85% | Jul 12-13 MC glances |
| Whitelist false-pos final rate | partial | Jul 15 window close |
| GROQ secret values (GNI 4 + Lens 11 key names) | 50%/unknown | Aug 9 keyfile FIRST |

## 5. TRAPS (<=8 lines)
- C3 auto-activation is DORMANT (env unset) -- do not assume reserves self-activate.
- Webhook reply-number maps to option POSITION -- never filter alert lists (R-S63-1).
- verify_reserves.py sits UNTRACKED in repo root -- James deletes after POOL-FIX; never commit.
- Session artifacts (LENS_TRANSFER / FRIENDS_ANALYSIS .md) live in chat downloads, not repo.
- Promotion messages are PROPOSALS -- system never edits roster; James's gate.
- Standing: gate digest UNDERCOUNTS (G-GAP-1); MC warnings REAL; R-S62-1..3; R-S60-1/2; R-S59-1.

## 6. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `d0b2b45` + one S63-close docs commit (verify ls-remote)
TOP3 = POOL-FIX (UA-probe 4 DEADs, then commit verdict pool), W-AUTO census (dashboard fossil leg 1, read TS full), G-TUNE ~Jul 15
DEADLINE = Aug 9 marathon / Groq cliff Aug 16; L-CLIFF scoped -> Lens session decides A/B/C
TRAP = C3 dormant (env unset); webhook numbering load-bearing (R-S63-1); C1-C5 live behavior UNVERIFIED until Jul-11/12 runs
FIRST MOVE = ls-remote verify HEAD; read Jul-11/12 Telegram for lifecycle proof; James picks POOL-FIX or W-AUTO

## 7. POINTERS (<=5 lines)
Lifecycle: ai_engine/analysis/source_health_monitor.py (C1-C4 helpers before selftest) |
  ai_engine/collectors/rss_collector.py (fall-through ~L487; stats carry is_reserve).
Verdicts: verify_reserves.py output banked in Sec 1 (script itself: delete after POOL-FIX).
L-CLIFF: LENS_TRANSFER_LCLIFF.md (chat download -> Lens repo). Friends: FRIENDS_SOURCES_ANALYSIS_S63.md.
Dashboard fossil: src/app/api/source-health/route.ts + its page (UNREAD -- read full before W-AUTO patch).

---
RULES APPENDS for GNI_RULES.md:
R-S63-1: Any option list whose reply-number maps to list POSITION in a consumer (Telegram
  webhook class) must preserve numbering across changes -- annotate bad options, never
  filter, until every consumer is read and updated in the same commit.
R-S63-2: Fallback resources (reserves, backups, secondaries) are guilty-until-verified:
  live-check + dedupe-against-primaries before they may be offered as safety. A dead
  reserve is worse than none -- it converts an outage into a silent one.
R-S63-3: No protection may permanently mute its own alert path. Any "already handled ->
  skip alert" state needs an escalation branch for re-failure (S63: reserve-active
  silenced a slot forever while the reserve itself was never serving).

DIARY S63 (<=10 lines):
Housekeeping first: S62's missing rules append turned out to be a path mystery
(GNI_RULES.md lives at root), solved by census not memory. Then the day's real gift --
Lens is PUBLIC, so I read all 778 lines myself and L-CLIFF deflated from monster to
two-session registry design; the qwen-prefix drift specimen was sitting there proving
the root cause. The reserve arc was Three Philosophies engineering: James's own Jul-9
activation not working led us to break-on-transport-success, then to the mute-button
hole, then to a pool offering dead feeds and self-replacements as safety. Three rules,
all the same shape: verified safety or no safety. And the bytes humbled me twice --
WaPo alive, migration landed. My buddy ran a marathon session and every commit stuck
the landing. Specimen #5's basket-gap insight now has a source-expansion answer. 👊
