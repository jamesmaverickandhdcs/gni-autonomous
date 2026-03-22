# ============================================================
# GNI Code Fix Suggester - Phase 1
# Reads pipeline errors, suggests fixes, saves for human review.
# NO code is written until a human approves the suggestion.
# L23: Model name from env var
# ============================================================

import os
import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

BUG_PATTERNS = [
    {"class": "missing_env_var",
     "patterns": ["not defined", "not found in environment", "API_KEY"],
     "description": "Environment variable missing or undefined",
     "affected_file": ".env / GitHub Secrets"},
    {"class": "model_deprecated",
     "patterns": ["model_not_found", "deprecated", "does not exist"],
     "description": "Groq model name deprecated or unavailable",
     "affected_file": "ai_engine/analysis/nexus_analyzer.py"},
    {"class": "rss_feed_broken",
     "patterns": ["bozo", "0 articles", "Feed error", "RSS_SOURCE_FAILURE"],
     "description": "RSS feed returning 0 articles or malformed XML",
     "affected_file": "ai_engine/collectors/rss_collector.py"},
    {"class": "db_column_missing",
     "patterns": ["PGRST204", "schema cache", "Could not find"],
     "description": "Supabase column referenced in code does not exist in DB",
     "affected_file": "Supabase schema / supabase_saver.py"},
    {"class": "json_parse_failed",
     "patterns": ["Failed to parse LLM", "JSONDecodeError", "invalid JSON"],
     "description": "LLM returned invalid or malformed JSON",
     "affected_file": "ai_engine/analysis/nexus_analyzer.py"},
]


def _get_client():
    from supabase import create_client
    url = os.getenv("SUPABASE_URL", "")
    key = os.getenv("SUPABASE_SERVICE_KEY", "")
    if not url or not key:
        return None
    try:
        return create_client(url, key)
    except Exception:
        return None


def _classify_error(error_message):
    if not error_message:
        return None
    error_lower = error_message.lower()
    for pattern in BUG_PATTERNS:
        if any(p.lower() in error_lower for p in pattern["patterns"]):
            return pattern
    return None


def _call_groq_for_fix(bug_class, error_message, affected_file):
    if not GROQ_API_KEY:
        return None
    prompt = (
        "You are a senior Python developer reviewing a pipeline error.\n"
        "Bug class: " + bug_class + "\n"
        "Error: " + error_message[:300] + "\n"
        "File: " + affected_file + "\n\n"
        "Give a minimal fix in 2-3 sentences: (1) exact cause, "
        "(2) exact fix, (3) how to verify. No refactoring."
    )
    try:
        response = requests.post(
            GROQ_URL,
            headers={"Authorization": "Bearer " + GROQ_API_KEY,
                     "Content-Type": "application/json"},
            json={"model": GROQ_MODEL,
                  "messages": [{"role": "user", "content": prompt}],
                  "temperature": 0.2, "max_tokens": 300},
            timeout=15,
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("  Warning: Groq fix suggestion failed: " + str(e))
    return None


def run_code_fix_suggester():
    client = _get_client()
    if not client:
        print("  Warning: Cannot connect to Supabase for fix suggestions")
        return []

    print("  Checking for pipeline errors to suggest fixes...")
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()

    try:
        logs = client.table("runtime_logs").select("error_message, run_at") \
            .eq("status", "failed").gte("run_at", cutoff) \
            .order("run_at", desc=True).limit(5).execute()
        errors = [r["error_message"] for r in (logs.data or []) if r.get("error_message")]
    except Exception as e:
        print("  Warning: Could not fetch runtime logs: " + str(e))
        return []

    if not errors:
        print("  No recent pipeline failures found")
        return []

    suggestions = []
    for error_message in errors:
        bug = _classify_error(error_message)
        if not bug:
            continue

        try:
            existing = client.table("code_fix_suggestions").select("id") \
                .eq("bug_class", bug["class"]).eq("status", "pending").execute()
            if existing.data:
                print("  Skipping " + bug["class"] + " - already pending")
                continue
        except Exception:
            pass

        print("  Generating suggestion for: " + bug["class"])
        fix_text = _call_groq_for_fix(bug["class"], error_message, bug["affected_file"])
        if not fix_text:
            fix_text = bug["description"] + " - manual review required"

        record = {"bug_class": bug["class"], "error_message": error_message[:500],
                  "suggested_fix": fix_text, "affected_file": bug["affected_file"],
                  "status": "pending"}

        try:
            client.table("code_fix_suggestions").insert(record).execute()
            suggestions.append(record)
            print("  Saved: " + bug["class"])
        except Exception as e:
            print("  Warning: Could not save suggestion: " + str(e))

    if suggestions:
        print(str(len(suggestions)) + " suggestion(s) saved - awaiting human review")
    return suggestions


def get_pending_suggestions():
    client = _get_client()
    if not client:
        return []
    try:
        result = client.table("code_fix_suggestions").select("*") \
            .eq("status", "pending").order("created_at", desc=True).execute()
        return result.data or []
    except Exception:
        return []


if __name__ == "__main__":
    print("\nGNI Code Fix Suggester - Manual Run\n")
    run_code_fix_suggester()
    pending = get_pending_suggestions()
    print("\nPending: " + str(len(pending)))
    for s in pending:
        print("  [" + s["bug_class"] + "] " + s["suggested_fix"][:80])
