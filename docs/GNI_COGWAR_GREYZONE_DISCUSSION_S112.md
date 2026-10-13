# COGNITIVE WARFARE WITH MULTI-MODEL GREY ZONE TACTICS — S112 DISCUSSION RECORD

**Session:** GNI S112 (2026-10-12 .. 2026-10-13). **Kind:** discussion record, not a ruling. Nothing
here is a DECISION except where a DECISION id is named; the one ruling taken in this thread is
DECISION S112-6 (NN-3: quality score no longer feeds source weights, `QUALITY_FEEDS_SOURCE_WEIGHTS =
False`, shipped by runner S112_R12), recorded in the order at the S112 close.

**Why this file:** the operator asked that everything discussed on this subject in S112 be kept in
one file, because the thread is the input to the long-shelved adversarial-source / "AI psychological
warfare framework" deep-work session (promised at S34-S35, never held).

**Provenance, per section — read this before quoting anything below:**

| section | provenance |
|---|---|
| 1 Questions | the operator's questions, in order; the last one quoted from the session record, with cuts marked `…` |
| 2 Lifecycle analysis | **RECONSTRUCTED.** The full reply was lost when the conversation was compacted; rebuilt from the session summary, which kept its structure, its sources and its figures. Wording is new; claims and figures are the summary's |
| 3 The five-question discussion | **VERBATIM**, copied from the session transcript (assistant reply of 2026-10-13); its headings are demoted one level and the partner project is named by its pseudonym, Partner B (the S105 identity separation); nothing else changed |
| 4 Corrections owed | written at save time from the bytes read in section 3's search |
| 5 Proposed constraints / open items | proposals, not rulings |
| 6 Sources | links read in S112 |

---

## 1. THE QUESTIONS ASKED (S112, in order)

1. Adversarial source: why "no adversarial source" (two rules, NN-PHI-6 and NP-3); why no gate on
   "fear without understanding"; does NN-3's "no stage reads downstream output" cover source weights?
2. Is "Cognitive Warfare using Grey Zone Tactics" the most important blockage on the way to Freedom
   from Fear?
3. Did we discuss this need before? Search the records. NN-3: "the choice is your call."
4. How is cognitive warfare with grey-zone tactics used and steered in geopolitics — initiation,
   framing, capture, relay, how people end up inside an echo chamber, how they drift away from
   critical thinking — given that some people hold that Freedom from Fear cannot be reached without
   understanding these?
5. (2026-10-13) "AI psychological warfare framework ဆိုတာ Cognitive Warfare using with Multi Models Grey
   Zone Tactics နဲ့ ဘာတွေတူ ဘာတွေကွာသလဲ … အဲဒါနဲ့ သက်ဆိုင်တာတွေ ငါတို့ ဆွေးနွေးခဲ့ဖူးလား … သတင်းအားလုံးကို
   မယုံတော့တာ ဆိုတာက Facts က ဖြစ်တာလား အီမိုကူးစက်ပြီး ဖီလင်ကဖြစ်တာလား … 'ရန်သူရဲ့ cognitive warfare' လို့
   label ကပ်ပြီး ကြောက်ရွံ့အောင် လုပ်ရင် — ဒီစကားမှာ ရန်သူဆိုတာ ဘယ်သူလဲ … Understanding ဆိုတာ ရုပ်ပိုင်းဆိုင်ရာ
   လုံခြုံမှုနဲ့ path မရှိလည်း ဖြစ်တည်လာနိုင်တယ်လို့ … ဆိုလိုတာလား … ဒါလေးတွေ ဆွေးနွေးပြီးမှ ဆက်လုပ်ကြမယ်"

---

## 2. LIFECYCLE ANALYSIS (RECONSTRUCTED — see provenance)

### 2.1 Answers to questions 1-3, as given

- **Adversarial source.** Two founding rules call for state-sponsored sources as *signal, not
  authority*: NN-PHI-6 (PHI-003) and NP-3 (S32: 3-4 Tier A canaries, selection frequency as a
  meta-signal). No such source is collected. The operator stopped the RT/CGTN/Press TV proposal on
  2026-05-18 (S34): a democracy-score frame was too blunt for AI-generated psychological warfare, and
  a source-selection framework is owed first. *(Correction, section 4: the handling side — the
  `_REVIEW_ONLY_SOURCES` classifier and the review_only path — is built; only collection is shelved.)*
- **Fear without understanding.** Teenager Standard 4 ("reject or reframe before publishing") had,
  as stated in this thread, no gate on GNI's own output. *(Correction, section 4: the escalation
  number is guarded by the PHI-003 gate in escalation_scorer.py and by self_bias_gate.py; the text
  is not.)*
- **NN-3 and source weights.** The quality score is GNI grading its own report; letting it move the
  weights the funnel selects by is a self-confirming loop. Ruled (the operator: "your call"):
  **DECISION S112-6 = A** — source weights learn from verified market outcomes only (W-14, NN-8);
  the quality-score channel is switched off by a named constant, shipped in S112_R12.
- **Is it the most important blockage?** Agreed with caveats: cognitive warfare with grey-zone
  tactics is the main *manufactured* obstruction to Freedom from Fear, because it manufactures
  exactly what PHI-003 rejects — fear without a path, and division by identity. It is not the only
  obstruction: real physical danger, poverty and closed information environments block it too, and
  understanding the techniques is necessary but not sufficient (taken up again in section 3, Q5).

### 2.2 Definitions used

- **Cognitive warfare** (NATO ACT): the fight over cognition itself; the brain is "both the target and
  the weapon"; aims at "attacking and degrading rationality"; military and non-military activity
  synchronised across the competition spectrum.
- **Grey zone:** coercion kept below the threshold of open war, built on deniability and ambiguity, so
  that the target cannot name the attack clearly enough to answer it.
- **DISARM** (the open framework for disinformation TTPs): phases Plan → Prepare → Execute → Assess.
- **"Firehose of Falsehood"** (RAND): high volume, many channels, rapid, repetitive, no commitment to
  consistency.

### 2.3 Why states use it (strategic rationale)

Cheap, deniable, below the threshold that triggers a military or legal answer, and aimed at the
decision rather than the territory. It rides wounds that already exist in the target society, so the
attacker supplies amplification, not the conflict.

### 2.4 Documented cases (more than one state, on purpose — symmetric scrutiny, PHI-002)

| case | actor (as attributed by the source) | what the record shows |
|---|---|---|
| Doppelganger | Russia-linked; the EU sanctioned SDA and Struktura | cloned news sites and fake articles under real outlets' look (EU DisinfoLab) |
| Spamouflage | China-linked | 7,700+ accounts on 50+ platforms with "scant engagement" — large, persistent, mostly low reach |
| "Unheard Voice" | pro-Western covert operations | the same techniques used by the other side; scrutiny that skips it is a label (section 3, Q4) |
| Myanmar, Aug 2018 | Tatmadaw | Facebook removed 52 Pages followed by ~12M people and banned Min Aung Hlaing — a domestic military information operation |

### 2.5 The lifecycle (stages mapped to DISARM)

| # | stage | what happens | mechanism and evidence | DISARM |
|---|---|---|---|---|
| 1 | Initiation | choose an existing fault line (identity, grievance, fear) and an objective | the attacker rarely invents the conflict; it finds one | Plan |
| 2 | Framing | build the narrative: who is to blame, what to fear | out-group words raise sharing odds (Rathje 2021: +35-57% in news media accounts); a negative word raises click-through (Robertson 2023: +2.3%; fear words lower clicks, sadness raises them) | Prepare |
| 3 | Capture | win attention and make the frame feel true | repetition makes a claim feel true even against prior knowledge (Fazio 2015, illusory truth) | Execute |
| 4 | Relay | pass it on through many hands: state media, proxies, cloned sites, bots, influencers, unwitting citizens | Doppelganger's clones; the firehose's many channels; most reach comes from real people re-sharing | Execute |
| 5 | Echo chamber | the frame circulates inside a closed group that hears itself | across >100M pieces of content, homophilic clusters; Facebook more segregated than Reddit (Cinelli 2021) — platform design matters | Execute |
| 6 | Distance from critical thinking | outside sources become suspect, belief fuses with identity, fatigue sets in | the end state is not belief in the lie but the shrug — "nothing can be known" — or identity-locked certainty | (effect) |
| — | Assess | the operator measures and adapts | DISARM's fourth phase; Spamouflage shows that persistence continues even when reach is low | Assess |

### 2.6 Three causal insights

1. **Ambiguity is the weapon.** The grey zone's deniability and the firehose's contradictions push
   people towards distrusting *all* news — which serves whoever is loudest (developed in section 3,
   Q3).
2. **Individual operations are weak; they ride existing chambers.** Spamouflage's scant engagement is
   the rule, not the exception. Danger comes when an operation finds a chamber already built by
   domestic polarisation and engagement-driven platforms.
3. **The stages chain.** Breaking any one link (framing recognised, relay not done, chamber exited)
   weakens the rest. That is why technique-level understanding (prebunking) is the defence named in
   the literature — though its lab evidence is contested (section 4, item 6).

### 2.7 Understanding is necessary, not sufficient

Freedom from Fear needs people to understand the *techniques* (not to memorise a list of actors);
it also needs safety and a path (worked through in section 3, Q5).

### 2.8 GNI mapping (as stated in the thread, with the save-time corrections marked)

| stage | GNI today | needed |
|---|---|---|
| Initiation / framing at the source | 69 injection patterns, SANITIZE_VOCAB, sentiment-free selection | behaviour-based source framework (the shelved S34/S35 work; U-2 A/B unanswered) |
| Relay — first-seen provenance | none | which outlet carried a narrative first, and who copied it |
| Relay — selection capture | **`_check_source_dominance` in self_bias_gate.py: one source > 35% of the latest run's selected set → SELF_BIAS_FLAG** (the thread said "needed"; corrected) | the S35 audit's consecutive-day version (> 5 days in the top 11) |
| GNI's own output | structural layer of self_bias_gate (escalation coherence, threat-has-path, required fields, flatline) | semantic self-audit — OPEN since S41; Roadmap 5 R5-2/R5-4 |
| Reader | fff_human_path in every report | prebunking in output: name one technique per report (NN-PHI-8's planned micro-lesson) |

Options offered at the end of the reply: **A** the deep-work session (lean), **B** a prebunking row in
Roadmap 5, **C** a Roadmap 6. Not yet ruled.

---

## 3. THE FIVE-QUESTION DISCUSSION (VERBATIM, 2026-10-13)

ဆွေးနွေးချက် ၅ ခုကို အစဉ်လိုက် ဖြေပါမယ်။ မှတ်တမ်းဟောင်းတွေ ပြန်ရှာရင်း ကျွန်တော့်ဘက်က အမှား ၅ ခု တွေ့တယ်။ အဲဒါကို အမှတ် ၂ မှာ အရင်ပြောပါမယ်၊ ဆွေးနွေးချက်ရဲ့ အဖြေအချို့ကို ပြောင်းစေလို့ပါ။

---

### ၁။ "AI psychological warfare framework" နဲ့ "Cognitive Warfare using Multi-Model Grey Zone Tactics"

**အဖြေ:** နှစ်ခုက တစ်ခုလုံးနဲ့ အစိတ်အပိုင်း ဆက်နွယ်မှုပါ။ AI psychological warfare က multi-model kit ထဲက လက်နက် တစ်ခု ဖြစ်ပါတယ်။ ဒါပေမဲ့ ကျွန်တော်တို့ မှတ်တမ်းထဲမှာ ဒီစကားလုံး နှစ်ခုရဲ့ အလုပ်က မတူပါဘူး —

- **"AI psychological warfare framework"**:
  - S34 (2026-05-18) မှာ သူငယ်ချင်း သုံးခဲ့တဲ့ စကားလုံးပါ။ S35 audit ထဲမှာလည်း "Dedicated session for AI psychological warfare framework" လို့ ပါတယ်။
  - ဒါက **ကာကွယ်ရေး framework** ပါ။ AI ထုတ်ထားတဲ့ content တွေ၊ ခြယ်လှယ်ထားတဲ့ summary တွေ ရှိနေတဲ့ ကမ္ဘာမှာ GNI က source ကို ဘယ်လို ရွေးမလဲ၊ ဘယ်လို ဖတ်မလဲ ဆိုတာ။ ပစ်မှတ်က GNI ကိုယ်တိုင်ပါ။
- **"Cognitive warfare … multi-model grey zone"**:
  - ဒါက geopolitics ထဲမှာ ဖြစ်နေတဲ့ **ခြိမ်းခြောက်မှု ဖြစ်စဉ်** ပါ။
  - "Multi-model" ကို ကျွန်တော် သုံးမျိုး ဖတ်ထားပါတယ်:
    - (က) multi-domain — သတင်း + ဥပဒေ + စီးပွားရေး + ရုပ်ပိုင်းဆိုင်ရာ လုပ်ရပ်။ ဥပမာ Three Warfares။
    - (ခ) multi-channel — state media + proxy + bot + influencer + AI-generated content။
    - (ဂ) multi-narrative — ဆန့်ကျင်ဘက် version တွေကို တပြိုင်နက် လွှတ်တာ (firehose)။
  - "AI model အများ" ကို တိုက်ရိုက် ဆိုလိုတာဆိုရင် ပြောပါ၊ ပြင်ပါမယ်။

2026-06-22 မှတ်တမ်းမှာ သူငယ်ချင်း သင်ပေးခဲ့တာ ရှိတယ်: "ဆိုက်ဝါး" = ရေရှည် psychological warfare။ အဲဒီမှာ psych warfare (စိတ်ခံစားမှု/စိတ်ဓာတ်ကို ပစ်မှတ်ထား) နဲ့ cognitive warfare (မြင်ပုံ၊ တွေးပုံ၊ ဆုံးဖြတ်ပုံကို ပစ်မှတ်ထား) ကို ခွဲခဲ့ကြတယ်။

| ရှုထောင့် | AI psychological warfare | Cognitive warfare (multi-model grey zone) |
|---|---|---|
| ပစ်မှတ် | ကြောက်စိတ်၊ စိတ်ဓာတ် | တွေးပုံ၊ ယုံကြည်ပုံ၊ ဆုံးဖြတ်ပုံ။ NATO ACT: "attacking and degrading rationality"; ဦးနှောက်က "both the target and the weapon" |
| နယ်ပယ် | သတင်း/content | သတင်း + ဥပဒေ + စီးပွား + ရုပ်ပိုင်းလုပ်ရပ် (ရုပ်ပိုင်း ဖြစ်ရပ်က narrative ရဲ့ ချိတ်ဖြစ်လာ) |
| AI ရဲ့ နေရာ | content ထုတ်သူ (အတု ဆောင်းပါး၊ summary၊ persona) | ကိရိယာ အများထဲက တစ်ခု — လက်နက်က **ညှိနှိုင်းမှု** |
| တာဝန်ခံ | မကြာခဏ သိနိုင် | တမင် ငြင်းနိုင်အောင် (deniable)၊ စစ်ပွဲ threshold အောက်မှာ |
| အချိန် | campaign (ဆိုက်ဝါးဆိုရင် ရေရှည်) | အမြဲတမ်း — "ငြိမ်းချမ်းချိန်" မရှိ |
| အောင်မြင်မှုရဲ့ ပုံ | စိတ်ဓာတ်ကျ၊ ကြောက် | ယုံကြည်မှု ပြို၊ ကွဲ၊ ဆုံးဖြတ်ချိန်မှာ လှုပ်မရ |

**တူတာ:**
- နှစ်ခုလုံး "fear without path" ကို သုံးတယ်။
- ရှိပြီးသား အနာကို အသုံးချတယ်။
- AI နဲ့ ချဲ့ထွင်တယ်။
- **မှားတဲ့ fact ထက် frame ကို ပိုသုံးတယ်။**

သူငယ်ချင်းရဲ့ S34 သက်သေ ("author က summary ကို ခြယ်လှယ်ပုံ") က နှစ်ခုဆုံတဲ့ နေရာ အတိအကျပါ။ Summary ဆိုတာ မှန်တဲ့ fact တစ်ခုကို frame ပေးလိုက်တဲ့ အချက် ဖြစ်လို့ပါ။

**GNI အတွက် အရေးကြီးဆုံး:** GNI ကိုယ်တိုင်က AI summarizer ပါ။ ဒါကြောင့် summary ခြယ်လှယ်ပုံ သက်သေက ပြင်ပ source တွေအပေါ်မှာသာ မဟုတ်ဘဲ GNI ရဲ့ LLM အပေါ်မှာပါ သက်ရောက်တယ်။ phi_compatibility_check.md ထဲမှာ "Self-bias semantic" က S41 ကတည်းက OPEN ဖြစ်နေတာ ဒီအတွက်ပါ။

---

### ၂။ မှတ်တမ်းဟောင်းတွေ — ဆွေးနွေးခဲ့ဖူးလား

ဆွေးနွေးခဲ့ဖူးပါတယ်၊ ပထမနေ့ကတည်းကပါ —

| ရက် | chat | ပါတာ |
|---|---|---|
| 2026-03-03 | 6a8a6408 | project ရဲ့ ပထမဆုံး သီအိုရီ "Techno-Geopolitics and **Cognitive Warfare** in the NAVI World" — echo chamber, Sectarian Trap။ GNI ဟာ cognitive warfare ကို ပထမနေ့ကတည်းက ရည်မှန်းခဲ့တာပါ |
| 2026-03-20 | 4df9d2de | embedding approach က keyword မပါဘဲ "grey zone warfare" ကို ဖမ်းနိုင်တယ် |
| 2026-04 | Partner B (0f309bea, 54909ac0, e695276e) | "Cold War playbooks with AI amplification"; "manufacture enemy → threat → consensus → act"; "information warfare → reality warfare" |
| 2026-05-18/21 | 7cb84650 (S34) | RT/CGTN ကို ရပ်ခဲ့၊ "AI generated psychological warfare is coming"၊ S34-2 shelved; audit: Semantic Injection UNDEFENDED, GPVS weight manipulation; S35 dedicated session ကတိ |
| 2026-05-22 | 704a7eab (S35) | U-2 A/B မေးခွန်း မဖြေရသေး |
| 2026-05-26 | 2da5f0db, b69e6faa | သူငယ်ချင်း ၃ ယောက် review: "lens ကိုယ်တိုင် pretense ဖြစ်သွားမယ့် risk" → self-bias gate ကို အဆိုပြုခဲ့ |
| 2026-06-12/15 | 5d98d101 (S43) | cognitive warfare အလွှာ ၄ ခု (flooding, division, trust demolition, decision capture)၊ **autoimmune response**၊ "name the mechanism, never the demon"၊ Tatmadaw 2018 Facebook op; **NN-PHI-8 Duty Clause** ကို commit လုပ်ခဲ့ |
| 2026-06-22 | 7a7c241f | Cognitive Warfare ဘာသာပြန်၊ ဆိုက်ဝါး၊ psych ≠ cognitive |

**မတွေ့တာ:** ကတိပေးခဲ့တဲ့ deep-work session ကိုယ်တိုင် တစ်ခါမှ မကျင်းပရသေးပါဘူး။

**ရှာရင်း တွေ့ခဲ့တဲ့ ကျွန်တော့် အမှားတွေ (WRONG):**
1. **R11 philosophy extract မှာ NN-PHI-8 ကျန်ခဲ့တယ်။**
   - NN-PHI-8 ကို phi_compatibility_check.md (S43, 2026-06-12, OPEN) မှာ မှတ်ထားတယ်။
   - ကျွန်တော် docx ၂ ခုပဲ ဖတ်ခဲ့ပြီး repo ရဲ့ ကိုယ်ပိုင် mapping file (GNI-L-011) ကို မဖတ်ခဲ့ပါ။ Rule ၂၉ ခု ဖြစ်ရမှာ ၂၈ ခုပဲ ရှိနေတယ်။
2. **CLM-1112 (T4 fear without understanding) ကို NOT BUILT လို့ အဆင့်သတ်မှတ်တာ မှားတယ်။**
   - escalation_scorer.py မှာ "PHI-003 gate" ရှိတယ်: GNI ရဲ့ ကိုယ်ပိုင် read က calm ဖြစ်ပြီး critical combo မရှိရင် escalation ကို 5.0 မှာ ဖြတ်တယ်။
   - self_bias_gate.py (gni_selfbias.yml, နေ့စဉ် 06:00 UTC) ကလည်း escalation နဲ့ sentiment ကိုက်/မကိုက် စစ်တယ်။
   - **ဂဏန်းကို စောင့်ထားတယ်၊ စာသားကိုတော့ မစောင့်ပါ** → PARTIAL ဖြစ်ရမယ်။
3. **CLM-1111/1125 note မှားတယ်။**
   - "parser က empty path လက်ခံတယ်၊ ဒါကြောင့် instruction သာ ဖြစ်တယ်" လို့ ရေးခဲ့တယ်။
   - တကယ်တော့ self_bias_gate ရဲ့ `_check_threat_has_path` က High/Critical report မှာ path ဗလာဖြစ်ရင် audit_trail ထဲ flag ရေးတယ်။
   - Grade PARTIAL ကတော့ မှန်ပါတယ် (ထုတ်ပြီးမှ စစ်တာ၊ flag သာ ရေးပြီး block မလုပ်လို့)။
4. **ပြီးခဲ့တဲ့ turn ရဲ့ mapping table မှာ "selection-frequency alert လိုတယ်" လို့ ပြောခဲ့တာ မှားတယ်။**
   - `_check_source_dominance` ရှိပြီးသားပါ: နောက်ဆုံး run ရဲ့ selected set ထဲမှာ source တစ်ခုက 35% ကျော်ရင် SELF_BIAS_FLAG ထွက်တယ်။
   - "၅ ရက်ဆက်တိုက်" version တော့ မဟုတ်ပါ။
5. **CLM-1127 note မပြည့်စုံဘူး။**
   - NN-PHI-6 ရဲ့ handling ဘက်ကို တည်ဆောက်ပြီးသားပါ: `_REVIEW_ONLY_SOURCES` (rt, cgtn, press tv, al-mayadeen, telesur, global times) → review_only path → cause+effect AND fff_path လိုတယ်။
   - Shelve လုပ်ထားတာက collection ပဲ ဖြစ်ပါတယ်။

**ထပ်ဆောင်း:** ပြီးခဲ့တဲ့ turn မှာ prebunking (Roozenbeek ~1.95x) ကို ယုံကြည်စိတ်ချစွာ ကိုးကားခဲ့တယ်။ ဒါပေမဲ့ ဒီအထောက်အထားကို ငြင်းခုံနေကြပါတယ်။ အမှတ် ၃ မှာ ပြပါမယ်။

---

### ၃။ "သတင်းအားလုံးကို မယုံတော့တာ" — fact ကလား၊ feeling ကလား

**အဖြေ:** Fact က အဲဒီ ကောက်ချက်ကို ဘယ်တော့မှ မရောက်နိုင်ပါဘူး။
- Fact က source တစ်ခု ဒါမှမဟုတ် claim တစ်ခုကို မယုံသင့်ကြောင်း ပြနိုင်ပါတယ် (track record)။
- "သတင်း**အားလုံး**" ဆိုတာကတော့ ဘယ်သက်သေကမှ မထောက်ခံနိုင်တဲ့ ယေဘုယျဆန်မှုပါ။
- ယုတ္တိဗေဒအရ blanket distrust ဟာ blanket trust ရဲ့ ကြေးမုံပြင်ပါ — နှစ်ခုလုံး claim တစ်ခုချင်း စစ်ရမယ့် အလုပ်ကို ကျော်သွားတယ်။

ဒါကြောင့် အဓိကက feeling နဲ့ မောပန်းမှုကနေ လာတာပါ —
- **Reuters DNR 2025:**
  - ယုံကြည်မှု 40%။
  - 40% က သတင်းကို တခါတရံ/မကြာခဏ ရှောင်တယ် (2017 မှာ 29%)။
  - အကြောင်းရင်း: overload ("It's too much")၊ ငယ်ရွယ်သူတွေမှာ **ဘာမှ မတတ်နိုင်ဘူး ခံစားရတာ (powerless)**၊ နားလည်ရ ခက်တာ။
  - ဒါတွေက fact ကနေ ဆင်ခြင်ပြီး ရောက်လာတဲ့ ကောက်ချက် မဟုတ်ဘဲ ခံစားချက် အခြေအနေတွေပါ။
- **Firehose ရဲ့ ရည်မှန်းချက်** ကလည်း ဒါပါပဲ: ပင်ပန်းပြီး ပခုံးတွန့်သွားအောင်။

**Analysis လုပ်ရင်း အဲဒီကို ရောက်သွားနိုင်လား?** ရောက်နိုင်ပါတယ်၊ သုတေသနမှာ မှတ်တမ်းတင်ထားပါတယ် —
- **van der Meer, Hameleers & Ohme (Journalism Studies, 2023, n=1,305):**
  - misinformation ကို ဒါမှမဟုတ် **misinformation သတိပေးချက်** ကို တွေ့ပြီးသူတွေက **မှန်တဲ့ သတင်း** ကို ယုံကြည်နိုင်မှု နည်းတယ်လို့ အဆင့်ပေးကြတယ်။
  - fact-check ကတော့ အဲဒီလို မကျစေပါ။
- **Modirrousta-Galian & Higham (JEP: General, 2023):**
  - Bad News / Go Viral! game တွေကို ROC နဲ့ ပြန်ခွဲကြည့်တဲ့အခါ အမှန်/အမှား ခွဲခြားနိုင်စွမ်း **မတက်ပါ**။
  - အကုန်လုံးကို "false" လို့ ပိုပြောလာကြတာပဲ ရှိတယ်။

**ယန္တရား — အလွှာ မခွဲတာ:** ခြယ်လှယ်မှု အများစုက **ဖြစ်ရပ် (fact)** အလွှာမှာ မနေဘဲ **frame၊ ရွေးချယ်မှု၊ ချန်လှပ်မှု** အလွှာမှာ နေပါတယ်။

| အလွှာ | မေးခွန်း | ခြယ်လှယ်မှု ဖြစ်တတ်လား |
|---|---|---|
| ၁ ဖြစ်ရပ် | ဖြစ်ခဲ့သလား | အနည်းဆုံး — လွတ်လပ်တဲ့ source အများနဲ့ စစ်လို့ရ |
| ၂ frame | ဘယ်စကားလုံး၊ ဘယ်သူ့ကို အကြောင်းရင်း လုပ် | အများဆုံး |
| ၃ ရွေးချယ်/ချန်လှပ် | ဘာ မပြော | အများဆုံး (NN-PHI-5) |
| ၄ ကောက်ချက်/ခန့်မှန်း | ဘာဖြစ်လာမလဲ | အလယ်အလတ် |

Analysis က အလွှာ ၂–၃ မှာ ခြယ်လှယ်မှုကို တွေ့ပြီး အလွှာ ၁ ပါ မှားတယ်လို့ ကောက်ချက်ချရင် blanket distrust ဖြစ်သွားပါတယ်။

မှန်တဲ့ analysis ရဲ့ ရလဒ်က ဒီလိုပါ: "ဖြစ်ရပ်က မှန်တယ် (source ၃ ခု)၊ frame က X ရဲ့ frame၊ Y ကို ချန်ထားတယ်" — **calibrated trust**။

Signal detection နဲ့ ပြောရရင် ရည်မှန်းချက်က **discernment** (မှန်တာကို လက်ခံ၊ မှားတာကို ငြင်း) ပါ၊ **skepticism** (အကုန်ငြင်း) မဟုတ်ပါ။ အကုန်ငြင်းရင် discernment က သုည ဖြစ်ပါတယ် — အကုန်ယုံတာနဲ့ အတူတူပါပဲ။

**Cui Bono:** ဘာမှ သိလို့ မရဘူးဆိုရင် အသံအကျယ်ဆုံးသူ အနိုင်ရပါတယ်။ ဒါကြောင့် blanket distrust ဟာ ကာကွယ်ရေး မဟုတ်ဘဲ **cognitive warfare အောင်မြင်သွားတဲ့ အခြေအနေ** ပါ။ မှန်တဲ့ သတိပေးချက်ကိုပါ လိုက်မလုပ်နိုင်တော့လို့ပါ။

**GNI အတွက်** (Roadmap 5 design constraint အဖြစ် ထည့်သင့်):
- (က) output တွေက သံသယဖြစ်စရာကိုသာ မပြောဘဲ **ဘာက ယုံလို့ရတယ်** ဆိုတာကိုလည်း ပြောရမယ်။
- (ခ) R5 measure တွေက suspicion ကို မတိုင်းဘဲ discernment ကို တိုင်းရမယ်။
- (ဂ) သတိပေးချက်တိုင်းမှာ "ဒါကတော့ မှန်နေဆဲ" ပါရမယ် — van der Meer spillover ကို ရှောင်ဖို့ပါ။

---

### ၄။ "ရန်သူ" ဆိုတာ ဘယ်သူလဲ

**အဖြေ:** ကျွန်တော့် စာကြောင်း "'ရန်သူရဲ့ cognitive warfare' လို့ label ကပ်ပြီး ကြောက်ရွံ့အောင် လုပ်ရင်" မှာ ကျွန်တော် ပြောချင်တာက label ကပ်တဲ့သူရဲ့ failure mode ပါ။ အဲဒီက "ရန်သူ" ဆိုတာ fact မဟုတ်ပါဘူး — **label ကပ်သူက ညွှန်ပြလိုက်တဲ့ ဘယ်သူမဆို** ပါ။ Label ကိုယ်တိုင်က ရန်သူကို ဖန်တီးလိုက်တာပါ။ ကျွန်တော့် စကားလုံးရွေးချယ်မှု မတိကျခဲ့တာ အားနည်းချက်ပါ: ရန်သူ ရှိပြီးသား ဖြစ်နေသလို ဖတ်လို့ ရသွားတယ်။

| | Fact အပေါ် အခြေခံတဲ့ စောင့်ကြည့်မှု | Label ကပ်ခြင်း |
|---|---|---|
| ပစ်မှတ် | **အပြုအမူ/နည်းစနစ်** (ညှိထားတဲ့ posting၊ ပုံဟောင်း ပြန်သုံး၊ အချိန်ကိုက်) | **identity** (နိုင်ငံ၊ လူမျိုး၊ outlet၊ အုပ်စု) |
| claim ပုံစံ | "S က D ရက်တွေမှာ B လုပ်ခဲ့တယ်၊ သက်သေ E၊ confidence C" | "X က ရန်သူ / X ရဲ့ ဝါဒဖြန့်" |
| မှားကြောင်း ပြလို့ရလား | ရ — ဘာသက်သေ ဆိုရင် ပြန်ရှင်းမလဲ ဆိုတာ ကြေညာထားတယ် | မရ — သက်သေ အားလုံးကို ပြန်အဓိပ္ပာယ်ကောက်တယ် |
| နယ်ပယ် | ဒီကိစ္စ၊ ဒီအချိန် | သူတို့ ပြောသမျှ |
| ညီမျှမှု | source အားလုံးကို စံတူသုံး (Unheard Voice = pro-Western covert ops) | out-group ကိုပဲ |
| စာဖတ်သူဆီ ပို့တာ | **ဘာကို စစ်ရမလဲ** (method) | **ဘယ်သူ့ကို ကြောက်ရမလဲ** (verdict) |
| ရလဒ် | discernment | ကြောက်စိတ် + ကွဲပြဲမှု (Sectarian Trap) |

**တူတာ:**
- နှစ်ခုလုံး အန္တရာယ်ရင်းမြစ်ကို နာမည်တပ်တယ်။
- အာရုံကို လမ်းညွှန်တယ်။
- **ဘာကို စောင့်ကြည့်မလဲ ရွေးတာကိုယ်တိုင်က ရွေးချယ်မှု တစ်ခုပါ။**
- ကြောက်စိတ် ဖြစ်စေနိုင်တယ်။

စောင့်ကြည့်မှုက label ဆီကို အဆင့်လိုက် ယိုယွင်းသွားတတ်ပါတယ်: အပြုအမူ သက်သေ → source တစ်ခုလုံး → နိုင်ငံတစ်ခုလုံး → share တဲ့ လူတွေ။ ဒါက ဇွန်လမှာ ဆွေးနွေးခဲ့တဲ့ autoimmune response ပါ။

ကျွန်တော်တို့ ကိုယ်ပိုင် စည်းကမ်းက ရှိပြီးသားပါ:
- "Name the mechanism, never the demon"
- PHI-002 "apparatus ≠ people"
- NN-PHI-8 "method, never verdict"
- ဥပမာ: Doppelganger ရဲ့ အပြုအမူကို စောင့်ကြည့်တာ (EU က SDA/Struktura ကို ပိတ်ဆို့ထား) ဟာ သက်သေအခြေခံပါတယ်။ "Russian media = လိမ်တယ်" ဆိုတာကတော့ label ပါ။ သရုပ်ဆောင်ချင်း တူပေမဲ့ claim မတူပါဘူး။

**GNI output အတွက် စမ်းသပ်နည်း:** သရုပ်ဆောင်ရဲ့ နာမည်ကို တခြားနာမည်နဲ့ လဲကြည့်ပါ။ Claim က ရပ်တည်နေသေးလား? **ဘယ်သူလဲ** ဆိုတဲ့ အပေါ်မှာပဲ မှီခိုနေရင် အဲဒါ label ပါ။

---

### ၅။ Understanding နဲ့ ရုပ်ပိုင်းလုံခြုံမှု၊ path

**အဖြေ:** Understanding ဟာ လုံခြုံမှုနဲ့ path မရှိဘဲ **ဖြစ်တည်လာနိုင်ပါတယ်**။ ၂၀၂၁ မြန်မာမှာ လူတွေ ဘာဖြစ်နေလဲ ရှင်းရှင်းလင်းလင်း နားလည်ခဲ့ကြပေမဲ့ လုံခြုံမှု မရှိခဲ့ပါဘူး။ Understanding တစ်ခုတည်း မလုပ်နိုင်တာက **Freedom from Fear အဖြစ် ပြောင်းလဲသွားဖို့** ပါ။

ကျွန်တော် အရင်က လျှော့ပြောခဲ့တဲ့ အချက်လည်း ရှိပါတယ်: လုံခြုံမှုနဲ့ path အချို့က understanding **ဖြစ်ပြီးမှ** သာ မဟုတ်ဘဲ **မဖြစ်ခင်** ကတည်းက လိုပါတယ်။ ဒါကြောင့် အစု နှစ်ခု ခွဲရပါမယ်။

**မဖြစ်ခင် (understanding ဖြစ်စေတဲ့ အခြေအနေ):**
- **B1 တွေးနိုင်လောက်တဲ့ အနည်းဆုံး လုံခြုံမှု:** ပြေးနေရရင် ဖတ်ချိန် မရှိ၊ အာရုံ ကျဉ်းသွားတယ်။
- **B2 သတင်းကို လုံခြုံစွာ ရယူနိုင်မှု:** source မပိတ်ခံရ၊ ဖတ်တာကိုယ်တိုင် အန္တရာယ် မဖြစ် (checkpoint မှာ ဖုန်းစစ်တာမျိုး)။
- **B3 မေးခွန်းထုတ်ဖို့ လူမှုရေး လုံခြုံမှု:** ယုံကြည်ချက် ပြောင်းရင် အုပ်စုထဲက နှင်မထုတ်ခံရ။ Echo chamber ကနေ ထွက်ရတဲ့ ကုန်ကျစရိတ်ပါ။
- **B4 path ရှိတယ်လို့ ယုံကြည်မှု (perceived efficacy):**
  - Witte ရဲ့ EPPM အရ ခြိမ်းခြောက်မှု မြင့်ပြီး efficacy နိမ့်ရင် **fear control** ဖြစ်တယ် — ငြင်းဆို၊ ရှောင်ပြေး။ လူက အန္တရာယ်ကို မစီမံတော့ဘဲ ကြောက်စိတ်ကိုပဲ စီမံတော့တယ်။
  - **ဒါကြောင့် path ရှိတယ်လို့ မယုံရင် သတင်းကို ရှောင်တယ် → understanding မဖြစ်လာဘူး။**
  - Reuters ရဲ့ "powerless" ငယ်ရွယ်သူ ရှောင်သူတွေက ဒီအချက်ပါ။

**ဖြစ်ပြီးမှ (understanding ကို လွတ်မြောက်မှုအဖြစ် ပြောင်းပေးတဲ့ အခြေအနေ):**
- **A1 အမှန်တကယ် ရုပ်ပိုင်း ကာကွယ်မှု** (ဥပဒေ၊ အရပ်သားကာကွယ်ရေး၊ digital security)
- **A2 အမှန်တကယ် လုပ်လို့ရတဲ့ လုပ်ရပ်** (response efficacy)
- **A3 နားလည်တဲ့ တခြားသူတွေ** (တစ်ယောက်တည်း နားလည်ရင် အထီးကျန်တယ်)
- **A4 တုံ့ပြန်တဲ့ အဖွဲ့အစည်း** (လုပ်ရပ်က အကျိုးရှိအောင်)

| | မဖြစ်ခင် (B) | ဖြစ်ပြီးမှ (A) |
|---|---|---|
| သဘော | အမြင်/ယုံကြည်မှု + အနည်းဆုံး | ရုပ်ပိုင်း + အမှန်တကယ် |
| လုပ်ဆောင်ချက် | စိတ်က **ဝင်ပါမလား** ကို ဆုံးဖြတ် | understanding က **လုပ်ရပ်** ဖြစ်မလား ကို ဆုံးဖြတ် |
| အတိုင်းအတာ | တစ်ဦးချင်း + အနီးပတ်ဝန်းကျင် | စုပေါင်း/အဖွဲ့အစည်း |
| GNI ပေးနိုင်လား | B2 (အခမဲ့)၊ B4 (NN-PHI-4 path)၊ B3 တစ်စိတ်တစ်ပိုင်း (T5) | A2 တစ်စိတ်တစ်ပိုင်း (solutions journalism) |
| GNI မပေးနိုင် | B1 | A1, A4 |

**တူတာ:**
- နှစ်ခုလုံး ပြင်ပ အခြေအနေပါ။ Understanding တစ်ခုတည်းက မဖန်တီးနိုင်ပါ။
- နှစ်ခုလုံးကို cognitive warfare က တိုက်ခိုက်ပါတယ်:
  - flooding → B1 ကို ခိုးတယ်။
  - division → B3/A3 ကို ခိုးတယ်။
  - trust demolition → A4 ကို ခိုးတယ်။
  - fear without path → B4 ကို ခိုးတယ်။
- UNGA 66/290 ရဲ့ "protection and empowerment" နဲ့ ကိုက်ပါတယ်: protection = A1, empowerment = B4 + A2။

**အကြောင်းအကျိုး စက်ဝိုင်း နှစ်ခု:**
- **ကောင်းတဲ့ စက်ဝိုင်း:** B (အနည်းဆုံး လုံခြုံမှု + path ယုံကြည်မှု) → understanding → လုပ်ရပ် (A2) → တခြားသူတွေနဲ့ (A3) → အမှန်တကယ် လုံခြုံမှု (A1) → bandwidth ပိုရ (B1) → ပိုနက်တဲ့ understanding
- **ဆိုးတဲ့ စက်ဝိုင်း (cognitive warfare ရဲ့ ရည်မှန်းချက်):** path မပါတဲ့ ခြိမ်းခြောက်မှု → fear control (ရှောင်) → understanding မဖြစ် → လုပ်ရပ် မရှိ → အမှန်တကယ် အားနည်း → ကြောက်စိတ် ပိုများ

**ဖြစ်နိုင်ခြေ ၄ ခု:**
- Understanding + path/safety = Freedom from Fear
- Understanding ရှိ၊ path/safety မရှိ = **ဆင်ခြင်တုံတရားနဲ့ ညီတဲ့ ကြောက်စိတ်**။ ရလဒ်က လှုပ်မရဖြစ်တာ၊ ထွက်ပြေးတာ၊ ဒါမှမဟုတ် သတ္တိ ဖြစ်နိုင်တယ်။ ဇွန်လမှာ ဖတ်ခဲ့တဲ့ Aung San Suu Kyi ရဲ့ "It is not power that corrupts but fear" က ဒီအမျိုးအစားပါ — ကြောက်စိတ်ကင်းတာ မဟုတ်ဘဲ ကြောက်စိတ်က **အုပ်ချုပ်တာ မခံရ** တာပါ။
- Safety ရှိ၊ understanding မရှိ = သက်တောင့်သက်သာ ရှိပေမဲ့ ခြယ်လှယ်ခံရနိုင်တယ်
- နှစ်ခုလုံး မရှိ = ကြောက်စိတ်က အုပ်ချုပ်တယ်

**GNI အတွက် ရိုးသားရမယ့် ကန့်သတ်ချက်:**
- PHI-003 က ငြင်းပယ်တာက **understanding မပါတဲ့** ကြောက်စိတ် ပါ၊ ကြောက်စိတ် ကိုယ်တိုင်ကို မဟုတ်ပါ။
- အန္တရာယ်က တကယ်ရှိရင် ကြောက်စိတ်ဟာ မှန်ကန်တဲ့ signal ပါ။ GNI က false comfort မပေးရပါ။
- ဒါကြောင့် GNI တိုင်းနိုင်တဲ့ Freedom from Fear ဆိုတာ = **ဖန်တီးထားတဲ့ ကြောက်စိတ် မရှိခြင်း + အမှန်တကယ် path ကို နာမည်တပ်ခြင်း** ပါ၊ "စာဖတ်သူ လုံခြုံတယ်လို့ ခံစားရတာ" မဟုတ်ပါ။ ဒါကို R5 spec §6 မှာ ထည့်ရပါမယ်။

---

### ဆက်လုပ်ရမယ့်အရာ

R12 run ရဖို့ ကျန်နေပါသေးတယ် (md5 6a275fdf…၊ မပြောင်းပါ)။ ဆွေးနွေးပြီးရင် R13 မှာ ပြင်ရမှာတွေ:
- WRONG 1–5
- Roadmap 5 constraint တွေ (discernment ကို တိုင်းဖို့၊ သတိပေးချက်မှာ "မှန်နေဆဲ" ပါဖို့၊ R5-4 ကို self_bias_gate ပေါ်မှာ ဆောက်ဖို့၊ Freedom from Fear ကန့်သတ်ချက်)

- **A** — R12 ကို အရင် run၊ ပြီးမှ R13 (ကျွန်တော့် lean: R12 က verify ပြီးသား၊ R13 က ပြင်ဆင်ချက် scope သီးသန့်ဖြစ်လို့)
- **B** — R12 ကို R12b အဖြစ် ပြန်ဆောက်ပြီး ပြင်ဆင်ချက်တွေ ပေါင်းထည့်

Sources:
- [van der Meer, Hameleers & Ohme 2023 — PsyPost summary](https://www.psypost.org/study-shows-how-efforts-to-combat-misinformation-might-undermine-trust-in-real-news/)
- [Modirrousta-Galian & Higham 2023 — Southampton ePrints](https://eprints.soton.ac.uk/475360)
- [Reuters Institute Digital News Report 2025 — Executive Summary](https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2025/dnr-executive-summary)
- [NATO ACT — Cognitive Warfare](https://www.act.nato.int/activities/cognitive-warfare/)
- [Extended parallel process model (Witte 1992) — Wikipedia](https://en.wikipedia.org/wiki/Extended_parallel_process_model)

---

## 4. CORRECTIONS OWED (found by the section 3 search; not yet in the tree)

Each of these is a WRONG for the S112 ledger. The fixes land in a runner after S112_R12 (R13, or the
first runner of S113). Bytes cited are as read at HEAD 1c3fe8a plus the R12 tree.

| # | what was wrong | what the bytes say | fix |
|---|---|---|---|
| 1 | `docs/GNI_PHILOSOPHY_S112.md` holds 28 rules; **NN-PHI-8 is missing** | `phi_compatibility_check.md` (GNI-L-011's own mapping file, S43, 2026-06-12): NN-PHI-8 the Duty Clause — seniors as the delivery channel to voting-age young adults, "Method, never verdict", status OPEN | add the third source to the extract's header and the NN-PHI-8 row; mint its claim; ledger row NOT BUILT (no code surface) |
| 2 | CLM-1112 (T4, fear without understanding) graded NOT BUILT | escalation_scorer.py "PHI-003 gate" caps escalation at 5.0 when GNI's own read is calm and no critical combo fired; self_bias_gate.py (gni_selfbias.yml, daily 06:00 UTC) checks escalation-sentiment coherence | re-grade PARTIAL: the number is guarded, the text is not |
| 3 | CLM-1111 / CLM-1125 note: "the parser accepts an empty path, so the rule is an instruction, not a check" | self_bias_gate `_check_threat_has_path` flags High/Critical reports with an empty fff_human_path to audit_trail | grade PARTIAL stands (after publication, flags, does not block); note rewritten |
| 4 | the thread's GNI table said a selection-frequency alert was "needed" | `_check_source_dominance` exists (share > 35% of the latest run's selected set) | corrected in section 2.8; the consecutive-day version is still owed |
| 5 | CLM-1127 note: "neither signal nor authority" | `_REVIEW_ONLY_SOURCES` (rt, russia today, cgtn, press tv, al-mayadeen, telesur, global times) routes such sources to review_only, which must pass cause+effect AND fff_path | note: handling built, collection shelved (S34) |
| 6 | prebunking cited with lab gains (Roozenbeek 2022, ~1.95x / 2.14x) and no caveat | Modirrousta-Galian & Higham 2023 (JEP: General) reanalysed the games with ROC: no gain in discrimination, more items called false | cite both; Roadmap 5 measures discernment, not suspicion |
| 7 | Roadmap 5 spec R5-4 reads as a new gate | the structural self-audit layer already runs daily | R5-2/R5-4 extend self_bias_gate rather than start beside it |
| 8 | ISO/IEC/IEEE 29148 cited from its abstract only (earlier in S112) | body not read | drop the citation |

---

## 5. PROPOSED CONSTRAINTS AND OPEN ITEMS (proposals — the operator rules)

**For Roadmap 5 (from section 3, Q3 and Q5):**
- Measure **discernment** (true accepted, false rejected; ROC / signal detection), never suspicion
  alone — a reader who rejects everything scores zero, like one who accepts everything.
- Every warning GNI prints carries what is still reliable ("the event is confirmed by N independent
  sources; the frame is X's; Y is missing") — against the warning spillover van der Meer, Hameleers &
  Ohme 2023 measured.
- Report what is reliable as well as what is suspect: confirming is as much GNI's job as debunking.
- §6 limits gains one line: the Freedom from Fear GNI can measure is *no manufactured fear + a real
  path named*, not "readers feel safe"; where danger is real, fear is a correct signal and false
  comfort is forbidden (PHI-003).

**For the adversarial-source framework (the shelved deep-work session):**
- Object of every claim is a behaviour or technique, never an identity; the same criteria for every
  source, including friendly ones; each claim carries evidence, confidence, scope, and what would
  clear it (ICD 203 discipline). Test: swap the actor's name — if the claim no longer stands, it is a
  label.
- Inputs already on file: the operator's S34 evidence of summary manipulation (screenshots offered,
  never collected); U-2 (A collect review_only / B framework only) still unanswered; Partner B's
  FIMI exposure matrix / DISARM / ABCDE work as a field-legible reference.
- GNI is itself an AI summariser: the framework has two faces — others' AI at the input, GNI's own
  LLM at the output (semantic self-audit, OPEN since S41).

**Open, not ruled:** A deep-work session / B prebunking row in Roadmap 5 / C Roadmap 6 (section 2.8);
NN-PHI-8's planned surfaces (conversation starter, micro-lesson, two human tests); the consecutive-day
selection alert.

---

## 6. SOURCES (read in S112)

- NATO ACT, Cognitive Warfare — https://www.act.nato.int/activities/cognitive-warfare/
- RAND, The Russian "Firehose of Falsehood" Propaganda Model (Paul & Matthews, 2016)
- DISARM Framework — https://www.disarm.foundation/
- Fazio et al. 2015, Knowledge does not protect against illusory truth (JEP: General)
- Rathje, Van Bavel & van der Linden 2021, Out-group animosity drives engagement on social media (PNAS)
- Robertson et al. 2023, Negativity drives online news consumption (Nature Human Behaviour)
- Cinelli et al. 2021, The echo chamber effect on social media (PNAS)
- Roozenbeek et al. 2022, Psychological inoculation improves resilience against misinformation on social media (Science Advances)
- Modirrousta-Galian & Higham 2023, Gamified inoculation interventions do not improve discrimination between true and fake news (JEP: General) — https://eprints.soton.ac.uk/475360
- van der Meer, Hameleers & Ohme 2023, Can fighting misinformation have a negative spillover effect? (Journalism Studies) — https://www.psypost.org/study-shows-how-efforts-to-combat-misinformation-might-undermine-trust-in-real-news/
- Reuters Institute Digital News Report 2025 — https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2025/dnr-executive-summary
- Witte 1992, Extended Parallel Process Model — https://en.wikipedia.org/wiki/Extended_parallel_process_model
- EU DisinfoLab, Doppelganger; Graphika, Spamouflage; Graphika & Stanford Internet Observatory, Unheard Voice (2022); Meta/Facebook, Removing Myanmar military officials from Facebook (Aug 2018)
- UNDP Human Development Report 1994; UN General Assembly resolution 66/290 (2012), paragraph 3
