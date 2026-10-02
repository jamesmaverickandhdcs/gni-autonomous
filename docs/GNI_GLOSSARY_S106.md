# GNI GLOSSARY - S106

**Live file = the highest session number.** Written at S106 (roadmap 3, row R3-1). The check
labelled `glossary` reads it: every abbreviation a live document or `docs/GNI_ORIGIN.md` uses
must appear under DEFINED, under NOT ABBREVIATIONS, or match a NAMESPACES pattern, and every
check in `tools/gni_rule_checks.py` must have a row under CHECKS. The check labelled
`origin citations` reads the SESSION INDEX. Section headings are parsed by exact text; a
renamed heading halts the detector rather than passing it.

Definitions follow ISO 704: they state what the thing IS, they do not define a term by
itself, and they do not define it by what it is not. The source column says where the term
is used or was ruled, so a reader can check the definition against the record.

**What the check cannot see (written down, not discovered later):** a token is a candidate
only when no part of it appears as a lowercase word anywhere in `docs/` prose. An
abbreviation spelled like an English word - MAD, AI, EU, SHA - is therefore invisible to the
check; those rows exist because they were written, not because the check forced them. Text
inside code spans and fenced blocks is not scanned. A DEFINED row nobody uses any more is not
detected.

## DEFINED

| term | definition | source |
|---|---|---|
| GNI | the autonomous geopolitical news intelligence system this repository builds and runs | every document |
| MAD | Multi-Agent Debate: the scheduled stage in which several agents argue a report and an arbitrator rules | `gni_mad.yml`; public methodology page |
| ARB-FIT | a marker string present in the log of a MAD debate run and absent from a grounding-watch run; the fallback way to tell the two apart when job data is absent | R-S84-4, amended S99 |
| GPVS | GNI Prediction Validation Standard: the verifier that scores each agent's directional predictions against later outcomes | public pages; STATE line L3 |
| BEV | bird's-eye view: a read-only survey of the real bytes taken before any edit | CONTRACT gate; ARCHITECTURE section 12 until S106 |
| LINEAGE-BEV | the gate that requires, before a proposal, a search of the past records for the design lineage of the thing being changed, reported as a `LINEAGE:` line | CONTRACT v7, S85 |
| LINEAGE | the required evidence line on every lettered proposal and every finding | CONTRACT v7 |
| Canary | an unprotected component whose failure is the signal | moved from ARCHITECTURE section 12 at S106 |
| GRAVEYARD | the section of the order holding falsified designs with the measurement that killed each, copied forward by bytes so they are never proposed again | DECISION S88-2 |
| Toil | manual work that scales with the system and produces no lasting value (SRE usage) | moved from ARCHITECTURE section 12 at S106 |
| Epistemic failure | a failure in which the system works but the record of it is wrong; contrasted with a runtime failure, in which something stops working | ARCHITECTURE section 8.1 |
| rho | findings opened divided by items closed, per session | ARCHITECTURE section 11 |
| Z | the share of CHECKABLE markers in the rules register that read yes; the macro map's vision-to-executable axis | `GNI_MACRO_MAP_S<N>.md` |
| COVERAGE | the share of claims whose status a check derives; reserved by roadmap 3 for row R3-3 | ROADMAP 3 |
| LOAD CHECK | the five lines a session echoes at its open to prove it loaded the right state | protocol PART B |
| cert | a measurement that certifies a change did what it claimed, built so that it can fail (R-S90-1) | GNI_RULES |
| fixture family | one synthetic repository in `tools/gni_rule_checks_fixture.py` with the exit code the detector must return on it | protocol PART C step 9a |
| control probe | an instrument's test of its own expectations on perturbed real bytes before it reports (R-S93-1) | `tools/gni_rule_checks.py` |
| Smart Office | the direction GNI took at S92: make the system's state visible from outside instead of rewriting the code | DECISION S92-3; `docs/GNI_ORIGIN.md` |
| WHACK-A-MOLE | James's name for the state, until S92, in which every fix surfaced more errors | `docs/GNI_ORIGIN.md` step 5 |
| SUBPAGE-IC | the sub-page integrity check: whether each Web App sub-page displays what the backend computed; ran five months without a completion test | ARCHITECTURE defect D4 |
| DET-DEAD | the defect class of a detector that exists in the code and is imported by nothing | ARCHITECTURE; ORDER |
| DEGRADE-SILENT | the defect class of a component that degrades to doing zero work while reporting success | ARCHITECTURE |
| SLO | service level objective: a stated target for a service level indicator | ARCHITECTURE section 10 |
| SLI | service level indicator: a measured quantity of service behaviour | ARCHITECTURE section 10 |
| SLO-CFG | the machine-read configuration lines of ARCHITECTURE section 10.3 that check C7 parses | ARCHITECTURE section 10.3 |
| SLM | service level management, the ITIL practice for stated service levels and external dependencies | ARCHITECTURE section 4 |
| SRE | site reliability engineering; the discipline ARCHITECTURE section 4 assigns to reliability concerns | ARCHITECTURE section 4 |
| ITIL | the IT service management framework whose SLM practice ARCHITECTURE section 4 uses | ARCHITECTURE section 4 |
| PM | project management; the discipline ARCHITECTURE section 4 assigns to the queue (scope baseline, definition of done, change control) | ARCHITECTURE section 4 |
| SWOT | strengths, weaknesses, opportunities, threats: the analysis run before an architectural proposal | CONTRACT |
| COR | corrective: the ISO/IEC 14764 class of an order item where something is broken | DECISION S92-4 |
| ADA | adaptive: the ISO/IEC 14764 class of an order item where the world moved | DECISION S92-4 |
| WIP | work in progress; CONTRACT v11 caps the order's open items | CONTRACT v11, R-S105-7 |
| SSOT | single source of truth: each fact lives in one file | protocol PART A |
| ICD | Intelligence Community Directive; ICD 203 sets the analytic standards that DoD line D2 implements | ORDER, definition of done |
| EU | European Union; named for Article 50(4) of its AI Act, which DoD line D4 implements | ORDER, definition of done |
| AI | artificial intelligence | ORDER; public disclosure |
| XAI | explainable AI: the audit trail of rejected articles kept visible with reasons | DECISION S89-4 |
| LLM | large language model | ARCHITECTURE; GNI_RULES |
| TPD | tokens per day, the provider's daily token budget, which refills continuously | R-S81-8 |
| CI | continuous integration: the push-triggered workflow `gni_ci_harness.yml` | ARCHITECTURE; HANDOFF |
| CD | continuous delivery | ARCHITECTURE section 7 |
| GHA | GitHub Actions, the scheduler that runs every workflow | GNI_RULES |
| PAT | personal access token | GNI_RULES |
| CLI | command-line interface | ARCHITECTURE; GNI_RULES |
| API | application programming interface; in this repo usually a route under `src/app/api/` | ARCHITECTURE; GNI_RULES |
| UI | user interface | GNI_RULES |
| RSC | React Server Components: the serialised payload in which a page's markup appears a second time | HANDOFF S105 |
| HTML | the markup language of the public pages | GNI_RULES; HANDOFF |
| HTTP | the protocol the public pages and APIs are served over | GNI_RULES |
| TLS | the transport security layer under HTTPS | GNI_RULES |
| JSON | the data format of snapshots and API bodies | GNI_RULES; HANDOFF |
| YAML | the format of the workflow files | GNI_RULES |
| SQL | the query language of the Supabase database | CONTRACT; GNI_RULES |
| DB | the Supabase Postgres database | GNI_RULES |
| UTC | coordinated universal time; every published clock is stated in it | CONTRACT; HANDOFF |
| SHA | the git commit hash | ARCHITECTURE |
| EOL | end of line; a published hash is computed on EOL-normalised bytes (R-S98-3) | GNI_RULES |
| EOL-INVARIANT | a value that does not change when line endings change | GNI_RULES |
| CRLF | the Windows line ending, carriage return plus line feed | GNI_RULES |
| CR | the carriage-return byte | GNI_RULES |
| LF | the line-feed byte, the Unix line ending | GNI_RULES |
| BOM | byte-order mark; six files under `ai_engine/` carry one | `tools/gni_rule_checks.py` |
| MB | megabyte | GNI_RULES |
| FIFO | first in, first out | ORDER |
| MSYS | the POSIX layer under Git Bash on Windows, which translates path-like arguments | R-S87-5 |
| MINGW64 | the 64-bit Git Bash environment on Windows the operator works in | ARCHITECTURE |
| IEEE | the standards body; IEEE 828 is cited for configuration management | ARCHITECTURE; ORDER |
| IEEE754 | the floating-point standard | ARCHITECTURE |
| DEP0040 | the Node.js deprecation notice for the `punycode` module, which a Node-20 sweep miscounted as a Node-20 site | GNI_RULES |
| CC | Creative Commons; with BY-SA, the licence the arc42 template is used under | ARCHITECTURE |
| BY-SA | attribution, share-alike: the Creative Commons terms of the arc42 template | ARCHITECTURE |
| GNI-R | prefix of the original rule namespace `GNI-R-###` | GNI_RULES |
| GNI-L | prefix of GNI's own lessons-learned namespace `GNI-L-###` | GNI_RULES |
| R-S83 | the session-rule prefix of S83, cited where S83 amended a rule instead of minting one | GNI_RULES |
| PHI | philosophy: the founding principles the `NN-PHI-#` rules protect | ORDER; GNI_RULES |
| PHI-003 | the philosophy document whose non-negotiables are quoted in the rules register | GNI_RULES |
| K-WATCH | the watch built to observe keyword match-count deflation before a selection change lands | GNI_RULES |
| V-W13 | the incident in which code, API and database were clean and a cached bundle was the bug | GNI_RULES |
| GRAPH-S2 | the false alarm raised before a full call site was read | GNI_RULES |
| TRANS-COUNT | the miscount in which one flag alone reported the default instead of the funnel | GNI_RULES |
| PHISH-HW | the account-security review item (OAuth, GitHub Apps, security log) | GNI_RULES |

## NOT ABBREVIATIONS

| word | why it is in capitals |
|---|---|
| ACCEPTING | emphasis |
| ADMITS | emphasis |
| ANALYSE | emphasis |
| ANALYTICAL | emphasis; the protocol's ANALYTICAL STANCE heading |
| ATTACHES | emphasis |
| BOLD-PREFIXED | emphasis |
| CONTRADICTED | emphasis |
| EXTENT | emphasis |
| GUARDING | emphasis |
| IMAGINED | emphasis |
| INSTANTIATION | emphasis; the protocol's instantiation rule |
| JAMES | a name, the operator's |
| MIDDLE | emphasis |
| MODERATE | emphasis |
| NON-NEGOTIABLES | heading of the PHI-003 quick reference |
| NON-TEST | emphasis |
| NORMALIZER | emphasis |
| ONE-SHOT | emphasis |
| ORGANISED | emphasis |
| PARTLY | a status word in the definition-of-done table |
| RECLAIM | emphasis |
| RHYTHM | emphasis |
| ROUND-ROBIN | a graveyard entry's name |
| SEPARATOR | emphasis |
| SERVER | emphasis |
| SYNONYMS | emphasis |
| UNCONDITIONALLY | emphasis |
| WEAKER | emphasis |
| INTRODUCTION | an arc42 section heading |
| GOALS | an arc42 section heading |
| REQUIREMENTS | an arc42 section heading |
| SOLUTION | an arc42 section heading |
| CROSSCUTTING | an arc42 section heading |
| TECHNICAL | an arc42 section heading |
| SMART | first word of Smart Office, defined above |
| OFFICE | second word of Smart Office, defined above |

## NAMESPACES

A token that matches one of these patterns in full is a member of that series. Two letters
name two series each; the row says which document each meaning lives in.

| pattern | meaning |
|---|---|
| `S\d+` | a session number |
| `S\d+-S\d+` | a range of sessions, both ends included |
| `S\d+-\d+` | a ruling of that session, written DECISION S105-6 |
| `R-S\d+-\d+` | a rule minted at that session (GNI_RULES) |
| `GNI-R-\d+` | a rule from the original register |
| `GNI-L-\d+` | a GNI lesson learned |
| `NN-PHI-\d+` | a non-negotiable of the founding philosophy |
| `C\d+` | a check in `tools/gni_rule_checks.py`; see CHECKS |
| `R3-\d+` | a row of roadmap 3 (ARCHITECTURE, ROADMAP 3) |
| `D\d+` | TWO SERIES: in the ORDER, a line of the definition of done (D1-D4); in the ARCHITECTURE, a defect homed at S92 (D1-D7). The letter is shared, the meanings are not |
| `D\d+-D\d+` | a range of either D series |
| `L\d+` | TWO SERIES: in a HANDOFF STATE section, a GNI layer (L1 pipeline, L2 MAD, L3 GPVS, L4 quota, L5 public); inside a rule's evidence, a source line number (L299) |
| `L\d+-L\d+` | a range of layers |
| `M\d+` | an amendment item in the CONTRACT version log |
| `R\d+` | a MAD debate round (R1 opening, R3 final position) |
| `F\d+` | a flag of the S69 census |
| `W\d+` | a weakness in the S92 AI-agent SWOT |
| `U\d+` | the work item named as the case behind the rule that a verify-grep on an unpatched file proves nothing |
| `B\d+` | a build item of the S40 plan |
| `P\d+` | a numbered probe of a session's instrument test |
| `SLO-\d+` | a numbered service level objective (ARCHITECTURE section 10) |
| `SLI-\d+` | a numbered service level indicator (ARCHITECTURE section 10) |

## SESSION INDEX

Sessions with no record under `docs/`. A session listed here as CHAT-ONLY was confirmed
from its chat transcript; the record is the chat, which is not in the repository.

**HOW TO OPEN ONE, FIRST TRY.** Both rows below share one chat TITLE, so the title alone finds
the wrong session half the time. Use the URL in the `find it` column; when the URL cannot be
opened, run the `conversation_search` query printed beside it - at S106 it returned both chats
among its first two hits, S53 first. Search by CONTENT words, never by session number alone: chat
titles carry no session number, and S106 found S53 only through the work it did.

| session | record | find it | status |
|---|---|---|---|
| S52 | chat "Project status review and next steps", closed 2026-06-28: the 14-commit truthfulness pass; at its end the seven-layer design was written and layer 1 (NFKC) shipped | https://claude.ai/chat/10df0efd-9c61-42ce-9080-24031f856ff5 - query `GNI S53 7-layer defense` (S52 wrote the design FOR S53) | CHAT-ONLY |
| S53 | chat "Project status review and next steps", 2026-06-28 to 2026-06-30: dedup fix, layer 6 guardian, the seven-layer UI sync, the MAD fabrication finding | https://claude.ai/chat/73cd999a-4e9b-41bc-960c-5d7cc700bfee - query `GNI S53 7-layer defense` | CHAT-ONLY |

## CHECKS

One row per check in `tools/gni_rule_checks.py`. The check labelled `glossary` refuses a
CHECKS tuple entry without a row here, so this list cannot fall behind the code.

| check | what it enforces |
|---|---|
| C1 | every rule id cited by a live document is registered or manifested (R-S90-2) |
| C2 | workflow and trigger counts in ARCHITECTURE 7.1 equal the workflow files (R-S91-5) |
| C3 | no rule id is defined twice in the register (R-S74-1) |
| C4 | no direct `createClient` under `src/app/api/`; no-store clients only (R-S62-3) |
| C5 | no check holds a hand-written expected integer, and each proves its input non-empty (R-S81-5) |
| C6 | every INPUT line of the macro map matches the live file it names (R-S95-4) |
| C7 | the published freshness bound is derived from the run history, in one regime (SLO-2, SLO-3) |
| C8 | the three GENERATED sections of ARCHITECTURE match their inputs (R-S104-1) |
| C9 | every abbreviation a live document or ORIGIN uses is in this glossary (R3-1) |
| C10 | every session ORIGIN cites has a record, and ORIGIN cites no commit hash (R3-1) |
| C11 | no page formats an escalation score itself; `src/lib/escalation.ts` shows it with its uncapped magnitude (DoD D2) |

## OWED - named as metrics by the roadmap 3 specification, defined nowhere in the record

- **lambda** - the specification cites "~6.5 per session" at S102, S103 and S104 with no
  definition and no command. Owed before R3-4.
- **mu** - listed among the metrics in the specification's glossary plan; no definition and
  no use anywhere in `docs/`.
