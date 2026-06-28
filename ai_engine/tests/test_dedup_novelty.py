# -*- coding: utf-8 -*-
# ============================================================
# S53 DEDUP FIX -- harness for the rewritten INJECTABLE
# check_recent_duplicate (article-URL novelty gate).
#
# RULING (locked): article-URL-novelty only. The title-keyword overlap compare
# is the proven defect (asymmetric div-by-recent-title) that suppressed the 27th
# evening report -- it is DROPPED. This gate keys on the article URL only:
#   basket exposes URL as 'link'; prior rows expose it as 'url'.
#   'id' is md5(source:title) -- NOT a URL -- never used here.
#
# Build order is the safety:
#   PART 1 (this file, baseline): (ii)/(iii) FAIL until the rewrite lands;
#     (i) OLD-SHAPE WITNESS documents the target behaviour (bug GONE).
#   PART 2 (after rewrite): all three GREEN.
#
#   Run:  python -m pytest ai_engine/tests/test_dedup_novelty.py -v
# ============================================================
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))             # ai_engine/

from analysis.supabase_saver import check_recent_duplicate


def _basket(links, summary_words="military strikes trade escalation"):
    """22-article basket; each article carries a distinct 'link' (URL) and a
    summary loaded with the same-event keywords. Titles intentionally vary."""
    return [
        {
            "title": f"Report fragment {i} on the regional situation",
            "summary": f"{summary_words} -- dispatch {i}",
            "link": link,
        }
        for i, link in enumerate(links)
    ]


# ── (i) OLD-SHAPE WITNESS: the 27th inputs that the OLD title-keyword gate
#        false-skipped. Prior report title was "US and Iran Trade Military
#        Strikes"; the basket is 22 DIFFERENT-URL articles whose summaries are
#        thick with military/strikes/trade. Under the OLD asymmetric div-title
#        compare these tripped a >=70% keyword overlap and got SKIPPED. The NEW
#        URL-novelty gate must NOT skip: every URL is new -> publish. ──────────
PRIOR_TITLE_WITNESS = "US and Iran Trade Military Strikes"  # explicit witness


def test_old_shape_witness_does_not_skip():
    basket = _basket([f"https://news.example/27th/{i}" for i in range(22)],
                     summary_words="US Iran military strikes trade escalation")
    # Prior run selected a DIFFERENT set of URLs (same event, different links).
    prior_selected = {f"https://other.example/prior/{i}" for i in range(22)}
    result = check_recent_duplicate(basket, prior_selected=prior_selected)
    assert result is None, (
        f"OLD-SHAPE WITNESS regressed: title-keyword false-skip is back "
        f"(prior title was {PRIOR_TITLE_WITNESS!r}); got {result!r}"
    )


# ── (ii) NEW PUBLISHES: fresh basket L1..L22, prior_selected non-overlapping
#         -> novelty 1.0 -> publish (None). ──────────────────────────────────
def test_new_basket_publishes():
    links = [f"https://news.example/today/L{i}" for i in range(1, 23)]
    basket = _basket(links)
    prior_selected = {f"https://news.example/yesterday/Y{i}" for i in range(1, 23)}
    assert check_recent_duplicate(basket, prior_selected=prior_selected) is None


# ── (iii) GENUINE DUP SKIPS: every basket URL already in prior_selected
#          (basket fully recycled) -> novelty 0.0 -> skip (truthy marker). ────
def test_recycled_basket_skips():
    links = [f"https://news.example/recycled/R{i}" for i in range(1, 23)]
    basket = _basket(links)
    prior_selected = set(links)            # 100% recycled
    result = check_recent_duplicate(basket, prior_selected=prior_selected)
    assert result, f"recycled basket should SKIP (truthy), got {result!r}"
    # Contract: marker must carry the keys main.py:185-196 reads.
    assert "created_at" in result and "title" in result
