# GNI_Autonomous — Global Nexus Insights

**L7 Autonomous Geopolitical Intelligence Pipeline**
Higher Diploma in Computer Science | Spring University Myanmar (SUM)
Sprint: March 20–29, 2026 | Days 7–17

---

## Live Deployment

- **Dashboard:** https://gni-autonomous.vercel.app
- **Health Monitor:** https://gni-autonomous.vercel.app/health
- **Intelligence History:** https://gni-autonomous.vercel.app/history
- **Market Analysis:** https://gni-autonomous.vercel.app/stocks
- **Transparency Engine:** https://gni-autonomous.vercel.app/transparency

> **Note:** The diploma project (frozen) is at https://gni-dusky.vercel.app — do not modify.

---

## What is GNI_Autonomous?

GNI_Autonomous is a fully autonomous geopolitical intelligence pipeline that:

1. Collects 242 articles/run from 13 carefully selected RSS sources
2. Runs them through a 4-stage intelligence funnel with 66 injection patterns
3. Scores, validates, and analyses them with Llama 3 via Ollama (local) or Groq (cloud)
4. Runs a Multi-Agent Debate (Bull vs Bear vs Arbitrator) for market direction
5. Scores escalation risk across 3 pillars: Technology, Geopolitical, Financial
6. Detects coordinated narratives across sources
7. Sends CRITICAL ALERTS to Telegram when escalation ≥ 8/10
8. Saves everything to Supabase with full transparency and immutable audit trail

**Quality score achieved: 9.25/10 [Excellent]**

---

## Architecture

### Pipeline Steps

| Step | Name | Description |
|------|------|-------------|
| 1 | RSS Collection | 242 articles from 13 sources |
| 2 | Intelligence Funnel | 4-stage: relevance → injection → dedup → scoring |
| 2b | Dedup Check | Skip LLM if same topic < 6h ago (>70% overlap) |
| 2c | Prompt A/B Selection | Alternate v1/v2 prompts, track quality per variant |
| 3 | AI Analysis | Llama 3 via Ollama (local) or Groq (cloud) |
| 3b | Quality Scoring | 5-dimension 10-point rubric |
| 3e | Semantic Validation | 10 checks: sentiment/score/tickers/risk/location |
| 3c | MAD Protocol | Bull vs Bear vs Arbitrator debate |
| 3f | Deception Detection | Centroid clustering — coordinated narrative detection |
| 3d | Escalation Scoring | 3-pillar risk: Tech + Geo + Financial |
| 4 | Save to Supabase | Full report with all fields |
| 5 | Article Trace | 242 articles documented per run |
| 5 | Telegram | CRITICAL ALERT + consolidated report + AI thinking |
| 7 | Runtime Log | Complete audit log |

### Source Coverage

| Source | Coverage | Pillar |
|--------|----------|--------|
| Al Jazeera | Middle East / Non-Western | Geopolitical |
| CNN / BBC / Fox / DW / France 24 | Global Western | Geopolitical |
| USNI News | Naval / Maritime / All oceans | Geopolitical |
| Straits Times | South China Sea / ASEAN | Geopolitical |
| Eye on the Arctic | Arctic competition | Geopolitical |
| Bloomberg Markets | Markets / Commodities | Financial |
| Nikkei Asia | Asia-Pacific finance | Financial |
| Wired | AI chips / Cyber | Technology |
| MIT Technology Review | Semiconductors / AI policy | Technology |

### Keyword Priority (Tiered)

- **Tier 4 (first):** Red Sea, Hormuz, Malacca, South China Sea, chokepoints
- **Tier 5:** AI chips, semiconductors, critical minerals, debt trap, belt and road
- **Tier 1:** China, Russia, Iran, Israel, Ukraine, Taiwan, North Korea
- **Tier 2:** War, nuclear, invasion, attack, sanctions, coup
- **Tier 3:** Economy, oil, trade, inflation, tariff
- **Tier 6:** Elections, diplomacy, NATO, UN
- **Tier 7:** Humanitarian, climate, pandemic

---

## Security

### Injection Detection
- 66 patterns across 10 categories
- Direct overrides, score manipulation, bias manipulation
- Prompt boundary attacks, encoded attacks, multilingual injections
- Role confusion/jailbreak, context overflow, nested injections
- Financial manipulation, data exfiltration
- **Pentest result: 9/9 attacks blocked, 0 false positives — Grade A+**

### Semantic Validation
10 checks on every LLM output:
- Sentiment/score direction match
- Extreme confidence detection
- Ticker whitelist enforcement
- Risk/sentiment consistency
- Market impact depth check
- Location validity (country not region)
- Source consensus range validation
- Title and summary presence

### MAD Security
- Verdict whitelist validation
- Confidence clamping to [0.0, 1.0]
- Injection signal detection in all 3 agent outputs

---

## Self-Improvement (L6)

### Prompt A/B Testing
- v1: Baseline production prompt
- v2: Improved specificity + source consensus instructions
- Alternates even/odd runs
- Auto-promotes winner after 10 runs if quality difference ≥ 0.3

### Source Credibility Model
- 13 sources seeded at neutral 0.750
- GPVS-based scoring: sources in accurate reports gain credibility
- Credibility maps to source_weights (0.5–2.0 range)
- Recalculates every 10 pipeline runs

---

## Autonomy (L7)

### Escalation Scorer
3-pillar risk scoring: Technology + Geopolitical + Financial
- CRITICAL (≥9): 🚨 fires Telegram CRITICAL ALERT
- HIGH (≥7): 🟥
- ELEVATED (≥5): 🟧
- MODERATE (≥3): 🟨
- LOW: 🟢

### Autonomous Frequency Control
- CRITICAL ≥9.5: run every 30 minutes
- CRITICAL: every 1 hour
- HIGH: every 2 hours
- ELEVATED: every 4 hours
- MODERATE: every 6 hours
- LOW: every 12 hours

### Deception Detection
- Centroid clustering across all top articles
- Flags when 3+ different sources share 60%+ keyword core
- Discounts source_consensus_score by 25% when coordination detected

### Health Agent
5 automated health checks:
1. Run gap (>26h since last success)
2. Quality drift (avg <6.0 or drift >1.5 points)
3. Article collection volume (<100 articles)
4. MAD confidence trend (<0.4 average)
5. Escalation spike (≥9.0 in last 24h)

### Immutable Audit Trail
- SHA-256 hash chain: hash(event_type + event_data + previous_hash)
- Tamper-evident: any modification breaks the chain
- verify_chain_integrity() validates entire chain
- Event types: REPORT_SAVED, PIPELINE_RUN, ESCALATION, SECURITY_FLAG, SYSTEM_START

### Self-Healing Runner
- Tier 1 (RSS collection failure): retry 3x with 30s delay
- Tier 2 (Funnel failure): retry 2x
- Tier 3+ (Analysis failure): no retry — too expensive
- All events logged to audit trail

---

## Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Ollama with llama3:8b (local development)
- Groq API key (GitHub Actions / cloud)
- Supabase account
- Telegram bot token

### Environment Variables
```
SUPABASE_URL=
SUPABASE_SERVICE_KEY=
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
GROQ_API_KEY=
GROQ_MODEL=llama-3.3-70b-versatile
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

### Installation
```bash
pip install -r requirements.txt
npm install
```

### Run Pipeline
```bash
python ai_engine/main.py
```

### Run with Self-Healing
```bash
python ai_engine/self_healing_runner.py
```

### Build Frontend
```bash
npm run build
```

---

## Engineering Rules (L1–L39)

Key rules observed throughout this sprint:

- **L20:** Read before edit — always read files before modifying
- **L23:** GROQ_MODEL env var — never hardcode model names
- **L26:** npm run build before git push
- **L29/L31/L32:** PowerShell safety — use Python writers for file creation
- **L33:** Always use llama-3.3-70b-versatile (L33)
- **L34:** Analytical novelty — causal language in market_impact
- **L35:** Three-minute plan check before every session
- **L36:** Battle Log updated every session
- **L37:** Declare deviations immediately
- **L38:** Day 7–17 numbering
- **L39:** Briefing from Sprint Plan

---

## Sprint Achievement

| Metric | Value |
|--------|-------|
| Sprint Duration | Days 7–17 (March 19–29, 2026) |
| Autonomy Level | L4 → L7 |
| Quality Score | 9.25/10 [Excellent] |
| Sources | 13 RSS sources |
| Articles/Run | 242 |
| Pipeline Steps | 20 |
| Analysis Files | 17 |
| Security Patterns | 66 injection patterns |
| Security Grade | A+ (9/9 pentest) |
| Commits | 30+ |
| Supabase Tables | 15+ |

---

## Diploma Note

This project is the sprint evolution of GNI v1.0 (frozen at gni-dusky.vercel.app).
The diploma codebase was frozen on Day 7 (March 19, 2026) before this sprint began.
GNI_Autonomous represents the autonomous intelligence system built on top of the diploma foundation.

**Higher Diploma in Computer Science | Spring University Myanmar (SUM) | 2026**
