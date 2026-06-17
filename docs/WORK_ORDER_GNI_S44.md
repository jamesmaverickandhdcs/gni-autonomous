# WORK ORDER — GNI Autonomous S44
**Prepared:** 2026-06-15 · Chiang Mai UTC+7 · Team Geeks / Bro Alpha
**For:** Claude Code instance, working in `C:\HDCS_Project\03\GNI_Autonomous`
**Source of truth:** every URL/tier below was LIVE-VERIFIED in chat this session (freshness + paywall + date-presence). Do not re-derive — but DO re-run the verify block before committing new feeds (GNI-R-242).

---

## 0. COLD-START (do first)
```bash
cd /c/HDCS_Project/03/GNI_Autonomous && source venv/Scripts/activate
git fetch && git log --oneline -3      # confirm HEAD a07ee3d or later
```
Operator: James ("Bro Alpha"). Warm tone, hard gates underneath. One question per turn.
Hard rules (reference by ID, do not re-derive): GNI-R-037/076 (BEV, read full file before edit), GNI-R-233 (never conclude before reading files; reset when corrected), GNI-R-242 (verify on live data, prove before commit), LR-078 (ship-to-file patch, not heredoc), LR-100 (after changing X, grep every Y that depends on X), LR-101 (pure-ASCII patch anchors), W2 (`assert count==1` on every anchor). py_compile before every commit. git push after commit (cron runs on GitHub Actions, not the laptop).

Primary file: `ai_engine/collectors/rss_collector.py` (SOURCES dict + ANALYSIS set at line ~202 + parse_date tuple + capture-lag gate).

---

## 1. THE 3-TIER FRESHNESS MODEL (architecture change — L2, dry-run first)
**Replace** the current hardcoded 2-tier scheme (18h news / 168h analysis, analysis-set at line ~202) with a **per-source `tier` field** + a window map:

```python
TIER_WINDOW_HOURS = {"news": 18.0, "review": 48.0, "opinion": 120.0}
```
- Every source declares `"tier": "news" | "review" | "opinion"`.
- Capture-lag gate: `lag = collected_at - published_at`; drop if `lag > TIER_WINDOW_HOURS[tier]`.
- Missing/unparseable publish date = STRICT DROP (keep the existing `date_is_real` flag from `parse_date`'s (iso, bool) tuple).
- NOTE: opinion tightens from 168h -> **120h**. Re-confirm no opinion source's normal cadence exceeds 120h (RFA at ~102h is the closest — watch it).
- LR-100 sweep: grep every reader of the old analysis-set / 18h constant and migrate them to the map.
- DRY-RUN (`CAPTURE_GATE_DRY_RUN=True`) on one live cron, confirm drop counts sane per tier, THEN flip.

---

## 2. PAYWALL CUT (PHI-001 — direct + indirect paid). Smallest arc, do early.
REMOVE from SOURCES (paid links are dead-on-arrival to free Telegram readers):
- **Wired** `https://www.wired.com/feed/rss` (TECH) — metered
- **Bloomberg Economics** `https://feeds.bloomberg.com/economics/news.rss` (FIN) — hard metered
- **Project Syndicate** `https://www.project-syndicate.org/rss` (FIN) — freemium register-gate
- **VERIFY then cut:** The Africa Report (metered?), War on the Rocks (membership but most free — likely KEEP)
**FIN backfill** (cutting Bloomberg+ProjSynd drops FIN to 2): add free Google-News FIN feeds from §4.

---

## 3. O1 — DEAD FEED SWAP (both confirmed serving 2023 archive content)
- DFRLab: REPLACE `https://medium.com/feed/dfrlab` -> **`https://dfrlab.org/feed/`** (they moved off Medium Feb 2025). Verified fresh 147h. **MUST add "DFRLab" to opinion tier** or its weekly cadence dies at 18h.
- CNN: REMOVE `http://rss.cnn.com/rss/edition.rss` entirely (whole rss.cnn.com host frozen Aug 2024). Replace with **NDTV World** (§4).
- ALSO REMOVE: **Global Times** `https://www.globaltimes.cn/rss/outbrain.xml` if present (Chinese state media).

---

## 4. NEW SOURCE PORTS — all LIVE-VERIFIED this session (newest-entry age shown)
All fold into **GEO pillar** unless noted. ⚖️ = government-funded (apply bias-laundering guard + OP-005, weight BELOW reader/NGO outlets).

### tier: "news" (18h)
| name | url | verified |
|---|---|---|
| Fox News World | `https://moxie.foxnews.com/google-publisher/world.xml` | 11.7h (US-right balance) |
| NDTV World | `https://feeds.feedburner.com/ndtvnews-world-news` | 8.2h (CNN replacement) |
| Myanmar Now | `https://myanmar-now.org/en/feed/` | 11.9h |
| Meduza EN | `https://meduza.io/rss/en/all` | 7.9h |
| The Moscow Times | `https://www.themoscowtimes.com/rss/news` | 9.6h |
| Daily NK | `https://www.dailynk.com/english/feed/` | 10.8h |
| Hong Kong Free Press | `https://hongkongfp.com/feed/` | 11.8h |

### tier: "review" (48h)
| name | url | verified |
|---|---|---|
| RFE/RL ⚖️ | `https://news.google.com/rss/search?q=when:48h+site:rferl.org&hl=en-US&gl=US&ceid=US:en` | 20.6h |
| Global Voices | `https://globalvoices.org/feed/` | 18.3h |

### tier: "opinion" (120h)
| name | url | verified |
|---|---|---|
| Radio Free Asia ⚖️ | `https://www.rfa.org/english/rss2.xml` | 102.1h (slow — watch) |

### DEAD direct feeds -> use Google-News `site:` fallback (auto-satisfies freshness via when:48h)
- The Irrawaddy -> `https://news.google.com/rss/search?q=when:48h+site:irrawaddy.com&hl=en-US&gl=US&ceid=US:en`
- IranWire -> `https://news.google.com/rss/search?q=when:48h+site:iranwire.com&hl=en-US&gl=US&ceid=US:en`

### FIN backfill (free, Google-News — add `when:24h` where missing)
- Financial Stability: `...q=when:24h+%22sanctions%22+OR+%22financial+stability%22+OR+%22debt+crisis%22`
- Central Banks: `...q=when:24h+%22central+bank%22+OR+%22Federal+Reserve%22+OR+%22interest+rates%22+OR+%22inflation%22`
- IMF/World Bank: same pattern, ADD `when:24h` (Lens versions lack it -> would be gutted by gate)

### REFERENCE-ONLY (do NOT add as collected feed)
- **Freedom House** `https://freedomhouse.org/rss.xml` — newest 139.3h **exceeds the 120h ceiling**; keep as democracy-score reference, or a `site:freedomhouse.org` Google fallback for fresher mentions.

---

## 5. FFF KEYWORD SET — `PHI003_FREEDOM_FROM_FEAR` (folded into GEO, NOT a 4th pillar)
Rationale: mass mobilization/crackdowns under authoritarian regimes are leading indicators of geopolitical rupture (UN human-security "Freedom from Fear" pillar; civil-resistance scholarship). This is PHI-003 pointed at early warning.

**Universal terms:** political prisoner, prisoner of conscience, arbitrary detention, enforced disappearance, civil disobedience, nonviolent resistance, pro-democracy protest, crackdown, internet shutdown, censorship, dissident, exile, defector, junta, martial law, Magnitsky, targeted sanctions.

**Country-specific (high-signal proper nouns):**
- Myanmar: Spring Revolution, NUG, People's Defence Force, PDF, Civil Disobedience Movement, CDM, Tatmadaw
- China: White Paper protest, A4 revolution, Uyghur, Xinjiang, Tibet, Hong Kong, 709 crackdown
- Iran: Woman Life Freedom, Mahsa Amini, hijab protest, IRGC, Evin prison
- Russia: Navalny, FBK, Anti-Corruption Foundation, foreign agent law, Memorial, mobilization protest
- North Korea: defector, kwanliso, political prison camp, forced labor
- Belarus: Tsikhanouskaya, Viasna, Bialiatski, 2020 protests

**Symmetry rule:** RFA + RFE/RL are US-government-funded — same category as the RT/TASS/Global Times we cut, opposite flag. Keep them (irreplaceable where no free press exists) BUT apply the same bias-guard + OP-005, and weight reader/NGO outlets (Meduza, Moscow Times, Myanmar Now, HKFP) above them. No state's narrative gets laundered.

---

## 6. S1b INJECTION CLIFF (separate root-cause arc — AFTER 1-5)
In the 0708 trace, War on the Rocks/Breaking Defense/Bellingcat/Amnesty/DFRLab collected fine, passed S1 relevance, then got WIPED 20->0 at Stage 1b. Root cause hypothesis: `ai_engine/funnel/prompt_injection_detector.py:108` domain allowlist regex flags full-content feeds whose article bodies carry many non-allowlisted links. Two sub-tasks:
1. The allowlist still lists dead/cut domains (reuters, nikkei, ft, technologyreview) — clean it.
2. Breaking Defense: GNI uses `/full-rss-feed/` (full body); Lens uses `/feed/` (summary). Switching to summary feed MAY fix the cliff — test.
**BEV first** — read `prompt_injection_detector.py` fully before touching. Do not hot-patch.

---

## STAGED COMMIT ORDER (one verified commit each — slow is faster than wrong, S43 lesson)
1. Paywall cut (§2) — pure deletion + FIN backfill
2. O1 swap + Global Times removal (§3)
3. New source ports (§4) — re-run the feed-verify block FIRST, keep only live+fresh
4. 3-tier refactor (§1) — DRY-RUN one cron, then flip
5. FFF keyword set (§5)
6. S1b injection cliff (§6) — separate arc

After each: py_compile -> (yaml-validate if touched) -> self-test -> commit -> push. Begin session close at 80% context (LR-057).

---

## VERIFY BLOCK (re-run before committing any new feed)
```bash
printf '\e[?2004l'
python - << 'EOF'
import requests, feedparser, time
from datetime import datetime, timezone
H={'User-Agent':'Mozilla/5.0 (compatible; GNI/1.0)'}; NOW=datetime.now(timezone.utc)
C=[  # (name, url, tier_window_hours)
 ("Fox News World","https://moxie.foxnews.com/google-publisher/world.xml",18),
 ("NDTV World","https://feeds.feedburner.com/ndtvnews-world-news",18),
 ("Myanmar Now","https://myanmar-now.org/en/feed/",18),
 ("Meduza EN","https://meduza.io/rss/en/all",18),
 ("Moscow Times","https://www.themoscowtimes.com/rss/news",18),
 ("Daily NK","https://www.dailynk.com/english/feed/",18),
 ("Hong Kong Free Press","https://hongkongfp.com/feed/",18),
 ("RFE/RL (GN)","https://news.google.com/rss/search?q=when:48h+site:rferl.org&hl=en-US&gl=US&ceid=US:en",48),
 ("Global Voices","https://globalvoices.org/feed/",48),
 ("Radio Free Asia","https://www.rfa.org/english/rss2.xml",120),
 ("DFRLab new","https://dfrlab.org/feed/",120),
]
def age(e):
    t=e.get('published_parsed') or e.get('updated_parsed')
    return None if not t else (NOW-datetime.fromtimestamp(time.mktime(t),tz=timezone.utc)).total_seconds()/3600
for name,url,lim in C:
    try:
        r=requests.get(url,headers=H,timeout=20); f=feedparser.parse(r.content); n=len(f.entries)
        if n==0: print(f"{name:22} DEAD/EMPTY -> Google site: fallback"); continue
        a0=age(f.entries[0]); tag="NO-DATE!" if a0 is None else f"{a0:6.1f}h"
        flag="FRESH" if (a0 is not None and a0<=lim) else "STALE/NODATE"
        print(f"{name:22} n={n:3} newest={tag} [{flag} <= {lim}h]")
    except Exception as e: print(f"{name:22} ERR {str(e)[:30]}")
EOF
```

— End of S44 work order. Hand to Claude Code; build in staged order. 🤜
