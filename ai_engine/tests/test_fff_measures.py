"""S115 roadmap 5 row R5-2: the Freedom-from-Fear measures in self_bias_gate.py.

Every input here is CONSTRUCTED. None is taken from docs/gni_output_sample_S*.json: the
thresholds were ruled before any measure ran over the sample (DECISIONS S115-1 to S115-4), and
these tests prove the measures discriminate, not what the sample holds.
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SBG = os.path.join(os.path.dirname(HERE), "analysis", "self_bias_gate.py")
_spec = importlib.util.spec_from_file_location("sbg_under_test", SBG)
sbg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sbg)

CLEAN = {
    "id": "clean", "title": "Two neighbours resume talks", "summary": "Two countries met on Monday.",
    "sentiment": "Neutral", "risk_level": "High",
    "fff_what_is_happening": "Two countries held talks on Monday. They agreed to meet again next month.",
    "fff_honest_analysis": "If the talks hold, fuel may cost less by winter.",
    "fff_human_path": "Watch the price of fuel at your local station this month and ask your school "
                      "how bus fares may change.",
}

FAILING = {
    "readability": {"fff_what_is_happening": "Notwithstanding multilateral considerations, "
                    "unprecedented geopolitical reconfigurations precipitated extraordinarily "
                    "consequential institutional deliberations."},
    "jargon": {"fff_what_is_happening": "Bearish sentiment pushed SPY lower on Monday."},
    "path_generic": {"fff_human_path": "Young people should stay informed about the talks this year."},
    "fear_vocabulary": {"summary": "The talks may bring a catastrophic outcome."},
    "threat_has_path": {"fff_human_path": "Watch."},
    "sectarian": {"summary": "Anonymous sources say Christians are behind the attack."},
    "manipulation": {"fff_honest_analysis": "Everyone knows the talks will fail."},
}


def test_every_measure_is_wired_and_budgeted():
    assert set(sbg.FFF_MEASURES) == set(FAILING)
    for name, (fn, budget) in sbg.FFF_MEASURES.items():
        assert fn in sbg.CHECKS, name
        assert budget in (sbg.PROXY_BUDGET, sbg.ABSOLUTE_BUDGET), name


def test_clean_report_passes_every_measure():
    for name, (fn, _) in sbg.FFF_MEASURES.items():
        assert fn(CLEAN) is None, (name, fn(CLEAN))


def test_each_failing_report_fails_its_own_measure():
    for name, change in FAILING.items():
        fn = sbg.FFF_MEASURES[name][0]
        finding = fn(dict(CLEAN, **change))
        assert finding is not None and finding["check"] == name, name


def test_funnel_lists_are_read_not_copied():
    lists = sbg._funnel_lists()
    for name in ("SANITIZE_VOCAB", "_PHI003_RHETORIC_PATTERNS", "_PHI002_PATTERNS",
                 "_SECTARIAN_PATTERNS"):
        assert lists[name], name
    assert ("catastrophic", "significant") in lists["SANITIZE_VOCAB"]


def test_fk_grade_matches_the_published_formula():
    # 6 words, 1 sentence, 6 syllables: 0.39*6 + 11.8*1 - 15.59 = -1.45
    assert sbg.fk_grade("The cat sat on the mat.") == -1.4
    assert sbg.fk_grade("") is None
    # 'U.S.' is one word, not three sentence ends
    assert sbg.fk_grade("U.S. forces left.") == sbg.fk_grade("US forces left.")


def test_syllable_heuristic_on_a_dictionary_table():
    table = {"cat": 1, "table": 2, "makes": 1, "beautiful": 3, "investigation": 5, "strikes": 1,
             "fired": 1, "agreed": 2, "countries": 2, "state": 1, "analysis": 4, "energy": 3,
             "people": 2, "prices": 2, "started": 2, "taxes": 2, "supplies": 2}
    assert {w: sbg._syllables(w) for w in table} == table


def test_investigation_is_not_investing_advice():
    path = "Follow the investigation of the attack in the news for a month."
    assert sbg._check_path_generic(dict(CLEAN, fff_human_path=path)) is None


def test_a_political_label_is_not_a_fear_amplifier():
    assert sbg._check_fear_vocabulary(dict(CLEAN, summary="The occupation entered its third year.")) is None
