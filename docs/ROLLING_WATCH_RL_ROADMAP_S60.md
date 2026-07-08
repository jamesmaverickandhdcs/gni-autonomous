# ROLLING WATCH + LEARNING ROADMAP — S60 DEEP ANALYSIS (2026-07-08)
Transferable. Feeds I4 (now GROUNDING+INTEGRITY WATCH), two new opportunity-cost checks,
and the RL/DL long-game. Perspective: senior G+T+F strategist, hidden-pattern/invisible-linking.
Constraint honored throughout: $0/month. Every item below runs on stdlib/numpy/sklearn/CPU
sentence-transformers inside GitHub Actions + Supabase pgvector. Zero GPU, zero paid API.

===============================================================================
PART 1 — THE 7-DAY ROLLING INTEGRITY WATCH (not_mad account, 14 crons of data)
===============================================================================
One daily script, one Telegram digest. Checks tiered by data-readiness.

TIER A — data exists TODAY, ship first (8 checks):
A1  Grounding/fabrication rate    grounding_hits per run (needs gate, in flight S60);
                                  arbitrator-level hit = instant alarm (Caucasus class).
A2  Verdict distribution drift    rolling verdict mix vs 30d baseline. Detects
                                  neutral-collapse (fake-neutral history: S46) AND
                                  sudden directional capture (cognitive-warfare tell).
A3  Confidence calibration        MAD confidence vs verified outcomes (debate_predictions
                                  now self-labels daily). Metric: Brier score, 7d window.
A4  Per-agent track record        accuracy by agent from debate_predictions outcomes.
                                  Feeds Part 3 item L3 (expert weighting).
A5  Solver estimate error         est vs real tokens trend (datapoints: 0.2%, +4.0%, +8.8%).
                                  Correlate with A6 — the open 429-churn question answers itself.
A6  429-churn pressure            rate-limit waits per run, trend. Leading indicator of
                                  quota architecture stress.
A7  MAD quality-score trend       13-flag composite + subscores (agents/consultants/arb),
                                  EWMA control chart; alarm on 2-sigma drop (regime-change
                                  detector — the S49 quality dip took manual eyes to spot).
A8  Terminal-failure + arb-consistency rate   mad_arb_failed frequency; arb_consistent flag
                                  rate. >1 terminal fail per 7d = structural alarm.

TIER B — needs one new column or small join (5 checks):
B1  Escalation-vs-market validation   escalation score vs realized SPY/GLD/USO move over
                                      matched horizon (GPVS-style, report-level).
B2  Pillar balance adherence          selected 22 vs 14/4/4 quota, drift over window.
B3  Source concentration              Herfindahl index on selection; one source >25% of
                                      picks in 7d = capture risk flag (PHI-001).
B4  Swan weak-signal anchoring        % runs where Swan cited a genuine score-0 article
                                      (flag exists in quality log; trend it).
B5  Injection/sanitize hit trend      stage-1b flags per run; a sustained rise = someone
                                      is probing the pipeline (Lens-grade signal).

TIER C — needs new collection, defer to after Part 2 ships (2 checks):
C1  Topic persistence half-life       how long selected topics survive in subsequent runs.
C2  Cross-project echo                GNI-selected topics vs Lens indicator hits (the two
                                      systems corroborating each other = highest-trust signal).

Verdict: 13 named checks before C-tier; 8 shippable immediately. The watch is one
script + one cron + one Telegram digest, growing check-by-check. Alarm philosophy
copied from W12-b: digest is INFO, red is reserved for A1-arbitrator hits, A8, and
2-sigma A7 breaks.

===============================================================================
PART 2 — THE TWO OPPORTUNITY-COST CHECKS (James's design, formalized)
===============================================================================
Named in RL language deliberately: these two checks ARE the reward signal + regret
signal that Part 3 learns from. Build them as measurement first; learning consumes later.

CHECK OC-A — SELECTION VALIDATION ("were the 22 marks right?")
For each selected article, score over the following 7 days:
  a. Persistence: does its topic/keyword cluster reappear in later runs' collected
     pool? (validates significance — real stories echo)
  b. Corroboration velocity: how many DISTINCT sources carry the topic within 48h?
     (single-source stories that never corroborate = weak marks, or plants)
  c. Escalation linkage: did the report containing it precede a CRITICAL/score
     move in the same direction? (B1 join)
  d. MAD uptake: did any agent actually CITE it in debate? (uncited selections =
     wasted context budget — feeds depth/count solver)
Output: per-article mark-quality score -> per-SOURCE and per-PILLAR aggregates ->
directly upgrades the GPVS source-weight update from verdict-quality-based to
selection-quality-based. Data: article trace tables + events (all exist).

CHECK OC-B — MISS DETECTION ("what did we fail to mark?") — the REGRET signal
For each REJECTED article (stage 1/2/3 rejects, all logged in the 304-article trace):
  a. Late-selection regret: same topic gets SELECTED in a later run (we were late
     by N runs — quantified earliness loss)
  b. Blowup regret: rejected topic's keyword enters emerging-keyword sensor or a
     later CRITICAL report within 7d (we rejected a precursor)
  c. External regret (C-tier): GDELT volume spike on a rejected topic (world decided
     it mattered; we didn't) — reuse Lens GDELT pacing discipline (LR rules exist)
Output: weekly regret list with WHICH STAGE rejected each miss -> tells you whether
relevance, dedup, or significance scoring is the leaky stage. This is the single
highest-value diagnostic GNI does not yet have.
Cognitive-warfare note: OC-B is also a DEFENSE check. An adversary shaping the
information environment WANTS your funnel to systematically ignore a slow-building
story. Regret tracking is how an automated pipeline notices its own blind spot
being farmed. This is PHI-003 applied to the machine itself: freedom from fear
includes freedom from engineered inattention.

===============================================================================
PART 3 — RL / DEEP LEARNING CATALOG (philosophy-aligned, $0-feasible)
===============================================================================
Strategic framing first. The long-game cognitive-warfare adversary does not inject
one fake story. They operate BELOW the weekly noise floor: shift baselines slowly,
poison source ecosystems gradually, farm the pipeline's habits (recency bias, source
trust inertia, keyword blind spots). Therefore two principles govern everything below:
  P-A: every learned weight must be AUDITABLE (no black box deciding what GNI reads
       — PHI-001 demands we can dig behind our own screen too)
  P-B: every check needs a SLOW twin — 7-day windows catch storms; 30/90-day drift
       charts catch campaigns. Ship 7d first, add slow twins cheaply (same code,
       wider window).

L1  CONTEXTUAL BANDIT — ARTICLE SELECTION (the flagship)
    What: Stage-4 ranking becomes a learning policy. Features: source, pillar,
    stage3 score, freshness, keyword novelty. Reward: OC-A mark-quality. Regret:
    OC-B misses. Algorithm: LinUCB or Thompson sampling — pure numpy, ~200 lines.
    Why it fits: GPVS source-weight updates are ALREADY a hand-rolled bandit;
    this formalizes it with exploration (deliberately sampling low-weight sources
    occasionally — which is ALSO the anti-capture defense: a farmed trust ranking
    cannot fully starve a source the explorer keeps sampling).
    Philosophy: PHI-002 (from the people — exploration keeps small voices sampled).

L2  CONFIDENCE CALIBRATION — ISOTONIC/PLATT
    What: map MAD raw confidence -> calibrated probability using debate_predictions
    verified outcomes. sklearn isotonic regression, retrain weekly, ~40 lines.
    Why: A3 will almost certainly show miscalibration (LLMs cluster 50-60%).
    A calibrated GNI can say "58% means 58%" — rare even in paid systems.

L3  EXPERT WEIGHTING — HEDGE / MULTIPLICATIVE WEIGHTS OVER AGENTS
    What: per-agent weights from A4 track records, fed INTO the arbitrator prompt
    as ground truth ("Swan 14d accuracy: 80%, Bear: 55%"). Online learning,
    exponential updates, ~30 lines. The arbitrator stops treating four voices
    as equal when the scoreboard says they are not.
    Caution: weights must DECAY (regime changes reset skill) and stay visible on
    the transparency page (P-A auditability).

L4  MISS CLASSIFIER — LEARNING FROM REGRET
    What: gradient-boosted classifier (sklearn, CPU) trained on OC-B regret set:
    features of rejected-then-important articles. Output: a "second-look" score
    that flags likely-regret rejections for a bonus review slot in selection.
    This is the funnel learning its own blind spots. Needs ~60-90 days of OC-B
    data first — REASON TO SHIP OC-B EARLY.

L5  NARRATIVE EMBEDDING LAYER — THE COGNITIVE-WARFARE DEFENSE CORE
    What: sentence-transformers (CPU, free in Actions) embed every selected +
    sampled-rejected article; store in Supabase pgvector (free tier includes it).
    Three detectors on top:
      L5a Narrative convergence: unrelated sources moving toward identical framing
          within a window = coordination signature (influence-op tell — Lens's
          mission appearing inside GNI's pipeline).
      L5b Source fingerprint drift: each source has a framing centroid; sudden
          centroid jump = editorial capture, ownership change, or compromise.
          (Media Watch Log Article 1 — Al Jazeera anchoring — is EXACTLY the
          manual version of this check.)
      L5c Semantic novelty: true novelty vs re-worded repetition — upgrades dedup
          from URL/keyword matching to meaning matching.
    Philosophy: this IS PHI-001 industrialized — dig behind the screen, at scale,
    against adversaries who count on no one watching the slow game.

L6  PROMPT EVOLUTION — BANDIT OVER PROMPT VARIANTS (RL without training an LLM)
    What: prompt_variants table already exists. Treat variants as bandit arms;
    reward = MAD quality composite + calibration + grounding-gate cleanliness.
    Selection pressure over prompts = evolution, no gradients, no fine-tuning.
    Timing: AFTER Aug-16 model migration settles (variants tuned to a dying model
    are wasted arms).

L7  TEMPORAL PATTERN DISCOVERY (Arc C, already queued as O6)
    What: motif mining / simple HMM over escalation-score + keyword + market
    sequences. The historical_correlations table (22 similar events, 96%
    directional) is the seed. Defer: LAST, as always planned — but note it
    consumes everything above as features.

L8  NLI CONTRADICTION GUARD (stretch)
    What: small CPU NLI model (e.g. DeBERTa-v3-small) checking verdict claims
    against cited article summaries — catches bias-laundering the grounding gate
    (entity-level) cannot (claim-level). Heavier; only after L5 proves the
    embedding infra.

===============================================================================
SEQUENCING (honest lean)
===============================================================================
NOW (S60-61):    Grounding gate shadow (in flight) -> Integrity Watch Tier A
                 (8 checks, one script) -> OC-A + OC-B measurement (no learning yet;
                 they must accumulate data BEFORE Aug 16 so the model swap gets a
                 before/after baseline — this is time-sensitive in a way nothing
                 else here is)
AUG 9 MARATHON:  model migration (unchanged scope + cliff-audit additions)
POST-CLIFF:      L2 calibration (cheapest, data will be ready) -> L1 bandit ->
                 L3 expert weights -> L5 embeddings -> L4 miss classifier
                 (regret data matured) -> L6 prompt evolution -> L7/L8
NEVER:           anything unauditable deciding what GNI reads or says. Weights on
                 the transparency page or they don't ship.

Bottom line count: 13 integrity checks + 2 opportunity-cost checks + 8 learning
systems = 23 named, costed, philosophy-mapped capabilities, all $0. The moat is
not any single one — it is that the verifier now labels data DAILY while
competitors' pipelines stay static. Time is the training set.
