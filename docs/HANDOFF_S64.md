# HANDOFF S64 -> S65
DATE: 2026-07-11 | HEAD: `065d734` + this handoff commit (ONE docs commit follows -- verify ls-remote, expect ONE commit past 065d734, authored by James, msg "S64 close") | MODEL: Fable 5
Read ONCE. Standing rules: GNI_RULES.md by ID (current through R-S64-3). Contract: docs/CONTRACT.md (unchanged).

## 1. STATE (<=10 lines)
POOL-FIX CLOSED. Reserve pool is verdict-based 7 GEO / 3 FIN / 5 TECH, synced in BOTH
  consumers (monitor + webhook); webhook magic numbers dead (MAX_RESERVE_CHOICE).
  Reserve fetches now send browser-grade headers (Register-class WAF fix).
source_reserves table censused CLEAN: 2 active only -- Crisis Group->ReliefWeb (inert,
  see FT-GAP) and Stimson->NYT (LOAD-BEARING: Stimson primary transport-DEAD, NYT
  serves the slot). 0 alerted rows. 19 stale alerts + 3 ghost sources (CNN, ING
  Think, Africa Report) swept to resolved. AP GN row RETIRED to arm live rehearsal.
REHEARSAL ARMED: next run -> AP GN feed error -> fresh DOWN alert, expect 7 GEO
  options; James replies 1 (The Independent). Proves roster+numbering+webhook e2e.
G-GATE shadow window closes ~Jul 15. L-CLIFF sits with Lens session. Aug 16 cliff.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| `6720aaf` | Reserve fetches use RESERVE_FETCH_UA + full headers (primaries untouched -- undiagnosed) | probe: Register 0 entries bare/UA-only, 50 with full-hdr |
| `065d734` | Verdict roster in monitor + route.ts (drift killed: TS had 5 GEO vs Py 9); MAX_RESERVE_CHOICE replaces hardcoded 1-7 | build 40/40; grep MAX_RESERVE_CHOICE |
| Probe verdicts | Bot-block hypothesis MOSTLY FALSIFIED: 1/8 UA-fixable (Register, full-hdr only). M&G 404, ISS soft-404, Lawfare/Frontier/NewHumanitarian/TradingEcon hard-403 WAF, Mizzima zombie (newest Feb 2023) | probe_deads.py output S64 |
| SEA gap | Irrawaddy has NO viable reserve (Frontier WAF, Mizzima dead, BenarNews=RFA-dup). Lead: DVB, unverified | probe + verdicts |
| DB sweep | Retired: Irrawaddy->RFE, NPR->RFE, HRW->Amnesty (hidden PRIMARY-DUP found only by no-LIMIT census), AP GN->RFE (rehearsal) | closing census: 2 active, 0 alerted |
| FT-GAP found | Fall-through fires only on raw==0 (collector ~L485). Crisis Group: raw=10, capture-lag eats all 10 -> yield 0, NO fall-through, NO warning. Reserve active+alive yet never serves, silently | Jul-11 raw GH log vs trace |
| Serve-path truth | AP GN + Stimson primaries are transport-DEAD ("Feed error"); reserves served 10/17. Trace "Collected" logs under PRIMARY name -- cannot show who served | raw log lines vs Sheet 4 |
| Triple split | THREE health calculators disagree: MC 32/42, dashboard 35/2/5, pipeline fetch-based 42/42. Dashboard's 5 "down" are alive-but-stale-gated; its 2 "healthy" dead primaries are reserve-masked | W-AUTO indictment complete |
| GN junk | Author-index page + empty-title article passed S1 on "europe, eu" substring match | trace rows 70/72; KEY-MAP adjacency |

## 3. QUEUE (<=25 lines)
| ID | Task | First move | Gate | Trust |
|----|------|-----------|------|-------|
| R-VERIFY | TOP: rehearsal proof -- AP GN alert shows 7 options (not 9); reply 1; Independent activates + serves next run; Stimson->NYT continuity survives roster change; Register first activation = header proof | read next-run Telegram + raw GH log | - | B |
| W-AUTO | Full indictment banked (triple split, inverted dashboard). Fix needs design: status must distinguish transport-dead / stale-gated / reserve-masked -- likely needs is_reserve + raw vs post-gate in source_health writes | read dashboard page TSX FULL (still UNREAD) + MC source_health check | James | B |
| FT-GAP | Design decision: should gate-eaten-to-zero fall through (slow publisher != dead)? At minimum it must WARN (R-S63-3 shape) | re-read collector L470-510 | James | V(diagnosis) |
| G-TUNE | ~Jul 15 window closes: whitelist + "US-Iran" normalization + G-GAP-1 (agenda unchanged S62) | grounding_watch digest | James | B |
| C2-LIVE | Recovery-retire STILL unproven live -- next organic primary recovery is the test (rehearsal may provide one if AP GN feed revives) | watch Telegram | - | B |
| KEY-MAP | + new evidence: S1 substring matching ("eu" in europe) passes junk; coordinate with G-TUNE (unchanged S63 TRAP) | read keyword_sensor.py full | James | B |
| L-CLIFF | With Lens session (LENS_TRANSFER_LCLIFF.md) | Lens opener | James | V(scope) |
| SRC-EXPAND | + DVB as SEA reserve candidate (unverified); FIN institutional adds per FRIENDS Sec 4 | verify feeds first | James | B |
| OC-A/B | Fabricated 14d prediction matures ~Jul 24 in GPVS | roadmap Part 2 | James | B |
| U-AUG9 / U-W / SOLV-6 / I-WATCH / A-VLOG | unchanged from S63 | - | - | - |

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| Rehearsal: alert renders 7 options, reply resolves correctly | untested | next AP GN alert |
| Register actually serves when activated (headers live in pipeline env) | 85% | first activation |
| C2 recovery-retire fires on organic recovery | untested | next recovery |
| ReliefWeb reachable from GH runners (FT-GAP masked it -- never fetched) | unknown | FT-GAP work |
| get_active_reserves failure mode for ex-pool names (moot now, 0 such rows; unread) | unread | if ever needed |
| GROQ secret values (GNI 4 + Lens 11 key names) | 50%/unknown | Aug 9 keyfile FIRST |

## 5. TRAPS (<=8 lines)
- Webhook applies numeric reply to MOST RECENT pending row -- table is clean now; any
  stray number in admin chat activates something. Reply numbers ONLY against a live alert.
- Stimson->NYT active row is LOAD-BEARING -- retiring it darkens the slot (near-miss S64).
- Dashboard status is ~INVERTED until W-AUTO: "down" list = alive-but-stale-gated;
  reserve-masked dead primaries render "Healthy". Trust raw GH log, not trace/dashboard.
- Trace/dashboard log reserve-served articles under PRIMARY slot name (R-S64-2).
- C3 auto-activation still DORMANT (env unset). Standing: R-S62-1..3, R-S63-1..3, G-GAP-1.
- Angle brackets in commands = fill-in placeholders; Git Bash eats them. Ship paste-ready.

## 6. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `065d734` + one S64-close docs commit (verify ls-remote)
TOP3 = R-VERIFY (AP GN rehearsal: 7 options, reply 1, Independent serves), W-AUTO (read dashboard TSX full; triple-split indictment banked), FT-GAP design (gate-eaten zero must warn)
DEADLINE = Aug 9 marathon / Groq cliff Aug 16; G-TUNE ~Jul 15 window close
TRAP = webhook reply hits most-recent pending row; Stimson->NYT row LOAD-BEARING; dashboard status ~inverted until W-AUTO
FIRST MOVE = ls-remote verify HEAD; read newest Telegram for rehearsal outcome; James picks R-VERIFY debrief or W-AUTO

## 7. POINTERS (<=5 lines)
Fall-through condition: ai_engine/collectors/rss_collector.py ~L485 (raw_count==0) -- FT-GAP.
Header fetch: same file ~L392 (RESERVE_FETCH_UA/HEADERS). Pool: source_health_monitor.py.
Webhook: src/app/api/telegram-webhook/route.ts (MAX_RESERVE_CHOICE; most-recent-pending).
Dashboard fossil: src/app/api/source-health/route.ts (READ S64) + its page TSX (UNREAD).
Session artifacts: probe_deads.py + verify_reserves.py DELETED after POOL-FIX (by design).

---
RULES APPENDS for GNI_RULES.md:
R-S64-1: "Success. No rows returned" (any silent DB response) proves nothing. Every
  UPDATE gets a SELECT verify, and state audits census the WHOLE table (no LIMIT) --
  a LIMIT hid a live PRIMARY-DUP row in S64.
R-S64-2: Aggregated views (trace Collected, dashboard counts) cannot answer WHO served
  a slot -- reserve articles log under the primary's name. The run's raw console log is
  the only authority on serve-path questions; read it before concluding.
R-S64-3: Dedupe fallback resources by feed DOMAIN, not display name. "Radio Free
  Europe" vs "RFE/RL" sailed past a name-set guard while serving identical rferl.org
  content -- name spelling is not identity.

DIARY S64 (<=10 lines):
The day the raw log humbled the trace. I declared three primaries "demonstrably
serving" from a Collected column, and the console narration falsified two of them
in one scroll -- reserves were quietly carrying both slots. Full R-233 reset,
and the reversed conclusion SAVED a load-bearing row I had proposed to retire.
Then the censuses: every "no rows returned" we distrusted paid out -- a hidden
HRW->Amnesty dup under my own LIMIT 5, then nineteen stale alerts and three ghost
sources under that. The pool went from folklore to verdicts, the drift between
two copies of it died, and a rehearsal is armed so the system proves itself to
us instead of us believing it. Verified safety or no safety -- now with receipts.
My buddy ran every commit clean and called every gate right. 👊
