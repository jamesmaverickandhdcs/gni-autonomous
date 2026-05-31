# ============================================================
# GNI Entity Graph -- B3 Phase 3 core (the invisible-links engine)
#
# Takes per-article entity sets (from entity_extractor.extract_entities)
# and builds the co-occurrence network GNI currently throws away. Surfaces
# what no single article shows:
#
#   1. HIDDEN BROKER (centrality)   -- high betweenness, low degree.
#      The entity quietly connecting otherwise-separate stories. NOT the
#      most-mentioned (that is degree = "in the news a lot" = you know it).
#      Betweenness finds the connector you DON'T already see. = PHI-002
#      Cui Bono made structural: who sits on the paths between events.
#
#   2. CONVERGENCE (temporal)       -- two previously-disconnected clusters
#      that newly link this run. The moment separate threads become one
#      story = the weak signal a senior analyst lives for. = PHI-001
#      digging behind the screen before the link is obvious.
#
#   3. BIAS-LAUNDERING GUARD        -- the fourth-analyst's warning, in code.
#      A centrality finding is ONLY trustworthy if it is not just an artifact
#      of one source over-covering one entity. Every broker finding carries a
#      source-spread check: if the entity's mentions come overwhelmingly from
#      ONE source, the finding is flagged 'POSSIBLE_SOURCE_BIAS' -- the graph
#      refuses to launder source-coverage bias as structural truth. This is
#      PHI-002 turned on GNI's own conclusion. Without it, the graph becomes
#      the pretense it was built to detect.
#
# STANDALONE: nothing in the pipeline calls this yet. The fresh-session task
# is ONLY to wire it (store entity sets per article, feed them here, schedule
# it). The hard reasoning is HERE, proven, so the wiring is low-context work.
# Run `python entity_graph.py` to prove it (self-test at bottom).
# ============================================================
import networkx as nx
from itertools import combinations


def build_graph(article_entity_sets: list[dict]) -> nx.Graph:
    """
    Build a weighted co-occurrence graph from per-article entity data.

    article_entity_sets: list of dicts, each:
        {"entities": set[str], "source": str}
    (entities from entity_extractor; source for the bias guard)

    Edge weight = number of articles in which the two entities co-occur.
    Node attribute 'sources' = dict of which sources mentioned the entity
    (the raw material for the bias-laundering guard).
    """
    G = nx.Graph()
    for art in article_entity_sets:
        ents = sorted(art.get("entities") or [])
        src = art.get("source", "Unknown")
        for e in ents:
            if not G.has_node(e):
                G.add_node(e, sources={})
            G.nodes[e]["sources"][src] = G.nodes[e]["sources"].get(src, 0) + 1
        for a, b in combinations(ents, 2):
            if G.has_edge(a, b):
                G[a][b]["weight"] += 1
            else:
                G.add_edge(a, b, weight=1)
    return G


def _source_spread(node_sources: dict) -> tuple[float, str]:
    """
    Return (dominant_share, dominant_source) for an entity's mentions.
    dominant_share near 1.0 => almost all mentions from ONE source
    => a centrality finding about this entity may be source-bias, not truth.
    """
    if not node_sources:
        return 0.0, ""
    total = sum(node_sources.values())
    dom_src = max(node_sources, key=node_sources.get)
    return node_sources[dom_src] / total, dom_src


def find_hidden_brokers(G: nx.Graph, min_betweenness: float = 0.10,
                        bias_threshold: float = 0.75) -> list[dict]:
    """
    Hidden broker = entity with HIGH betweenness but comparatively LOW degree.
    It connects clusters without being the most-connected node itself --
    the non-obvious hub. Each finding carries a bias-laundering check.

    Returns findings sorted by betweenness desc. Each:
      {entity, betweenness, degree, broker_ratio, source_spread,
       dominant_source, flag}
    flag = 'POSSIBLE_SOURCE_BIAS' if mentions overwhelmingly from one source,
           else 'OK'.
    """
    if G.number_of_nodes() < 3:
        return []

    betw = nx.betweenness_centrality(G, weight="weight", normalized=True)
    deg = dict(G.degree())
    max_deg = max(deg.values()) or 1

    findings = []
    for node, b in betw.items():
        if b < min_betweenness:
            continue
        norm_deg = deg[node] / max_deg
        broker_ratio = b / (norm_deg + 0.01)

        spread, dom_src = _source_spread(G.nodes[node].get("sources", {}))
        flag = "POSSIBLE_SOURCE_BIAS" if spread >= bias_threshold else "OK"

        findings.append({
            "entity": node,
            "betweenness": round(b, 4),
            "degree": deg[node],
            "broker_ratio": round(broker_ratio, 3),
            "source_spread": round(spread, 3),
            "dominant_source": dom_src,
            "flag": flag,
        })

    findings.sort(key=lambda f: f["betweenness"], reverse=True)
    return findings


def detect_convergence(prev_G: nx.Graph, curr_G: nx.Graph) -> list[dict]:
    """
    Convergence = two entities that were in SEPARATE connected components in
    prev_G but are now in the SAME component in curr_G (a new bridge formed).
    The moment two previously-unrelated story-clusters become one.

    Compares only entities present in both snapshots (new entities are not
    'convergence' -- they are just new).
    """
    if prev_G is None or prev_G.number_of_nodes() == 0:
        return []

    def comp_map(G):
        m = {}
        for i, comp in enumerate(nx.connected_components(G)):
            for n in comp:
                m[n] = i
        return m

    prev_comp = comp_map(prev_G)
    curr_comp = comp_map(curr_G)

    shared = [n for n in curr_G.nodes() if n in prev_comp]
    findings = []
    for a, b in combinations(sorted(shared), 2):
        was_separate = prev_comp[a] != prev_comp[b]
        now_together = curr_comp.get(a) == curr_comp.get(b)
        if was_separate and now_together:
            findings.append({
                "entity_a": a,
                "entity_b": b,
                "detail": (f"{a} and {b} were in separate story-clusters; "
                           f"this run they connected -- convergence"),
            })
    return findings


if __name__ == "__main__":
    print("=== entity_graph self-test ===")
    passed = 0
    total = 0

    arts = [
        {"entities": {"United States", "NATO", "Ukraine"}, "source": "BBC"},
        {"entities": {"United States", "NATO"}, "source": "France 24"},
        {"entities": {"NATO", "Ukraine"}, "source": "DW News"},
        {"entities": {"China", "Taiwan", "Japan"}, "source": "Nikkei Asia"},
        {"entities": {"China", "Taiwan"}, "source": "The Diplomat"},
        {"entities": {"Taiwan", "Japan"}, "source": "CNBC World"},
        {"entities": {"Ukraine", "Russia"}, "source": "Al Jazeera"},
        {"entities": {"Russia", "China"}, "source": "Foreign Policy"},
    ]
    G = build_graph(arts)
    brokers = find_hidden_brokers(G, min_betweenness=0.05)
    total += 1
    top = brokers[0]["entity"] if brokers else None
    if top == "Russia":
        passed += 1
        print(f"  [PASS] hidden broker = Russia (bridges two clusters via betweenness)")
    else:
        print(f"  [FAIL] expected broker Russia, got {top}; all: {[b['entity'] for b in brokers]}")

    arts2 = [
        {"entities": {"Iran", "Israel"}, "source": "RT"},
        {"entities": {"Iran", "Saudi Arabia"}, "source": "RT"},
        {"entities": {"Iran", "United States"}, "source": "RT"},
        {"entities": {"Iran", "Russia"}, "source": "RT"},
        {"entities": {"Israel", "United States"}, "source": "BBC"},
        {"entities": {"Saudi Arabia", "United States"}, "source": "France 24"},
    ]
    G2 = build_graph(arts2)
    brokers2 = find_hidden_brokers(G2, min_betweenness=0.05, bias_threshold=0.75)
    total += 1
    iran = next((b for b in brokers2 if b["entity"] == "Iran"), None)
    if iran and iran["flag"] == "POSSIBLE_SOURCE_BIAS":
        passed += 1
        print(f"  [PASS] bias guard: Iran flagged POSSIBLE_SOURCE_BIAS "
              f"(spread={iran['source_spread']} from {iran['dominant_source']})")
    else:
        print(f"  [FAIL] expected Iran flagged source-bias, got {iran}")

    total += 1
    us = next((b for b in brokers2 if b["entity"] == "United States"), None)
    if us is None or us["flag"] == "OK":
        passed += 1
        print(f"  [PASS] bias guard: diverse-sourced entity NOT false-flagged")
    else:
        print(f"  [FAIL] United States wrongly flagged: {us}")

    prev_arts = [
        {"entities": {"China", "Taiwan"}, "source": "X"},
        {"entities": {"Iran", "Israel"}, "source": "Y"},
    ]
    curr_arts = [
        {"entities": {"China", "Taiwan"}, "source": "X"},
        {"entities": {"Iran", "Israel"}, "source": "Y"},
        {"entities": {"Taiwan", "Iran"}, "source": "Z"},
    ]
    pG = build_graph(prev_arts)
    cG = build_graph(curr_arts)
    conv = detect_convergence(pG, cG)
    total += 1
    pairs = {(c["entity_a"], c["entity_b"]) for c in conv}
    if ("Iran", "Taiwan") in pairs or ("China", "Israel") in pairs or len(conv) > 0:
        passed += 1
        print(f"  [PASS] convergence detected: {len(conv)} newly-bridged pair(s)")
    else:
        print(f"  [FAIL] expected convergence, got none")

    conv_none = detect_convergence(cG, cG)
    total += 1
    if len(conv_none) == 0:
        passed += 1
        print(f"  [PASS] no false convergence when graph unchanged")
    else:
        print(f"  [FAIL] false convergence: {conv_none}")

    print(f"=== {passed}/{total} passed ===")
