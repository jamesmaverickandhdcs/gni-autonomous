"""S115 roadmap 5 row R5-3: tools/gni_fff_review.py on a COPY of the tree with constructed outputs.

The committed sample and any real rating are never read here. Proves: the pick holds every
minority verdict and is reproducible; the reader's sheet carries no machine verdict; a review that
does not answer exactly the selected items is refused; positive and negative agreement follow
Cicchetti and Feinstein's formulas; a small class reads INSUFFICIENT, a perfect reader AGREES and a
contrary one DISAGREES.
"""
import importlib.util
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tools"))
import gni_fff_review as rv  # noqa: E402

_spec = importlib.util.spec_from_file_location("fff_cases_rv", os.path.join(HERE, "test_fff_measures.py"))
cases = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cases)

HARD = cases.FAILING["readability"]


def _tree(root, outputs):
    for rel in ("ai_engine/analysis/self_bias_gate.py", "ai_engine/funnel/intelligence_funnel.py"):
        os.makedirs(os.path.dirname(os.path.join(root, rel)), exist_ok=True)
        shutil.copy(os.path.join(REPO, rel), os.path.join(root, rel))
    os.makedirs(os.path.join(root, "docs"), exist_ok=True)
    with open(os.path.join(root, "docs", "gni_output_sample_S1.json"), "w", encoding="utf-8") as fh:
        json.dump({"harvest": {"rows": len(outputs), "outputs": outputs}}, fh)
    return root


def _outputs():
    """20 outputs: 3 pass readability (the minority), 17 fail it; one carries a rhetoric pattern."""
    out = []
    for k in range(20):
        o = dict(cases.CLEAN, id="id%02d" % k, md5="m%02d" % k)
        if k >= 3:
            o.update(HARD)
        if k == 7:
            o.update(cases.FAILING["manipulation"])
        out.append(o)
    return out


def test_pick_holds_every_minority_verdict_and_is_reproducible(tmp_path):
    root = _tree(str(tmp_path), _outputs())
    _, _, items = rv.select(root, size=8, cap=10)
    ids = [o["id"] for _, o in items]
    assert {"id00", "id01", "id02", "id07"} <= set(ids)
    assert len(ids) == len(set(ids)) == 8
    assert [k for k, _ in items] == ["R%02d" % n for n in range(1, 9)]
    assert ids == [o["id"] for _, o in rv.select(root, size=8, cap=10)[2]]


def test_the_sheet_is_blind(tmp_path):
    root = _tree(str(tmp_path), _outputs())
    name, seed, items = rv.select(root, size=8, cap=10)
    page = rv.sheet_html(items, rv._md5(rv.selection_text(name, seed, items, rv.measure_sources(root))), 1)
    asked = " ".join(text for _, text, _ in rv.QUESTIONS)
    words = [m for m in rv.MEASURE_QUESTION if m not in asked]       # a question may say "jargon"
    assert "readability" in words and "path_generic" in words
    for word in words + ["FFF_MEASURES", "Flesch", "budget", "DEFEATED", "SUPPORTED"]:
        assert word not in page, word
    payload = json.loads(page.split("const P = ", 1)[1].split(";\n", 1)[0].replace("<\\/", "</"))
    assert all(set(it) == {"item", "report_id", "fields"} for it in payload["items"])
    assert "</script>" in page and page.count("</script>") == 1


def _rows(items, verdicts, contrary=False, flip=()):
    rows = []
    for k, o in items:
        r = {"item": k, "report_id": o["id"], "paraphrase": "two sides talk", "note": ""}
        for q in rv.QIDS:
            fails = any(verdicts[o["id"]][m] for m, (mq, _) in rv.MEASURE_QUESTION.items() if mq == q)
            if contrary or k in flip:
                fails = not fails
            r[q] = rv.FAIL_ANSWER[q] if fails else ("no" if rv.FAIL_ANSWER[q] == "yes" else "yes")
        rows.append(r)
    return rows


def test_agreement_follows_the_formulas_and_the_verdict_rule(tmp_path):
    root = _tree(str(tmp_path), _outputs())
    _, _, items = rv.select(root, size=20, cap=10)
    outs = {o["id"]: o for _, o in items}
    v = rv._machine(root, list(outs.values()))
    perfect = rv.agreement(_rows(items, v), outs, v)
    assert perfect["readability"]["verdict"] == "INSUFFICIENT"      # only 3 outputs pass it
    assert perfect["readability"]["p_pos"] == 1.0
    assert perfect["manipulation"]["verdict"] == "INSUFFICIENT"     # 1 output fails it
    flipped = rv.agreement(_rows(items, v, flip=("R01", "R02", "R03")), outs, v)
    r = flipped["readability"]
    a, b, c, d = r["a"], r["b"], r["c"], r["d"]
    assert a + b + c + d == 20
    assert r["p_pos"] == 2 * a / (2 * a + b + c) and r["p_neg"] == 2 * d / (2 * d + b + c)


def test_perfect_reader_agrees_and_contrary_reader_disagrees(tmp_path):
    outs = _outputs()
    for k in range(3, 9):               # six more pass readability: both classes now reach MIN_CLASS
        outs[k] = dict(cases.CLEAN, id=outs[k]["id"], md5=outs[k]["md5"])
    root = _tree(str(tmp_path), outs)
    _, _, items = rv.select(root, size=20, cap=10)
    by = {o["id"]: o for _, o in items}
    v = rv._machine(root, list(by.values()))
    assert rv.agreement(_rows(items, v), by, v)["readability"]["verdict"] == "AGREES"
    assert rv.agreement(_rows(items, v, contrary=True), by, v)["readability"]["verdict"] == "DISAGREES"


def _tsv(meta, rows):
    head = ["# %s: %s" % kv for kv in meta.items()] + ["\t".join(rv.COLUMNS)]
    return "\n".join(head + ["\t".join(r[c] for c in rv.COLUMNS) for r in rows]) + "\n"


def test_a_review_that_does_not_answer_the_selection_is_refused(tmp_path):
    root = _tree(str(tmp_path), _outputs())
    _, _, items = rv.select(root, size=8, cap=10)
    v = rv._machine(root, [o for _, o in items])
    sel = [(k, o["id"]) for k, o in items]
    meta = {"reader_role": "test", "date": "2026-10-24", "selection_md5": "x"}
    rows = _rows(items, v)
    rv.parse_review(_tsv(meta, rows), sel)
    bad_value = [dict(r) for r in rows]
    bad_value[0]["T1"] = "maybe"
    no_para = [dict(r) for r in rows]
    no_para[1]["paraphrase"] = " "
    for text in (_tsv(meta, rows[:-1]), _tsv(meta, bad_value), _tsv(meta, no_para),
                 _tsv({"date": "2026-10-24", "selection_md5": "x"}, rows),
                 _tsv(dict(meta, date="24/10/2026"), rows)):
        try:
            rv.parse_review(text, sel)
        except rv.ReviewError:
            continue
        raise AssertionError("accepted a review it must refuse")


def test_agree_refuses_a_review_made_on_another_selection(tmp_path):
    root = _tree(str(tmp_path), _outputs())
    name, seed, items = rv.select(root, size=8, cap=10)
    sel = rv.selection_text(name, seed, items, rv.measure_sources(root))
    with open(os.path.join(root, "docs", "GNI_FFF_REVIEW_SELECTION_S1.tsv"), "w", encoding="utf-8") as fh:
        fh.write(sel)
    v = rv._machine(root, [o for _, o in items])
    meta = {"reader_role": "test", "date": "2026-10-24", "selection_md5": "0" * 32}
    with open(os.path.join(root, "docs", "GNI_FFF_REVIEW_S1.tsv"), "w", encoding="utf-8") as fh:
        fh.write(_tsv(meta, _rows(items, v)))
    assert rv.main(["--agree", "1", "--root", root]) == 1
    assert not os.path.exists(os.path.join(root, "docs", "GNI_FFF_AGREEMENT_S1.md"))
    meta["selection_md5"] = rv._md5(sel)
    with open(os.path.join(root, "docs", "GNI_FFF_REVIEW_S1.tsv"), "w", encoding="utf-8") as fh:
        fh.write(_tsv(meta, _rows(items, v)))
    assert rv.main(["--agree", "1", "--root", root]) == 0
    assert os.path.exists(os.path.join(root, "docs", "GNI_FFF_AGREEMENT_S1.md"))


def test_agree_refuses_when_a_measure_changed_after_the_pick(tmp_path):
    for rel in rv.MEASURE_SOURCES:
        root = _tree(str(tmp_path / rel.replace("/", "_")), _outputs())
        name, seed, items = rv.select(root, size=8, cap=10)
        sel = rv.selection_text(name, seed, items, rv.measure_sources(root))
        with open(os.path.join(root, "docs", "GNI_FFF_REVIEW_SELECTION_S1.tsv"), "w", encoding="utf-8") as fh:
            fh.write(sel)
        v = rv._machine(root, [o for _, o in items])
        meta = {"reader_role": "test", "date": "2026-10-26", "selection_md5": rv._md5(sel)}
        with open(os.path.join(root, "docs", "GNI_FFF_REVIEW_S1.tsv"), "w", encoding="utf-8") as fh:
            fh.write(_tsv(meta, _rows(items, v)))
        with open(os.path.join(root, rel), "a", encoding="utf-8") as fh:
            fh.write("\n# a later edit\n")
        assert rv.main(["--agree", "1", "--root", root]) == 1, rel
        assert not os.path.exists(os.path.join(root, "docs", "GNI_FFF_AGREEMENT_S1.md")), rel
