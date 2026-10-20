"""S115 roadmap 5 row R5-2: the FAILURE TEST on a copy that the row's DONE line asks for.

A copy of the tree holding self_bias_gate.py, the funnel it reads, a query file and an output
sample of ONE output: when that output fails a measure the claim bound to it reads DEFEATED, and
when it is the clean output the claim reads SUPPORTED. The outputs are constructed (the ones in
test_fff_measures.py); the committed sample is never read here.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tools"))
import gni_fitness as gf  # noqa: E402

_spec = importlib.util.spec_from_file_location("fff_cases", os.path.join(HERE, "test_fff_measures.py"))
cases = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cases)

# fitness id -> (measure it runs, the binding's verbatim fragment of the claim)
BOUND = {
    "F-FFF-READ": ("readability", "Can a teenager understand what is happening?"),
    "F-FFF-JARGON": ("jargon", "not buried in jargon or market terminology"),
    "F-FFF-PATH": ("path_generic", "Can a teenager understand what can be done about it?"),
    "F-FFF-HASPATH": ("threat_has_path", "Every threat must have a path."),
    "F-FFF-FEAR": ("fear_vocabulary", "Does the content create fear without understanding?"),
    "F-FFF-SECT": ("sectarian", "Does the content divide people by identity?"),
    "F-FFF-MANIP": ("manipulation", "Manipulation techniques are never in GNI output."),
}
QUERY = b"select 1;\n"


def _copy_tree(root, outputs, query_md5=None, rows=None):
    for rel in ("ai_engine/analysis/self_bias_gate.py", "ai_engine/funnel/intelligence_funnel.py"):
        os.makedirs(os.path.dirname(os.path.join(root, rel)), exist_ok=True)
        shutil.copy(os.path.join(REPO, rel), os.path.join(root, rel))
    os.makedirs(os.path.join(root, "docs"), exist_ok=True)
    with open(os.path.join(root, "q.sql"), "wb") as fh:
        fh.write(QUERY)
    snap = {"query_file": "q.sql", "query_md5": query_md5 or hashlib.md5(QUERY).hexdigest(),
            "harvest": {"rows": len(outputs) if rows is None else rows, "outputs": outputs}}
    with open(os.path.join(root, "docs", "gni_output_sample_S1.json"), "w", encoding="utf-8") as fh:
        json.dump(snap, fh)
    return root


def test_every_fitness_is_registered_and_runs_its_own_measure():
    for fid, (measure, _) in BOUND.items():
        assert fid in gf.FITNESS, fid
        assert measure in gf.FITNESS[fid][0], fid


def test_one_failing_output_defeats_its_claim_and_the_clean_one_supports_it(tmp_path):
    for fid, (measure, fragment) in BOUND.items():
        bad = _copy_tree(str(tmp_path / ("bad_" + measure)), [dict(cases.CLEAN, **cases.FAILING[measure])])
        good = _copy_tree(str(tmp_path / ("good_" + measure)), [dict(cases.CLEAN)])
        assert gf.derive(bad, fid, fragment, {})[0] == "DEFEATED", fid
        assert gf.derive(good, fid, fragment, {})[0] == "SUPPORTED", fid


def test_a_proxy_budget_admits_one_in_ten_and_not_two(tmp_path):
    # readability is a proxy (budget 0.10): 1 failing output in 10 holds, 2 in 10 does not
    fail = dict(cases.CLEAN, **cases.FAILING["readability"])
    one = _copy_tree(str(tmp_path / "one"), [fail] + [dict(cases.CLEAN)] * 9)
    two = _copy_tree(str(tmp_path / "two"), [fail] * 2 + [dict(cases.CLEAN)] * 8)
    frag = BOUND["F-FFF-READ"][1]
    assert gf.derive(one, "F-FFF-READ", frag, {})[0] == "SUPPORTED"
    assert gf.derive(two, "F-FFF-READ", frag, {})[0] == "DEFEATED"


def test_a_sample_from_another_query_or_a_cut_copy_is_refused(tmp_path):
    frag = BOUND["F-FFF-MANIP"][1]
    for root in (_copy_tree(str(tmp_path / "md5"), [dict(cases.CLEAN)], query_md5="0" * 32),
                 _copy_tree(str(tmp_path / "rows"), [dict(cases.CLEAN)], rows=2)):
        try:
            gf.derive(root, "F-FFF-MANIP", frag, {})
        except gf.FitnessError:
            continue
        raise AssertionError("accepted a sample it must refuse: " + root)


def test_a_fragment_that_does_not_state_the_rule_is_refused(tmp_path):
    root = _copy_tree(str(tmp_path / "frag"), [dict(cases.CLEAN)])
    try:
        gf.derive(root, "F-FFF-READ", "Every threat must have a path.", {})
    except gf.FitnessError:
        return
    raise AssertionError("a fragment of another rule was accepted")
