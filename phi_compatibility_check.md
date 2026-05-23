# PHI-003 Philosophy Compatibility Check
# GNI Autonomous — Team Geeks
# Rule: LR-099 — Every philosophy update requires this file to be reviewed and updated before session close.
# Last verified: May 24, 2026 (GNI S36)

## Non-Negotiables Mapping

| NN | Principle | Code Location | Status | Last Verified |
|---|---|---|---|---|
| NN-PHI-1 | GNI serves the human being, not the market. Teenager Standard. | `nexus_analyzer.py` FFF prompt + `brief/page.tsx` FFF section | LIVE | May 24 2026 |
| NN-PHI-2 | All news directions equal — good, bad, opportunity, threat | `intelligence_funnel.py` OPPORTUNITY keywords + balance signal | LIVE | May 24 2026 |
| NN-PHI-3 | Manipulation techniques never in GNI output | `intelligence_funnel.py` INJECTION_PATTERNS Cat 1-11 + SANITIZE_VOCAB | LIVE | May 24 2026 |
| NN-PHI-4 | Every threat must have a path — fff_human_path always required | `nexus_analyzer.py` + `prompt_manager.py` fff_human_path field | LIVE | May 24 2026 |
| NN-PHI-5 | Absence is intelligence — coverage gaps reported | NOT IMPLEMENTED | OPEN | — |
| NN-PHI-6 | Adversarial sources are signal not authority — review_only | `rss_collector.py` content_type + `intelligence_funnel.py` classifier | LIVE | May 23 2026 |
| NN-PHI-7 | Data reset when philosophy resets | U-8 executed May 23 2026 | COMPLETE | May 23 2026 |

## Output Layer Compatibility

| Output | FFF Fields | Status | Last Verified |
|---|---|---|---|
| Main report (`reports` table) | fff_what_is_happening, fff_honest_analysis, fff_human_path | LIVE | May 24 2026 |
| Pillar reports (`pillar_reports` table) | fff_what_is_happening, fff_honest_analysis, fff_human_path | LIVE | May 24 2026 |
| Brief page (`/brief`) | FFF section displayed | LIVE | May 24 2026 |
| Telegram channel | FFF section appended | LIVE | May 24 2026 |
| MAD protocol | Receives stage1b_passed articles only | LIVE | May 23 2026 |

## Scoring Compatibility

| Principle | Scoring Implementation | Status |
|---|---|---|
| All directions equal | OPPORTUNITY keywords +3 each, balance signal +3 | LIVE |
| Depth over speed | Recency capped at +2 when content score < 5 | LIVE |
| Source diversity | max_per_source=2 | LIVE |
| Adaptive vocabulary | YAKE unsupervised extraction | LIVE |
| Dynamic relevance | BM25 query-based scoring | LIVE |

## Open Items (NN-PHI not yet implemented)

| # | Item | Priority |
|---|---|---|
| NN-PHI-5 | Absence detection — coverage gap reporting | S37 |
| GPVS | Human security track alongside SPY metric | S37 |
| Layer 4 | LLM spot-check for ambiguous article classification | S37 |
| About page | Update copy to reflect PHI-003 identity | S37 |
| Banner | Update from "rebuilding" to "PHI-003 live" | S37 |

## Instructions for Next Philosophy Update

1. Open this file FIRST before any implementation
2. Review every row — mark any principle that the new philosophy changes
3. For each changed principle — identify the code location that implements it
4. Add new rows for any new non-negotiables
5. Mark implementation status as OPEN for anything not yet coded
6. Do not close the session until all OPEN items are either implemented or explicitly deferred with a session number
