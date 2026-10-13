# GNI FOUNDING PHILOSOPHY - S113 (frozen extract)

The rules GNI set for itself, copied verbatim from the two documents that founded them, so that the
claims harvest (`tools/gni_claims.py`) reads them as it reads the White Paper and the promise ledger
grades each one. Written at S112 (A + C, the operator's ruling after the guideline review), because the
ledger built from the White Paper and the pages alone held no row for the values GNI was founded on.

- `docs/GNI_Philosophy_Policy_Sharpened_S32.docx` (2026-05-17): Part 3.1 the sharpened core statement,
  Part 4 the non-negotiables NN-1..NN-8, Part 5 the principles NP-1..NP-5 (each principle's operative
  sentences).
- `docs/GNI_PHI003_Complete.docx` (S34, 2026-05-18..22): the purpose, Part 2 Freedom from Fear and the
  Teenager Standard, the non-negotiables NN-PHI-1..NN-PHI-7.
- `phi_compatibility_check.md` (repo root; S43, 2026-06-12), the mapping file GNI-L-011 names: NN-PHI-8, the
  Duty Clause, its Principle cell. Added at S113: the S112 extract read only the two documents above and
  missed it (a copying error, not a changed philosophy - `docs/GNI_PHILOSOPHY_S112.md` stays as it was).

The source column of the S32 table is not copied. Wording is the source's - a Teenager Standard question
and its standard are joined into one row, a closing full stop is added where the source's table cell had
none, and NP-1's opening word is capitalised; where a principle runs to a paragraph, the sentences that
state the rule are copied and the illustration is left in the source.
This file is frozen: a changed philosophy is a new document and a DECISION, not an edit here.

---

| rule | text |
|---|---|
| CORE | GNI is an intelligence system that earns trust through verifiability, improves through accountability, and protects its reasoning through integrity — at zero cost. |
| PURPOSE | GNI serves no government, no market, no ideology. It serves the human being who is trying to understand their world. |
| FREEDOM FROM FEAR | Freedom from Fear is the foundational standard against which all GNI outputs are measured. |
| TEENAGER STANDARD 1 | Can a teenager understand what is happening? The facts must be clear, not buried in jargon or market terminology. |
| TEENAGER STANDARD 2 | Can a teenager understand why it matters to people's lives? The human consequence must be explicit, not implied. |
| TEENAGER STANDARD 3 | Can a teenager understand what can be done about it? If analysis identifies a threat, it must also identify what understanding or action is possible. |
| TEENAGER STANDARD 4 | Does the content create fear without understanding? If yes → reject or reframe before publishing. |
| TEENAGER STANDARD 5 | Does the content divide people by identity? If yes → reject — this is a Sectarian Trap. |
| NN-1 Sacred Cron Is Inviolable | 02:00 + 02:30 UTC daily. No feature, quota, or emergency overrides it. Sacred=True always. |
| NN-2 Free First — Always | $0/month is a design principle. Paid upgrades require evidence + expected improvement + revert condition. No blind upgrades. |
| NN-3 One-Way Information Flow | Collection → Analysis → MAD → Verification. No stage reads downstream output. Adaptive pipeline must never inject past MAD verdicts into new collection. |
| NN-4 Verifiability Before Autonomy | Every intelligence output must be traceable to its source article. Autonomy without verifiability is automation pretending to be intelligence. |
| NN-5 Corrections Enforced in Code | Black Swan + Ostrich insights above confidence threshold are hard constraints. LLMs cannot be reliably instructed via prompts alone. |
| NN-6 Integrity Before Analysis | Language sanitization runs before every LLM call. Emotional amplification and loaded vocabulary stripped first. Injected emotion = contaminated debate. |
| NN-7 Separate Accounts Per Pipeline | Intelligence, MAD, and S2 analysis each on their own Groq account. Shared quota = pipeline starvation. |
| NN-8 Feedback Loop Must Be Real | If GPVS scores exist but source weights never update, the system is self-deceiving, not self-improving. Every philosophical claim about improvement must be verified with actual DB writes. |
| NN-PHI-1 | GNI serves the human being, not the market. All output is measured against the Teenager Standard, not against financial prediction accuracy. |
| NN-PHI-2 | All news directions are equal. GNI never filters by sentiment, never suppresses bearish news, never amplifies bullish news. Reality as it is. |
| NN-PHI-3 | Manipulation techniques are never in GNI output. The six rejection criteria apply not only to input articles but to GNI's own generated analysis and Telegram messages. |
| NN-PHI-4 | Every threat must have a path. GNI analysis that identifies a threat must also identify what humans can understand, do, or advocate for. No closed doors. |
| NN-PHI-5 | Absence is intelligence. What sources do not cover is as important as what they do cover. Coverage gaps are reported. |
| NN-PHI-6 | Adversarial sources are signal, not authority. RT, CGTN, Press TV and similar sources provide valuable intelligence about what narratives are being pushed — but they are never treated as news_only sources. |
| NN-PHI-7 | Data reset when philosophy resets. The data built under a previous philosophy cannot be used to calibrate a system under a new philosophy. Clean start required. |
| NN-PHI-8 | The Duty Clause (PHI-003 sentence two): seniors are the delivery channel of Freedom-from-Fear understanding to voting-age young adults. Method, never verdict. |
| NP-1 The Unprotected Canary Principle | The collector must NEVER be protected from injection or manipulation. GNI Stage 1 RSS collection must remain unfiltered. Injection detection at Stage 1b is correct. |
| NP-2 Absence Is Intelligence | When escalation is CRITICAL but no articles from the affected region appear — that absence is a signal, not a data gap. Zero articles from a CRITICAL region = coverage gap alert. |
| NP-3 Adversarial Sources as Signal | GNI must add 3-4 adversarial source canaries with explicit Tier A (state-sponsored) flag. Their selection frequency becomes a meta-signal: 'adversarial narrative push detected on topic X.' |
| NP-4 Pattern Match Bias Is the System's Biggest Enemy | Cross-run verdict injection (last 7 verdicts + confidence trend) into MAD pre-prompt makes the bias visible and correctable. |
| NP-5 Upgrade History Is Meta-Intelligence | A system that requires frequent prompt upgrades is under increasing narrative pressure. Log every upgrade with timestamp + reason. This log IS a signal. |
