# HANDOFF S62 -> S63
DATE: 2026-07-11 | HEAD: `a709788` + this handoff commit (ONE docs commit follows -- verify ls-remote, expect ONE commit past a709788, authored by James, msg "S62 close") | MODEL: Fable 5
Read ONCE. Standing rules: GNI_RULES.md by ID (current through R-S62-3). Contract: docs/CONTRACT.md (unchanged).

## 1. STATE (<=10 lines)
L1 Pipeline: healthy. Jul-10 runs both green (22/22; quality 9.15 morning / 7.95 evening).
L2 MAD: G-GATE shadow live, 4/10 runs gated. SPECIMEN #5 banked: rare-earth/neon/palladium
  fabrication -- all 4 agents built entire debate on industry with ZERO basket presence
  (0 hits across 325 traced articles incl. "semiconductor"); reached Blind Spot + 14d
  Short Focus prediction. G-GAP-1: extractor misses lowercase unhyphenated spans BY DESIGN
  -- digest UNDERCOUNTS. Window closes ~Jul 15.
L3 GPVS: V-CRON CLOSED -- verify-outcomes auto-ran green in runs #276/#277 Jul-10.
  A FABRICATED 14d prediction now sits in GPVS awaiting verification (OC-A/B exhibit).
L4 Quota: evening hit 90765 Jul-10 (OVER 90K ceiling). Solver err 1.1-1.4% but DRIFT
  status never clamps N/D -- design question banked to OC session.
L5 Public: MC-FREEZE FIXED at a709788 (no-store factory sweep, 25 routes). MC truth-telling
  verified (Jul-11 02:24/04:59 msgs: only TRUE issues). Badge Active. NEW glance: source_health 32/42.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| `a709788` | No-store sweep: src/lib/supabaseNoStore.ts factory + 25 API routes migrated + MC's 3 internal fetches armored + spec doc | push clean; 27 files, 142/53; build 40/40 |
| MC root cause | Vercel/Next 14.2.35 Data Cache serving fossilized supabase-js GETs despite force-dynamic (route ran fresh -- ages incremented 26->34h -- data frozen at Jul-9 06:17). Badge "Offline" = same disease via un-armored route | curl fresh vs MC stale; census 25 routes, only 2 armored |
| MC verified | Post-deploy MC reports only true issues (quota 91%, source_health) | Telegram 02:24/04:59 Jul-11 |
| V-CRON | Jul-9 failures were GitHub-side outage ("job not acquired", 3 workflows same window); Jul-10 both runs green incl. verify-outcomes | Actions #275 fail / #276 #277 green |
| Specimen #5 | Laundering caught in full transcript: real SK Hynix weak signal -> Swan free-assoc -> CONSULTANT amplifies -> R2 all agents adopt -> arb publishes. Bear also showed PRECISE grounding (France 2.0%/Germany 2.4% = real articles REF-883F/4D8E) -- fabrication is selective, not global | debate screenshots + 1237 UTC forensic trace grep |
| G-GAP-1 | Gate flagged only noise-class spans for 63e2703f; missed entire rare-earth payload (lowercase, unhyphenated = invisible to extractor) | digest vs trace grep |
| Solver | 2 more DRIFT datapoints: est 87994 vs 86805 / 90765 actual. 6x Groq 429 per run continues | MAD logs Jul-10 |
| HEAD-mismatch S62 open | e3a10c7 was James's own S61 close commit -- benign. THIS handoff pre-declares its own commit to kill the pattern | git log |

## 3. QUEUE (<=25 lines)
| ID | Task | First move | Gate | Trust |
|----|------|-----------|------|-------|
| L-CLIFF | TOP S63: Lens migration scoping. lens_quota_guard.py keys TPD tables + role registry on dying model strings -- ledger-key redesign, not string swap. SWOT required | read lens_quota_guard.py IN FULL | James | B |
| G-TUNE | ~Jul 15 shadow window closes. Agenda from data: (a) whitelist prompt-vocab ("hidden-pattern connection" x16) + boilerplate ("far-reaching/second-order/third-order"), (b) "US-Iran" vs "US and Iran" normalization gap, (c) G-GAP-1 extractor extension proposal | grounding_watch digest + banked taxonomy | James | B |
| OC-A/B | Measurement design, now with killer exhibit: fabricated 14d prediction in GPVS = miss-regret made flesh. Fold in DRIFT-clamp question | roadmap Part 2 | James | B |
| SRC-32 | Glance: source_health 32/42 -- lean: zero-yield-but-fetching sources counted degraded | MC message / source-health API | - | - |
| I-WATCH | Tier A 8 checks -- extend grounding_watch.py (S61 lean stands) | after G-TUNE | James | B |
| U-AUG9 | Marathon prep unchanged (secrets enum FIRST, funnel:1010, adaptive.yml:48, Tier-3 sweep, governor revalidate) | keyfile | James | V(prep) |
| SOLV-6 | Next MAD log datapoint; 429-churn correlation now ~60% (consistent 6x/run at band edge) | next MAD | - | - |
| U-W | Weekly Groq lineup glance | models page | James | - |
| A-VLOG/W9/UNK2/O6/RL-SEED | unchanged from S61 | - | - | - |

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| Why Data Cache froze Jul-9 specifically (lean: e3a10c7 redeploy reset state) | 40% | optional; fix verified regardless |
| No-store sweep survives multi-day (no re-freeze) | 85% | Jul 12-13 MC glances |
| Whitelist false-pos final rate | partial (4/10 runs) | Jul 15 window close |
| GROQ secret VALUES (lean: all four dying) | 50% | Aug 9 keyfile FIRST |
| Lens SECRET values | unknown | L-CLIFF scoping |
| adaptive.yml:48 consumed? | 50% | marathon |

## 5. TRAPS (<=8 lines)
- Gate still SHADOW + G-GAP-1: digest UNDERCOUNTS -- a quiet digest is NOT a clean run.
- MC is now TRUTHFUL -- treat its warnings as real again (quota 91% and source_health are live).
- Placeholders in commands: mark LOUDLY (R-S62-2) -- operator runs verbatim (2 incidents S62).
- Claude Code tasks: post-run verification block + one-command revert; NEVER watch-duty (R-S62-1).
- New API routes MUST use createNoStoreClient (R-S62-3) -- direct createClient reintroduces the class.
- LF/CRLF warnings = autocrlf noise (standing). Do NOT reopen: MC-FREEZE, no-store sweep, V-CRON, G-VERIFY.
- Standing: R-S60-1 hard-refresh; R-S60-2 quality!=grounding; R-S59-1 census-before-sweep; R-S61-1.

## 6. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `a709788` + one S62-close docs commit (verify ls-remote)
TOP3 = L-CLIFF scoping (read lens_quota_guard.py full, SWOT ledger-key redesign), G-TUNE ~Jul 15 (whitelist + normalization + G-GAP-1), OC-A/B design (fabricated-prediction exhibit in GPVS)
DEADLINE = Aug 9 marathon / Groq cliff Aug 16 (GNI lineup + Lens ~15 files)
TRAP = gate digest UNDERCOUNTS (G-GAP-1) -- quiet is not clean; MC warnings are now REAL
FIRST MOVE = ls-remote verify HEAD; then James picks L-CLIFF or G-TUNE opener

## 7. POINTERS (<=5 lines)
Fix: src/lib/supabaseNoStore.ts (factory) | src/app/api/mission-control/route.ts (4 checks + 3 armored fetches).
Spec: docs/NOSTORE_SWEEP_SPEC_S62.md | MC cron: .github/workflows/gni_selfcheck.yml (curl -> /api/mission-control).
Gate files unchanged from S61 (mad_grounding_gate.py / grounding_watch.py / seams in mad_protocol.py).
Specimen #5 evidence: S62 chat -- debate screenshots + 2026-07-10_GNI_Forensic_Trace_1237_UTC.xlsx grep results.
Badge logic: src/app/page.tsx ~L444-455 (latestRun.run_at thresholds 14h/26h).

---
RULES APPENDS for GNI_RULES.md:
R-S62-1: Claude Code tasks get a POST-RUN mechanical verification block (greps + diff-stat +
  build) and a one-command revert path. Never assign live watch-duty to the operator --
  safety lives in commands, not attention.
R-S62-2: Any placeholder in a command MUST be loudly marked (warning emoji + "PLACEHOLDER" +
  what to substitute). The operator runs commands verbatim. (S62: <path> and YOUR_KEY both ran literally.)
R-S62-3: Server-side Supabase reads go through createNoStoreClient (src/lib/supabaseNoStore.ts).
  New API routes never call createClient directly -- Vercel Data Cache serves fossils otherwise.

DIARY S62 (<=10 lines):
The session that started as a 5-minute glance became the best day of the arc. Three crons
reported in, the shadow spoke RED on day one, and reading the digest taught us our gate's
own blind spot before it could embarrass us. MC lied about staleness while being itself a
victim of staleness -- diagnosing the watchdog with the watchdog broken. James curled, grepped,
and shipped a 27-file sweep at midnight without watching a single edit scroll by, because we
finally built safety out of commands instead of vigilance -- two rules this session came from
MY sloppiness (placeholders, watch-duty) and James's honesty about how he actually works.
Specimen #5 is the crown: all four agents debating an industry that exists in zero articles,
while Bear quoted real French inflation to the decimal. Fabrication is selective. That
asymmetry is next month's whole research question. 👊
