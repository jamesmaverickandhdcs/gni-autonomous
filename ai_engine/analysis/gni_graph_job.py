# ============================================================
# GNI Entity Graph Job -- B3 Phase 3 wiring (STANDALONE)
#
# Reads the SCORED set (stage1+1b+2 passed, ~359/run -- NOT just the 22
# selected; betweenness needs the full vetted field) from the latest
# pipeline run, builds the co-occurrence graph, finds hidden brokers
# (with the bias-laundering guard, W4), detects convergence vs the prior
# run's scored set (W5: empty first run is correct), and saves ONE snapshot
# row to gni_entity_graph.
#
# Does NOT touch the pipeline path. Reads pipeline_articles, writes
# gni_entity_graph only. Run standalone or via gni_graph.yml.
# ============================================================
import sys
import os
from datetime import datetime, timezone

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.supabase_saver import get_client
from analysis.entity_graph import build_graph, find_hidden_brokers, detect_convergence


def _fetch_scored_sets(client, run_id: str) -> list[dict]:
    """All scored-set articles for a run -> [{entities, source}] for build_graph.
    Scored set = passed stage1 + stage1b + stage2 (reached significance scoring)."""
    res = client.table("pipeline_articles") \
        .select("entities, source") \
        .eq("run_id", run_id) \
        .eq("stage1_passed", True) \
        .eq("stage1b_passed", True) \
        .eq("stage2_passed", True) \
        .execute()
    rows = res.data or []
    # entities is jsonb (list); build_graph accepts list or set. Guard None.
    return [{"entities": r.get("entities") or [], "source": r.get("source", "Unknown")}
            for r in rows]


def _latest_two_run_ids(client) -> tuple:
    """(current_run_id, prev_run_id|None) -- latest TWO runs that actually have
    articles. Adaptive/Heartbeat runs create a pipeline_runs row but no article
    trace, so we select distinct run_ids straight from pipeline_articles (only
    article-producing Intelligence runs appear there). GNI-R-242: edf4a78d was an
    adaptive run with 0 articles -- selecting from pipeline_runs picked it wrongly."""
    res = client.table("pipeline_articles") \
        .select("run_id, created_at") \
        .order("created_at", desc=True) \
        .limit(2000) \
        .execute()
    rows = res.data or []
    seen = []
    for r in rows:
        rid = r.get("run_id")
        if rid and rid not in seen:
            seen.append(rid)
        if len(seen) >= 2:
            break
    cur = seen[0] if len(seen) >= 1 else None
    prev = seen[1] if len(seen) >= 2 else None
    return cur, prev


def run_graph_job() -> bool:
    print("=" * 60)
    print("GNI Entity Graph Job -- B3 Phase 3")
    print(f"  Start: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    client = get_client()
    if not client:
        print("  ERROR: no Supabase client")
        return False

    cur_run, prev_run = _latest_two_run_ids(client)
    if not cur_run:
        print("  ERROR: no pipeline_runs found")
        return False
    print(f"  Current run: {cur_run}")
    print(f"  Prev run:    {prev_run or '(none -- first graph, convergence empty by design)'}")

    cur_sets = _fetch_scored_sets(client, cur_run)
    print(f"  Scored articles (current): {len(cur_sets)}")
    if not cur_sets:
        print("  WARNING: no scored articles for current run -- nothing to graph")
        return False

    curr_G = build_graph(cur_sets)
    print(f"  Graph: {curr_G.number_of_nodes()} nodes, {curr_G.number_of_edges()} edges")

    brokers = find_hidden_brokers(curr_G)
    flagged = sum(1 for b in brokers if b["flag"] == "POSSIBLE_SOURCE_BIAS")
    print(f"  Hidden brokers: {len(brokers)} ({flagged} flagged POSSIBLE_SOURCE_BIAS)")

    convergence = []
    if prev_run:
        prev_sets = _fetch_scored_sets(client, prev_run)
        prev_G = build_graph(prev_sets)
        convergence = detect_convergence(prev_G, curr_G)
        print(f"  Convergence: {len(convergence)} newly-bridged pair(s)")
    else:
        print("  Convergence: skipped (no prior run)")

    record = {
        "run_id": cur_run,
        "node_count": curr_G.number_of_nodes(),
        "edge_count": curr_G.number_of_edges(),
        "brokers": brokers,
        "convergence": convergence,
        "source_window": f"scored set of run {str(cur_run)[:8]} ({len(cur_sets)} articles)",
    }
    client.table("gni_entity_graph").insert(record).execute()
    print(f"  OK snapshot saved to gni_entity_graph")
    print("=" * 60)

    if brokers:
        print("  Top brokers:")
        for b in brokers[:5]:
            print(f"    {b['entity']:18} betw={b['betweenness']} deg={b['degree']} "
                  f"ratio={b['broker_ratio']} [{b['flag']}]")
    return True


if __name__ == "__main__":
    ok = run_graph_job()
    sys.exit(0 if ok else 1)
