# ============================================================
# GNI Source Credibility Model — Day 12
# Calculates per-source GPVS contribution weekly
# Sources that appear in accurate reports get higher scores
# Integrates with intelligence_funnel.py source weights
# ============================================================

import os
import sys
import json
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analysis.source_weights import norm

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")


def _get_client():
    try:
        from supabase import create_client
        if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
            return None
        return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    except Exception:
        return None


def calculate_credibility_scores() -> dict:
    """
    Calculate credibility scores for all sources based on GPVS outcomes.

    Logic:
    1. Get all pipeline_runs that have a linked report with a GPVS outcome
    2. For each run, get the articles that were selected (stage4_selected=True)
    3. If the report was accurate (direction_correct_3d=True), credit those sources
    4. Score = gpvs_wins / gpvs_total (with smoothing)

    Returns dict of {norm(source): {"score": float, "wins": int, "total": int}}.
    wins/total are the REAL per-source counts. They used to be computed here and
    then discarded, with the caller substituting a GLOBAL outcome count as each
    source's per-source stat (I-3) — which /health then displayed.
    """
    client = _get_client()
    if not client:
        return {}

    try:
        # Get reports with GPVS outcomes
        outcomes = client.table("prediction_outcomes")             .select("report_id, direction_correct_3d, direction_correct_7d, accuracy_score")             .execute()

        if not outcomes.data:
            print("  ⚠️  No GPVS outcomes yet — credibility scores not updated")
            return {}

        # Get pipeline runs with their report IDs
        runs = client.table("pipeline_runs")             .select("id, report_id")             .execute()

        run_map = {r["id"]: r["report_id"] for r in (runs.data or [])}
        outcome_map = {o["report_id"]: o for o in outcomes.data}

        # Get all selected articles per run
        source_stats = {}

        for run_id, report_id in run_map.items():
            if not report_id or report_id not in outcome_map:
                continue

            outcome = outcome_map[report_id]
            is_accurate = outcome.get("direction_correct_3d", False)

            # Get selected articles for this run
            articles = client.table("pipeline_articles")                 .select("source")                 .eq("run_id", run_id)                 .eq("stage4_selected", True)                 .execute()

            for art in (articles.data or []):
                raw_source = art.get("source")
                if not raw_source:
                    continue
                source = norm(raw_source)
                if source not in source_stats:
                    source_stats[source] = {"wins": 0, "total": 0}
                source_stats[source]["total"] += 1
                if is_accurate:
                    source_stats[source]["wins"] += 1

        if not source_stats:
            print("  ⚠️  No source contribution data found")
            return {}

        # Calculate credibility scores with Laplace smoothing
        scores = {}
        for source, stats in source_stats.items():
            wins = stats["wins"]
            total = stats["total"]
            # Laplace smoothing: add 1 win and 2 total to avoid 0/0
            score = (wins + 1) / (total + 2)
            scores[source] = {
                "score": round(score, 3),
                "wins": wins,
                "total": total,
            }

        return scores

    except Exception as e:
        print(f"  ⚠️  Credibility calculation failed: {e}")
        return {}


def calculate_topic_scores() -> dict:
    """
    Calculate per-topic and per-location accuracy for each source.
    Uses report location_name and title keywords to assign topics.
    Returns dict: {source: {top_topics, topic_scores, location_scores}}
    """
    client = _get_client()
    if not client:
        return {}

    try:
        # Get reports with GPVS outcomes + location data
        reports_result = client.table("reports") \
            .select("id, location_name, title, sentiment") \
            .execute()

        outcomes_result = client.table("prediction_outcomes") \
            .select("report_id, direction_correct_3d, accuracy_score") \
            .execute()

        runs_result = client.table("pipeline_runs") \
            .select("id, report_id") \
            .execute()

        if not outcomes_result.data or not runs_result.data:
            return {}

        report_map = {r["id"]: r for r in (reports_result.data or [])}
        outcome_map = {o["report_id"]: o for o in outcomes_result.data}
        run_map = {r["id"]: r["report_id"] for r in runs_result.data}

        # Topic keywords for classification
        TOPIC_KEYWORDS = {
            "Iran": ["iran", "tehran", "hormuz", "persian"],
            "China": ["china", "beijing", "taiwan", "xi jinping"],
            "Russia": ["russia", "moscow", "ukraine", "putin"],
            "Europe": ["europe", "eu", "nato", "germany", "france", "uk"],
            "Middle East": ["middle east", "israel", "gaza", "syria", "saudi"],
            "Energy": ["oil", "gas", "opec", "energy", "crude", "pipeline"],
            "AI & Tech": ["artificial intelligence", "ai", "semiconductor", "chip", "cyber"],
            "Finance": ["market", "inflation", "fed", "interest rate", "tariff", "trade"],
            "Asia Pacific": ["asia", "japan", "korea", "pacific", "india", "asean"],
        }

        # source -> {topic -> {wins, total}, location -> {wins, total}}
        source_topics: dict = {}
        source_locations: dict = {}

        for run_id, report_id in run_map.items():
            if not report_id or report_id not in outcome_map:
                continue

            outcome = outcome_map[report_id]
            is_accurate = outcome.get("direction_correct_3d", False)
            report = report_map.get(report_id, {})
            location = report.get("location_name", "") or ""
            title = (report.get("title", "") or "").lower()

            # Detect topics from title
            matched_topics = []
            for topic, keywords in TOPIC_KEYWORDS.items():
                if any(kw in title for kw in keywords):
                    matched_topics.append(topic)
            if not matched_topics:
                matched_topics = ["General"]

            # Get selected articles for this run
            articles = client.table("pipeline_articles") \
                .select("source") \
                .eq("run_id", run_id) \
                .eq("stage4_selected", True) \
                .execute()

            for art in (articles.data or []):
                raw_source = art.get("source")
                if not raw_source:
                    continue
                source = norm(raw_source)

                # Topic tracking
                if source not in source_topics:
                    source_topics[source] = {}
                for topic in matched_topics:
                    if topic not in source_topics[source]:
                        source_topics[source][topic] = {"wins": 0, "total": 0}
                    source_topics[source][topic]["total"] += 1
                    if is_accurate:
                        source_topics[source][topic]["wins"] += 1

                # Location tracking
                if location:
                    if source not in source_locations:
                        source_locations[source] = {}
                    if location not in source_locations[source]:
                        source_locations[source][location] = {"wins": 0, "total": 0}
                    source_locations[source][location]["total"] += 1
                    if is_accurate:
                        source_locations[source][location]["wins"] += 1

        # Convert to scores
        result = {}
        all_sources = set(list(source_topics.keys()) + list(source_locations.keys()))

        for source in all_sources:
            # Topic scores
            topic_scores = {}
            top_topics = []
            if source in source_topics:
                for topic, stats in source_topics[source].items():
                    if stats["total"] >= 2:  # min 2 appearances to score
                        score = round((stats["wins"] + 1) / (stats["total"] + 2), 3)
                        topic_scores[topic] = score
                # Top 3 topics by total appearances
                sorted_topics = sorted(
                    source_topics[source].items(),
                    key=lambda x: x[1]["total"],
                    reverse=True
                )
                top_topics = [t for t, _ in sorted_topics[:3]]

            # Location scores
            loc_scores = {}
            if source in source_locations:
                for loc, stats in source_locations[source].items():
                    if stats["total"] >= 2:
                        score = round((stats["wins"] + 1) / (stats["total"] + 2), 3)
                        loc_scores[loc] = score

            result[source] = {
                "top_topics": top_topics,
                "topic_scores": topic_scores,
                "location_scores": loc_scores,
            }

        return result

    except Exception as e:
        print(f"  Warning: Topic score calculation failed: {e}")
        return {}


def update_credibility_scores() -> bool:
    """
    Calculate and save credibility scores to the source_credibility table.
    Called every 10th pipeline run (main.py) or on demand.

    Writes source_credibility ONLY. The weight column is owned exclusively by
    the GPVS EMA path in analysis.source_weights (single-writer principle,
    bridge (a)): this function used to overwrite weight with 0.5 + cred*1.5,
    a memoryless formula that erased the EMA's learning on whichever run
    landed last. Credibility is dashboard evidence, not a weight mover — both
    signals derive from the same GPVS outcomes, so feeding one into the other
    double-counts the same evidence.
    """
    client = _get_client()
    if not client:
        return False

    print("  📊 Calculating source credibility scores...")
    stats = calculate_credibility_scores()

    if not stats:
        print("  ⚠️  No scores to update — insufficient GPVS data")
        return False

    try:
        now = datetime.now(timezone.utc).isoformat()

        for source, stat in stats.items():
            # Real per-source wins/total, straight from the contribution scan
            # (I-3). No global outcome re-fetch: the old loop refetched the
            # whole prediction_outcomes table once per source (~51 fetches)
            # only to store the same global count on every row.
            client.table("source_credibility").upsert({
                "source": source,
                "credibility_score": stat["score"],
                "gpvs_wins": stat["wins"],
                "gpvs_total": stat["total"],
                "last_calculated": now,
            }).execute()

        print(f"  ✅ Credibility scores updated for {len(stats)} sources")

        # Update topic and location scores
        print("  📍 Calculating per-topic accuracy...")
        topic_data = calculate_topic_scores()
        for source, data in topic_data.items():
            try:
                client.table("source_credibility").upsert({
                    "source": source,
                    "top_topics": data["top_topics"],
                    "topic_scores": data["topic_scores"],
                    "location_scores": data["location_scores"],
                    "last_calculated": now,
                }).execute()
            except Exception as te:
                print(f"  Warning: topic update for {source}: {te}")
        print(f"  ✅ Topic scores updated for {len(topic_data)} sources")
        return True

    except Exception as e:
        print(f"  ⚠️  Credibility update failed: {e}")
        return False


def get_credibility_status() -> list:
    """Return current credibility scores for /health page."""
    client = _get_client()
    if not client:
        return []
    try:
        result = client.table("source_credibility") \
            .select("source, credibility_score, gpvs_wins, gpvs_total, top_topics, topic_scores, location_scores, last_calculated") \
            .order("credibility_score", desc=True) \
            .execute()
        return result.data or []
    except Exception:
        return []


def seed_initial_credibility() -> bool:
    """
    Seed BOTH trust tables from the collector's canonical roster (I-6) at
    neutral: 0.5 credibility (Laplace prior at 0/0) / 1.0 weight. Called on every pipeline run.

    The old hand-maintained 13-source list was a fossil — it had drifted to
    name sources long since departed (Bloomberg, Wired, Straits Times) while
    missing ~30 live ones, so most of the roster had no seeded row anywhere.
    The roster is imported from the collector, never copied, so it cannot
    drift again.

    INSERT-if-missing only: an existing row carries learned history and is
    never reset to neutral. The source_weights half is delegated to
    analysis.source_weights, which owns the weight column — this module does
    not write that table (single-writer principle, bridge (a)).
    """
    client = _get_client()
    if not client:
        return False

    try:
        from analysis.source_weights import get_roster_sources, seed_roster_weights
        roster = {norm(s) for s in get_roster_sources()}

        existing = client.table("source_credibility").select("source").execute()
        existing_sources = {norm(r["source"]) for r in (existing.data or [])}

        now = datetime.now(timezone.utc).isoformat()
        new_sources = sorted(roster - existing_sources)

        if new_sources:
            client.table("source_credibility").insert([
                {
                    "source": s,
                    "credibility_score": 0.5,
                    "gpvs_wins": 0,
                    "gpvs_total": 0,
                    "last_calculated": now,
                }
                for s in new_sources
            ]).execute()
            print(f"  ✅ Seeded credibility for {len(new_sources)} sources")

        seed_roster_weights(client)
        return True

    except Exception as e:
        print(f"  ⚠️  Seed failed: {e}")
        return False


if __name__ == "__main__":
    print("\U0001f4ca GNI Source Credibility Model\n")
    seed_initial_credibility()
    status = get_credibility_status()
    if status:
        print(f"  {'Source':<30} {'Score':>8} {'Wins':>6} {'Total':>6}")
        print("  " + "-" * 55)
        for s in status:
            print(f"  {s['source']:<30} {s['credibility_score']:>8.3f} {s['gpvs_wins']:>6} {s['gpvs_total']:>6}")
    else:
        print("  No credibility data yet")
