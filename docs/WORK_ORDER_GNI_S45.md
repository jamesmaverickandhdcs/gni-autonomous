# WORK ORDER — GNI Autonomous S45 (post-flip health recalibration)
**Prepared:** 2026-06-19 · Chiang Mai UTC+7 · Team Geeks / Bro Alpha
**For:** Claude Code, in `C:\HDCS_Project\03\GNI_Autonomous`
**Basis:** two LIVE ENFORCING crons (2026-06-18 0643 + 1244 UTC) + their forensic traces, reviewed in chat. The S44 flip succeeded — the gate is enforcing correctly. This arc fixes the *side effect* the enforcing runs exposed, not the gate.

---

## 0. COLD-START
```bash
cd /c/HDCS_Project/03/GNI_Autonomous && source venv/Scripts/activate
git fetch && git log --oneline -3      # confirm HEAD = fee2c42 (S44 flip) or later
```
Operator: James ("Bro Alpha"). Warm tone, hard gates. One question per turn.
Hard rules (reference by ID): GNI-R-037/076 (BEV — read full file before edit), GNI-R-233 (read files, reset when corrected), GNI-R-242 (prove on live data), LR-078 (ship-to-file patch), LR-100 (grep downstream of any change), LR-101 (pure-ASCII anchors), W2 (assert count==1), LR-105 (dry-run-first protects the future). py_compile before commit; push after.

---

## 1. WHY — what the enforcing runs revealed (read before touching anything)
The flip works: gate dropped 361 then 341, kept 22, all 3 pillars filled, quality 9.35/7.65, FFF live. Collected volume fell ~670 -> ~330 — **expected and correct** (stale backlog no longer carried).

THE PROBLEM (self-reinforcing false-failure loop):
- Freshness gate drops stale-at-collection articles -> a slow source's *survivor count* falls -> `source_health_monitor` compares that count to a rolling average **learned in the pre-gate era** (when stale backlog inflated counts) -> flags "RSS FAILURE" -> fires a reserve-DOWN alert.
- But the source is NOT down. DFRLab/ICIJ/Bellingcat/Krebs/Rest of World hit 0 *because their newest real content is >120h old right now* — healthy, slow, correctly gated. The 0643 run fired 6 simultaneous "Source DOWN" alerts; 1244 fired 5. That is cry-wolf alert fatigue.

**Philosophy framing (PHI-001 "intelligence as a right"):** a flood of false alarms buries the real signal. Honest health reporting is part of intelligence integrity — the operator must be able to trust a DOWN alert means DOWN. The gate became honest; the health baseline must catch up.

---

## 2. ARC A (URGENT) — recalibrate source health for the post-gate world
**BEV FIRST:** read `ai_engine/analysis/source_health_monitor.py` fully before editing. Do not hot-patch.

Root cause: health is measured on **post-gate survivor count**. It must be measured on **fetch success**, because the freshness gate is a legitimate downstream filter, not a health signal.

PROPOSED DESIGN (confirm sound on BEV, then implement):
- Separate two concepts the monitor currently conflates:
  - **Fetch health** = did the feed return HTTP 200 with >=1 *raw* parseable entry (BEFORE the freshness gate)? This is the real up/down signal.
  - **Yield** = how many survived the gate. Expected to be LOW (often 0-2) for opinion-tier sources. NOT a failure.
- A source is "DOWN" only if **fetch fails OR raw entry count == 0** (pre-gate). Never alert on post-gate survivor count alone.
- **Tier-aware:** opinion-tier (120h) sources are *expected* to yield 0-2/run. Exempt them from count-based alerting; health-check them on fetch success only.
- **Re-baseline the rolling averages** now that the gate enforces — the pre-gate averages (e.g. "was averaging 5.0") are obsolete inflated baselines. Reset or recompute from post-gate runs.
- LR-100: grep every reader of the health/average fields and the reserve-activation trigger; confirm the reserve auto-activation keys off the new "fetch-down" signal, not yield.

DRY-RUN (LR-105): run against the next live cron (or replay the two 0618 traces) and confirm: the genuinely-fetch-broken feeds (Stimson, occasionally Crisis Group/AP-Google) still flag, while slow-but-fetched feeds (DFRLab/ICIJ/Bellingcat/WoR/HRW) do NOT flag. Only flip alerting live after that proof.

---

## 3. ARC B (IMPORTANT) — junk-header parse guard
**BEV:** read `parse_date` + the entry-ingest loop in `rss_collector.py`.

Confirmed live across all enforcing runs: some `site:`/archive feeds emit nav/chrome rows as entries with epoch-zero dates:
- RFE/RL: "Video Archive - Radio Free Europe/Radio Liberty" -> 63,554h
- The Irrawaddy: "Rohingya Archives - The Irrawaddy" -> 81,840h
- (earlier: RFE/RL "Majlis"/"Home"; ICIJ "Donate to ICIJ" no-date)

These currently drop at the gate (harmless to output) but pollute logs AND the health count. Add a guard that skips an entry if:
- its published date is implausibly old (lag > ~43,800h / 5 years -> treat as feed-chrome, not an article), OR
- its title equals/contains the feed's own `<title>` or matches a small chrome denylist ("Video Archive", "Archives", "Home", "Donate to").

Skip BEFORE the entry enters the pipeline and BEFORE it counts toward the source's raw-entry total. Pure-ASCII anchors (LR-101), assert count==1 (W2).

---

## 4. ARC C (IMPORTANT) — RFE/RL decision
Enforcing data confirms RFE/RL is the weakest port: junk header rows + heavy dedup loss (S1b 16 -> S2 13/11 every run, ~3-4 lost to dedup) + never selected. After Arc B removes the junk rows, run one cron and re-check its real yield. Then decide: keep (if dedup loss is just wire-overlap on hot stories and it still surfaces unique items) or replace with a cleaner free outlet. JAMES DECIDES after the data is clean.

---

## 5. LOGGED — observations, low urgency (do NOT bundle)
- **Yahoo Finance:** noisy aggregator (12 collected, 1 passed S1, avg 1.3, geo 8%). FIN fills fine via the Google feeds; candidate for replacement, low priority.
- **Stimson Center:** persistent fetch error, no reserve, contributes nothing for many sessions — formally retire or fix the URL.
- **The Conversation / Africa Is A Country:** collect 1-2, pass 0 at S1 relevance (off-topic, not stale). Check keyword fit; cosmetic.
- **MAD Arbitrator consistency:** one 0618 run scored Arbitrator 66.7% ("Arb consistent: False"). Watch; if recurring, inspect cross-run verdict injection.
- **Opinion-tier value:** WoR/HRW/Bellingcat/EFF ARE getting selected under enforcing (HRW earning 15-25 avg score) — tier is working. DFRLab/ICIJ often 0; revisit only if they stay dark after Arc A/B.

---

## 6. PHILOSOPHY ANCHOR (why this arc matters)
- **PHI-001 (intelligence as a right):** false-alert noise is an access barrier of its own — it buries real signal. Honest health = honest intelligence.
- **PHI-002 (from/of/for the people):** the slow analysis/FFF sources (HRW, Amnesty, Bellingcat, Myanmar Now, Meduza) are exactly the voices we must NOT auto-drop just because they publish slowly. Tier-aware health protects them.
- **PHI-003 (Freedom from Fear):** the FFF early-warning layer depends on slow, deep sources surviving in the pool. Don't let a count threshold silence them.

---

## 7. STAGED COMMIT ORDER (slow is faster than wrong — S43 lesson)
1. **Arc B** (junk-header parse guard) — smallest, cleans the data first so Arc A measures truth.
2. **Arc A** (health recalibration) — BEV-heavy, dry-run, then flip alerting.
3. **Arc C** (RFE/RL) — only after B+A give clean data; James decides.
4. Logged items — separate future session.

After each: py_compile -> self-test -> commit -> push. Begin close at 80% context (LR-057).

— End S45 work order. The gate is honest; make the health monitor honest too. 🤜
