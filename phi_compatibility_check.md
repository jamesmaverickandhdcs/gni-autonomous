# PHI-003 Philosophy Compatibility Check
# GNI Autonomous — Team Geeks
# Rule: LR-099 — Every philosophy update requires this file to be reviewed and updated before session close.
# Last verified: May 31, 2026 (GNI S40)

## Non-Negotiables Mapping

| NN | Principle | Code Location | Status | Last Verified |
|---|---|---|---|---|
| NN-PHI-1 | GNI serves the human being, not the market. Voting-Age Standard. | `nexus_analyzer.py` FFF prompt + `brief/page.tsx` FFF section + `escalation_scorer.py` PHI-003 consistency gate (escalation must agree with honest sentiment/risk read -- no manufactured fear) + `self_bias_gate.py` daily audit (escalation-sentiment coherence) | LIVE | May 31 2026 |
| NN-PHI-2 | All news directions equal — good, bad, opportunity, threat | `intelligence_funnel.py` OPPORTUNITY keywords + balance signal | LIVE | May 24 2026 |
| NN-PHI-3 | Manipulation techniques never in GNI output | `intelligence_funnel.py` INJECTION_PATTERNS Cat 1-11 + SANITIZE_VOCAB | LIVE | May 24 2026 |
| NN-PHI-4 | Every threat must have a path — fff_human_path always required | `nexus_analyzer.py` + `prompt_manager.py` fff_human_path field + `self_bias_gate.py` (threat-has-path check) | LIVE | May 31 2026 |
| NN-PHI-5 | Absence is intelligence — coverage gaps reported | `absence_detector.py` + `gni_keyword_history` + `gni_coverage_alerts` | LIVE | May 24 2026 |
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
| NN-PHI-5 | Absence detection — coverage gap reporting | COMPLETE May 24 2026 |
| GPVS | Human security track alongside SPY metric | S37 |
| Layer 4 | LLM spot-check for ambiguous article classification | S37 |
| About page | Update copy to reflect PHI-003 identity | S37 |
| Banner | Update from "rebuilding" to "PHI-003 live" | S37 |
| Self-bias semantic | Does GNI output use the OP-005/Cui Bono techniques it flags in sources? | IMPORTANT S41 |

## Self-Audit Layer (S40 -- BEGUN, NOT COMPLETE)

The fourth analyst (S39) named GNI's one genuine gap: GNI audits its sources
but nothing audits GNI itself. An anti-pretense instrument never itself
audited becomes the purest pretense. The self-bias gate answers this -- in
layers, only the first of which is built.

| Layer | What it checks | Status |
|---|---|---|
| Structural coherence | escalation must agree with sentiment/risk (NN-PHI-1); every threat has a path (NN-PHI-4) | LIVE -- `self_bias_gate.py`, daily 06:00 UTC, writes SELF_BIAS_FLAG / SELF_BIAS_AUDIT_CLEAN to tamper-evident audit_trail |
| Semantic self-audit | Does GNI's OWN output use the manipulation techniques (OP-005 framing, Cui Bono distortion) it flags in adversarial sources? | OPEN -- the heart of the fourth analyst's gap. Not yet built. |

Origin: the BEARISH 10/10 escalation latch (caught by a 16-year-old before
any analyst) was the live proof the gap was real. Structural layer shipped S40.

## Instructions for Next Philosophy Update

1. Open this file FIRST before any implementation
2. Review every row — mark any principle that the new philosophy changes
3. For each changed principle — identify the code location that implements it
4. Add new rows for any new non-negotiables
5. Mark implementation status as OPEN for anything not yet coded
6. Do not close the session until all OPEN items are either implemented or explicitly deferred with a session number
