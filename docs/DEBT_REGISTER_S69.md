# GNI DEBT REGISTER — S69 archaeology (2026-07-15)
Method: conversation_search across all GNI records for fallback pivots, "temporary fix",
"deferred", "TBD", "not yet built", parked rulings. Every row = LEAD (handoff discipline:
BEV before action). Classes: OPEN / VERIFY (likely paid, 1-grep confirms) / HEALTHY
(deferred WITH record — the good pattern) / FROZEN / RESOLVED.

## CLASS 1 — DET-DEAD-class candidates (vanished without record)
| ID | Debt | Born | Evidence | Status |
|----|------|------|----------|--------|
| D-1 | Detector never wired to funnel; wiring abandoned mid-session, marked DONE | Mar 21 (Day 11) | tonight's grep: zero imports | CONFIRMED OPEN (→ DET-DEAD queue item) |
| D-2 | **"7-layer defense" copy vs code**: S52 shipped Layer 1 (NFKC) only; S53 record says "Layers 2-7 designed-on-disk, NOT built" — yet /methodology + /about/devops describe all 7 as OPERATING (prompt-boundary detection, hardened-JSON guardian, language normalization...) | S52-S53 | S53 session record vs live page copy | STRONG CANDIDATE — same disease as D-1: designs described as live. Some listed layers may exist under older names (SHA-256 chain ✓, source-credibility ✓) — needs bytes census |
| D-3 | Stand-by stock architecture (fetch_prices.py + stock_prices table + gni_market.yml) — planned Apr 8; a 15-min Vercel cache shipped as "temporary protection" | Apr 8 (S24) | /stocks works today via Yahoo direct — the temporary cache may be the living implementation | VERIFY |
| D-4 | TECH pillar fix: nexus_analyzer JSON regex fallback loses `weakness_identified` | Apr 8 (S24) | never seen again in records | VERIFY |
| D-5 | Fox News source_weights DB cleanup (`DELETE FROM source_weights WHERE source='Fox News'`) | Apr 8 (S24) | never seen again | VERIFY (minor) |
| D-6 | Stats arc: S53 paused on James's `gni_stats` injection_patterns column ruling — ruling never recorded | S53 (Jun 29) | /about sprint tiles render live today incl. "81 Injection patterns" — did the arc finish, and from WHICH array does it read? Directly feeds F1/option-C | VERIFY (high value) |
| D-7 | Solver Commit-2: FLOOR_HIT status surfaced to mad_runner (print-only "load-bearing soon") | S51-S52 | today's MAD log prints solver line — may be paid | VERIFY (minor) |

## CLASS 2 — VERIFY (likely paid; one grep each)
| ID | Debt | Born | Likely resolution |
|----|------|------|-------------------|
| V-1 | auth.ts `origin === ''` bypass — explicitly "temporary fix" pre-IEEE | Mar 29 | R-S54-4 (curl always 401s) implies permanent fix landed + O-SEC S60 audit; confirm bypass removed |
| V-2 | phi_compatibility_check.md S37 items: GPVS human-security track, L4 LLM spot-check, About PHI-003 copy, banner | May-Jun | L4 exists (c4/KEY-MAP ✓), /about shows FFF identity ✓ — check file's Open Items current state |
| V-3 | C4 MAD sleep values (20s→45s round, 30s→60s pre-arb) | Apr 8 | today's log shows 90s pre-arb — likely paid+exceeded |

## CLASS 3 — HEALTHY DEBT (deferred WITH record — the pattern that works)
- W-10 TPM contamination from manual runs — deferred BY JAMES, documented (Apr 12)
- SEC-1 shared Supabase split — deferred BY JAMES as future milestone (Apr 12)
- Semantic self-audit Layer 2 (self-bias gate) — OPEN row in phi_compatibility_check.md with owner + origin story; gni_selfbias exists (structural layer live S40)
- /api/webhooks — publicly labeled "SOON" on dev-hub (declared-future, honest)
- A-VLOG hydration era (single-source-of-truth for UI numbers) — banked S59, stalled but recorded
- GT-5 enforce decision, FT-GAP-B/C, GT-3, CLIFF-CODE — all queue rows ✓
*Why these are healthy: each has an instrument holding it (rules file, compat file, queue, public label). D-1's lesson: debt without an instrument decays into "fact".*

## CLASS 4 — FROZEN / RESOLVED
- Myanmar event-driven trigger ("freshness check = temporary workaround, mechanism TBD") — mooted by GNI_Myanmar freeze at 9d6a5e5
- Supabase RLS (Apr 8 item) — RESOLVED S60 (37 tables, O-SEC)
- Quota portioning policy (GNI-R-219) — RESOLVED via quota guard + sacred + solver arcs
- Mission Control red — RESOLVED S54 (benign threshold)
- W-15 recency bonus — the poetry of the register: BORN Apr 12 (W-15 fix), DIED S38 (art→article NameError), REVIVED S68 (`9991c4a`), first breath TODAY. A debt that was paid, silently died, and got paid again 3 months later.

## VERIFY BATCH (read-only, one paste)
```bash
printf '\e[?2004l'
cd /c/HDCS_Project/03/GNI_Autonomous
# V-1 auth bypass
grep -n "origin" src/lib/auth.ts
# D-2 seven layers: what actually exists in the funnel package
ls ai_engine/funnel/
grep -rn "prompt.boundary\|prompt_boundary\|hardened.json\|language.normal" ai_engine/ --include="*.py" -il
# D-6 stats hydration: which array feeds the /about tile
grep -n "injection\|pattern" src/app/api/about-stats/route.ts
# D-3 market workflow
ls .github/workflows/
# D-4 TECH pillar fallback
grep -n "weakness_identified" ai_engine/analysis/nexus_analyzer.py | head -5
# D-7 solver commit-2
grep -n "FLOOR_HIT\|solver" ai_engine/mad_runner.py | head -5
```

## CLASS 5 — "DEFERRED BY JAMES" RULING LEDGER (explicit deferrals, audited)
| ID | Ruling | Born | Terms | Status TODAY (Jul 15) |
|----|--------|------|-------|----------------------|
| J-1 | W-10 TPM contamination from manual runs — "test for couple months first" | Apr 12 | ~2 months → mid-June | **OVERDUE FOR RE-RULING** — window elapsed Jun 12; keep the manual-MAD-trigger caution or lift it? |
| J-2 | SEC-1 shared Supabase — "future HD milestone" | Apr 12 | open | ✅ CLOSED PROPERLY — later ruling "Cancelled by James, never caused issues" (the model deferral: got a final verdict) |
| J-3 | U1 model decision — "watch Groq lineup weekly, decide ~Aug 2" | S56 | weekly watch, dated | LIVE — 18 days out; folded into U-AUG9 keyfile day. Q: is the weekly Groq-lineup watch actually happening? |
| J-4 | U3 probe harness fire — "postponed to Aug 9" | S57 (Jul 7) | dated ✓ | HEALTHY but AT-RISK: probe file was to be committed via O1 "so it can't vanish" — see J-5 |
| J-5 | O1 version-control call (S55_appends, dryrun script, exports/, probe file untracked) | S56-S57 | parked for James | **UNKNOWN — if never ruled, the probe file may still be UNTRACKED and can vanish** (DET-DEAD-adjacent: dated deferral resting on an unversioned file) |
| J-6 | O4 SQL: clean raw-429 mad_reasoning fossils — "James in Supabase" | S57 | 5-min task | UNKNOWN |
| J-7 | C scorer fix (bear_used_numbers + consultant boilerplate) — banked into Aug 9 integrated session | S50 | dated ✓ | HEALTHY |
| J-8 | W-04 English-only pipeline — Phase 2 | Apr 12 | standing | STANDING (GNI_Myanmar frozen; ASEAN-language gap noted on /about/feedback as public claim ✓ honest) |
| J-9 | I4 rolling integrity check — design stage | S56 | open | Partially superseded by SUBPAGE-IC arc + daily integrity concept (S48) |
| J-10 | W-01 single-Groq dependency — acknowledged, fallback plan | Apr 12 | open | Largely paid: 3-account topology + Cerebras adaptive + CLIFF arc active |
| J-11 | W-02 arbitrator TPM collapse — acknowledged | Apr 12 | future | ✅ PAID — rate governor S46 (production-proven on Hormuz storm) |
| J-12 | Mission Control red — postponed | S53 | - | ✅ PAID S54 (benign threshold) |
| J-13 | I2-w wire GPVS verifier to cron — "after manual runs trusted" | S56 | conditioned | ✅ PAID S60 (`2c4be45`) |

### Ledger verdict
Of 13 explicit James-deferrals: 5 paid, 1 properly cancelled, 3 healthy-dated, **1 overdue for re-ruling (J-1), 3 unknown (J-5, J-6 + J-3's weekly-watch habit).**
The system works: dated deferrals with instruments got closed. The three unknowns share one trait — they ended in "James will do X in Supabase/GitHub" with no verify step scheduled.
**Lesson (append to R-S69-2):** a James-deferral needs the same instrument as a Claude-fallback: a date OR a trigger condition, plus a scheduled verify. "James in Supabase" without a verify line is how J-6-class items go dark.

### Additions to verify batch
```bash
# J-5: anything still untracked that a deferral rests on?
git status --short
git ls-files --others --exclude-standard | head -20
# J-1 context: manual MAD triggers since April (log check is James's memory + Actions history)
```

## CLASS 6 — CROSS-PROJECT FINDS (GNI debts parked in Lens-context records)
| ID | Debt | Born | Status |
|----|------|------|--------|
| D-8 | **L-CLIFF fix designed but living in a chat artifact**: S63 read lens_quota_guard.py (778 lines), reframed root cause as "dual source of truth" (guard's private model strings drifted from call sites — specimen `qwen/qwen3-32b` vs `qwen3-32b`), designed `lens_models.py` role registry — "analysis transferred to a Lens session artifact." Aug 16 = 32 days | S63 (Jul 11) | AT-RISK: is the design artifact saved to disk in C:/school/lens, or only in chat? A designed-fix-on-chat is DET-DEAD-adjacent. L-CLIFF queue says "Lens opener SOON" — verify artifact exists before that session |
| D-9 | **GNI_RULES.md duplicate-append anomaly**: S63 close grep returned 6 instead of 3 for the new rules — "investigate at S64 open" | S63 | UNKNOWN if S64 investigated — 1-grep verify |
| D-10 | "staging checker needs updating" | Mar 23 | UNKNOWN — no later record found; may be extinct with old architecture |
| D-5+ | Fox News in source_weights/credibility — flagged Mar 23 AND Apr 8, never confirmed cleaned | Mar 23 | STRENGTHENED: two flags, zero closures |
| ctx | /comparison 7/15/30-day trend windows = CFA-standard 3-horizon design (Mar 23, deliberate) | Mar 23 | F15 context: windows are designed; only the data window feeding them is capped. Relabel lean stands, now informed |
| ctx | LENS-001 "GNI Maintenance Protocol" — GNI work in Lens sessions: critical→quick commit, feature→queue, ALWAYS note in session record | Apr 11 | The instrument existed; cross-project leakage happens when the "note in session record" step is skipped — R-S69-2 kin |

### Verify additions
```bash
# D-9: duplicate rule appends?
grep -c "R-S63-1" GNI_RULES.md; grep -c "R-S63-2" GNI_RULES.md; grep -c "R-S63-3" GNI_RULES.md   # expect 1 each
# D-5: is Fox News still seeded anywhere in code?
grep -rn "Fox News" ai_engine/ --include="*.py" | head -5
```
(D-8 verify is a Lens-side `ls`: does the S63 L-CLIFF analysis doc exist in C:/school/lens?)

## S70 STATUS APPENDS (2026-07-16)
- D-7 CORRECTED: NOT paid. FLOOR_HIT lives only in mad_budget_solver.py; mad_runner has zero
  solver references. Import census result (above grep) determines: wired-elsewhere vs orphan
  (R-S69-3 class). Commit-2 (surface to MAD path) remains OPEN, load-bearing soon.
- F-TILES DISSOLVED into SRC-INTEGRITY I-9: Stimson deliberately dead (CF 403 bot-wall,
  PROMOTE-NYT S67 comment, rss_collector:95); frozen tile = fossil source_health DB row;
  fix = graveyard purge SQL + roster-filtered display. L762 tuple = test fixture, harmless.
- S70 morning: D-9 dead, F4 paid, Fox World lineage closed (60, ritual satisfied),
  I-8 (writer B silent-dead since Jul 8) + I-9 (fossil graveyard) added to integrity scope.
## S74 STATUS APPENDS (2026-07-17)
- D-11 BORN: escalation_scorer recalibration (June Option B) never executed -- deferred
  half laundered itself (R-S69-2 disease, no queue row existed). Evidence: 109/110 scored
  reports = 10.0, lone 5.0 is the PHI-003 gate's single firing in 17 calm-sentiment
  opportunities (sentiment 93 Bearish / 12 Neutral / 5 Bullish -- NOT pinned).
  Saturation is 3-LAYER: base caps (5+5+4=14 vs cap 10), diversity bonus guaranteed
  by S39 14/4/4 quota, CRITICAL_COMBOS fire near-daily (hormuz+iran=+3) which also
  mutes the gate's combo_bonus<3 condition. score_breakdown not persisted to reports,
  so combo theory unverifiable by SQL -- B design must add persistence.
  Feeds: frequency controller, CRITICAL alerts (>8 = always true), escalation_level,
  historical_correlations.avg_escalation_score. Architectural -> SWOT-gated session,
  POST-Groq-cliff (keyword-deterministic, not model-coupled; August belongs to cliff).
- D-9 re-verified at new path docs/GNI_RULES.md after S74 move: 1/1/1, stays dead.
- D-10 (Mar 23 staging checker): still UNKNOWN, likely extinct -- untouched this session.
