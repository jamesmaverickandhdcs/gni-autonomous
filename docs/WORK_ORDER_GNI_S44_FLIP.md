# WORK ORDER — GNI S44 arc-4 FLIP (enforce 3-tier gate + retier)
**Prepared:** 2026-06-17 · Chiang Mai UTC+7 · Team Geeks / Bro Alpha
**For:** Claude Code, in `C:\HDCS_Project\03\GNI_Autonomous`
**Basis:** two live dry-run crons (2026-06-16 0713 + 1451 UTC), reviewed in chat. This is the deferred arc-4 flip — every line below is grounded in those two forensic traces, not a hypothesis.

---

## 0. COLD-START
```bash
cd /c/HDCS_Project/03/GNI_Autonomous && source venv/Scripts/activate
git fetch && git log --oneline -3      # confirm HEAD = 5369d2a (arc 6) or later
```
Hard rules (reference by ID, do not re-derive): GNI-R-037/076 (BEV), GNI-R-233 (read files, reset when corrected), GNI-R-242 (prove on live data), LR-078 (ship-to-file patch), LR-100 (grep downstream of any change), LR-101 (pure-ASCII anchors), W2 (assert count==1). py_compile before commit; git push after (cron runs on GitHub Actions).

---

## 1. WHY THE FLIP IS SAFE (dry-run evidence, both crons)
- Drop counts 366 / 346 of ~670 — expected band, backlog rejection working.
- **Dead-feed ghosts now caught at the gate:** DFRLab 1660h, Bellingcat 1441h, ICIJ "Donate" (no-date) — all dropped, none reach readers. O1 fully closed.
- **S1b cliff fix proven:** War on the Rocks / Breaking Defense / Bellingcat / Amnesty / DFRLab all 100% Pass-S1b both runs (were 20->0 before arc 6). WoR even got selected.
- **No analysis-tier starvation:** opinion-tier sources collect + pass fine at 120h.
- **FFF live:** channel posts carry "Freedom from Fear Intelligence"; Meduza/Moscow Times/RFE-RL/Myanmar Now landing in the pool.

---

## 2. THE FLIP (one commit)
**2a. Retier (evidence: both sources selected top-of-pillar but zero-kept at 18h news gate):**
- EFF Deeplinks: add `"tier": "opinion"` (newest 79h/87h; cred 91; selected both runs, avg score 25.9/32.0)
- IEEE Spectrum: add `"tier": "opinion"` (multi-day cadence, gaps to 400h; selected both runs)
- Anchor each on its unique URL line. Krebs on Security stays news/accepted-casualty (131h+ cadence, gaps to 1128h — too slow even for 120h, low selection value).

**2b. Flip the gate:**
```python
CAPTURE_GATE_DRY_RUN = False
```
**2c. LR-100:** `tier` is read only by `_window_for` in `rss_collector.py` — contained, no downstream migration (already verified arc 4).

**2d. Verify + ship:**
```bash
python -m py_compile ai_engine/collectors/rss_collector.py && echo OK
# self-test: tier counts should be opinion=10, review=4, news=28 (total 42)
git add -A && git commit && git push
```

---

## 3. WATCH THE FIRST ENFORCING CRON (the gate after this commit)
Next gni_pipeline.yml run (02:00 / 10:00 UTC) is the first that actually DROPS in production. Confirm:
- Real drop count ~350 (matches dry-run).
- All 22 selection slots still fill.
- No opinion-tier source fully starved (HRW/Amnesty/ICIJ/Bellingcat/WoR/DFRLab/EFF/IEEE should still surface their fresh items).
- The selected 22 lose the stale picks that dry-run was tolerating.

---

## 4. LOG — follow-up bug arc (do NOT bundle into the flip; separate small arc)
- **RFE/RL dedup loss:** Pass-S1b 17->S2 7 (run1), 16->5 (run2) — ~65% culled at dedup. Plus junk header rows parsed as articles ("Majlis"/"Home" at ~48,000h). Action: parse-guard the feed-chrome rows; investigate why RFE/RL duplicates so heavily (likely wire overlap on Ukraine/Iran). RFE/RL is the weakest new port — consider replacement if it stays low-yield.
- **Yahoo Finance fake-old timestamps:** entries at 13,096h and 1,511h — undated items getting bad dates. Aggregator noise (predicted). Action: tighten date parsing or watch; candidate for a cleaner free FIN source.

---

## 5. LOG — observations for a FUTURE scoring arc (not now)
- **Opinion-tier under-selection:** HRW/Amnesty/ICIJ/DFRLab/WoR/RFA/Bellingcat collect + pass fine but rarely win Stage-4 slots — the 22 are dominated by news-tier wire (AP/AlJazeera/BBC/CNBC/DW/Dawn). The 120h tier keeps them alive in the pool but they don't win slots. If the FFF/analysis layer is meant to surface deep signal, Stage-3 may need a small opinion-tier scoring boost. Design carefully (don't over-correct).

---

## 6. PROPOSED NEW RULE (assign an LR id)
Born from arc 6: **A work order's stated root cause is a hypothesis, not a finding.** Trace the live code path and reproduce empirically before fixing — the named culprit may be dead code. (Arc 6: the documented S1b culprit `prompt_injection_detector.py:108` was unused; the real cause was the funnel's `(send|forward|post|submit|exfiltrate).{0,50}url` pattern. Recommend deleting the dead module.)

---
— End of flip work order. One commit (§2), watch one cron (§3), then bugs/observations are separate. 🤜
