"""
GNI Source Topic Accuracy Tracking
Adds per-topic and per-location accuracy to credibility_model.py
New columns: top_topics, topic_scores, location_scores
GNI-R-008: ALTER TABLE ran first -- confirmed
GNI-R-037: Full file read done
GNI-R-062: py_compile check at end
Run from: C:\HDCS_Project\03\GNI_Autonomous
Usage: python add_source_topic_tracking.py
"""

import os
import py_compile

file_path = os.path.join("ai_engine", "analysis", "credibility_model.py")

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

fixes = 0

# Fix 1: Add calculate_topic_scores() function before update_credibility_scores()
old1 = "def update_credibility_scores() -> bool:"
new1 = """def calculate_topic_scores() -> dict:
    \"\"\"
    Calculate per-topic and per-location accuracy for each source.
    Uses report location_name and title keywords to assign topics.
    Returns dict: {source: {top_topics, topic_scores, location_scores}}
    \"\"\"
    client = _get_client()
    if not client:
        return {}

    try:
        # Get reports with GPVS outcomes + location data
        reports_result = client.table("reports") \\
            .select("id, location_name, title, sentiment") \\
            .execute()

        outcomes_result = client.table("prediction_outcomes") \\
            .select("report_id, direction_correct_3d, accuracy_score") \\
            .execute()

        runs_result = client.table("pipeline_runs") \\
            .select("id, report_id") \\
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
            articles = client.table("pipeline_articles") \\
                .select("source") \\
                .eq("run_id", run_id) \\
                .eq("stage4_selected", True) \\
                .execute()

            for art in (articles.data or []):
                source = art["source"]

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


def update_credibility_scores() -> bool:"""

if old1 in content:
    content = content.replace(old1, new1)
    fixes += 1
    print("OK Fix 1: Added calculate_topic_scores() function")

# Fix 2: Call calculate_topic_scores() inside update_credibility_scores()
# and save results to new columns
old2 = '        print(f"  \u2705 Source weights updated based on credibility")\n        return True'
new2 = '        print(f"  \u2705 Source weights updated based on credibility")\n\n        # Update topic and location scores\n        print("  \U0001f4cd Calculating per-topic accuracy...")\n        topic_data = calculate_topic_scores()\n        for source, data in topic_data.items():\n            try:\n                client.table("source_credibility").upsert({\n                    "source": source,\n                    "top_topics": data["top_topics"],\n                    "topic_scores": data["topic_scores"],\n                    "location_scores": data["location_scores"],\n                    "last_calculated": now,\n                }).execute()\n            except Exception as te:\n                print(f"  Warning: topic update for {source}: {te}")\n        print(f"  \u2705 Topic scores updated for {len(topic_data)} sources")\n        return True'

if old2 in content:
    content = content.replace(old2, new2)
    fixes += 1
    print("OK Fix 2: Added topic score update inside update_credibility_scores()")

# Fix 3: Update get_credibility_status() to include new columns
old3 = '        result = client.table("source_credibility")             .select("source, credibility_score, gpvs_wins, gpvs_total, last_calculated")             .order("credibility_score", desc=True)             .execute()'
new3 = '        result = client.table("source_credibility") \\\n            .select("source, credibility_score, gpvs_wins, gpvs_total, top_topics, topic_scores, location_scores, last_calculated") \\\n            .order("credibility_score", desc=True) \\\n            .execute()'

if old3 in content:
    content = content.replace(old3, new3)
    fixes += 1
    print("OK Fix 3: Updated get_credibility_status() to include new columns")

if fixes == 0:
    print("ERROR: No target blocks found -- file may have changed.")
    exit(1)

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print(f"OK Updated: {file_path} ({fixes} fixes applied)")

# GNI-R-062
py_compile.compile(file_path, doraise=True)
print("OK py_compile: syntax OK")
print("DONE. Now run: npm run build")
