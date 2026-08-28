# replay_scorer.py -- S87. Re-score stored history with the LIVE scorer.
#
# READ-ONLY. No DB write, no Groq call, no network beyond Supabase SELECT.
# Safe to run at any time; costs nothing.
#
# WHY: escalation_scorer is keyword-deterministic, so any change to it can be
# evaluated against every stored run BEFORE it ships. At S87 this falsified the
# 2026-03-24 'Fix 2' design in one command: simulated final score was 10.0 on
# 191/191 runs, identical to production. Five months of belief, one measurement.
#
# It IMPORTS score_escalation -- never re-implements it. A copy that drifts from
# the original measures nothing. Keep it that way.
#
# Usage: python tools/replay_scorer.py   (from repo root, venv active)
# Source: pipeline_articles where stage4_selected -- the exact set the scorer saw.
# Coverage starts 2026-05-24; there is NO pre-crisis baseline in this corpus.

import sys, os, collections
sys.path.insert(0, os.path.abspath('ai_engine'))
from analysis.escalation_scorer import (score_escalation,
    TECH_SIGNALS, GEO_SIGNALS, FIN_SIGNALS, CRITICAL_COMBOS)
from analysis.supabase_saver import get_client

c = get_client()
assert c, "NO CLIENT -- STOP"
rows, step, off = [], 1000, 0
while True:
    r = (c.table("pipeline_articles")
          .select("run_id,title,summary,created_at")
          .eq("stage4_selected", True).order("created_at")
          .range(off, off + step - 1).execute())
    if not r.data:
        break
    rows += r.data
    if len(r.data) < step:
        break
    off += step
runs = collections.defaultdict(list)
for a in rows:
    runs[a["run_id"]].append(a)
print("articles=%d runs=%d" % (len(rows), len(runs)))

final_c, base_ge10, div3, combo_c, sizes = collections.Counter(), 0, 0, collections.Counter(), collections.Counter()
word = collections.Counter()
combo_fire = collections.Counter()
for rid, arts in runs.items():
    out = score_escalation(arts)
    b = out.get("score_breakdown", {})
    final_c[out["escalation_score"]] += 1
    sizes[len(arts)] += 1
    if (b.get("base_total") or 0) >= 10.0:
        base_ge10 += 1
    if (b.get("diversity_bonus") or 0) == 3.0:
        div3 += 1
    combo_c[b.get("combo_bonus")] += 1
    txt = " ".join((a.get("title") or "") + " " + (a.get("summary") or "") for a in arts).lower()
    for s in list(TECH_SIGNALS) + list(GEO_SIGNALS) + list(FIN_SIGNALS):
        if s in txt:
            word[s] += 1
    for kws, bonus in CRITICAL_COMBOS:
        if all(k in txt for k in kws):
            combo_fire["+".join(kws)] += 1

n = len(runs)
print("\n-- articles per run --", dict(sizes.most_common(5)))
print("-- final score --", dict(sorted(final_c.items())))
print("-- base_total >= 10.0 : %d/%d (%.0f%%)" % (base_ge10, n, 100.0*base_ge10/n))
print("-- diversity == 3.0   : %d/%d (%.0f%%)" % (div3, n, 100.0*div3/n))
print("-- combo_bonus --", dict(sorted((k, v) for k, v in combo_c.items() if k is not None)))
print("\n-- combos firing --")
for k, v in combo_fire.most_common(10):
    print("   %-28s %4d  %5.1f%%" % (k, v, 100.0*v/n))
with open("../keyword_rates.tsv", "w", encoding="utf-8") as f:
    for s, v in word.most_common():
        f.write("%s\t%d\t%.1f\n" % (s, v, 100.0*v/n))
print("\n-- top 20 keywords by firing rate (full table -> ../keyword_rates.tsv) --")
for s, v in word.most_common(20):
    print("   %-24s %4d  %5.1f%%" % (s, v, 100.0*v/n))
print("-- keywords that NEVER fire: %d" % (len(set(TECH_SIGNALS)|set(GEO_SIGNALS)|set(FIN_SIGNALS)) - len(word)))
