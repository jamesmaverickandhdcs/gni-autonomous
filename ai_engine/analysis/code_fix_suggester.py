# ============================================================
# GNI Code Fix Suggester - Phase 1
# Reads pipeline errors, suggests fixes, saves for human review.
# Admin-required actions protected by 4-strike confirmation system.
# L23: Model name from env var
# L56: Admin-only gate for secrets and infrastructure
# ============================================================

import os
import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")  # public channel
TELEGRAM_ADMIN_CHAT_ID = os.getenv("TELEGRAM_ADMIN_CHAT_ID", "")  # private admin only

# Bug classes that ALWAYS require admin action (L56)
# These touch secrets, credentials, or infrastructure
ADMIN_REQUIRED_CLASSES = [
    "missing_env_var",
    "db_credentials",
    "workflow_config",
]

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
    {"class": "groq_rate_limit",
     "patterns": ["rate limit", "429", "quota exceeded", "rate_limit_exceeded"],
     "description": "Groq API rate limit hit -- too many requests on free tier",
     "affected_file": "ai_engine/analysis/nexus_analyzer.py + frequency_controller.py"},
]

STRIKE_WARNINGS = [
    "",
    (
        "WARNING (Strike 1 of 3): This action involves secrets or infrastructure "
        "(.env / GitHub Secrets / credentials). "
        "Only an admin should proceed. "
        "Admin has been notified via Telegram. "
        "Pipeline continues as normal."
    ),
    (
        "WARNING (Strike 2 of 3): This action has been attempted TWICE. "
        "It touches secrets that control the entire system's identity. "
        "A wrong change here can break all API connections. "
        "Admin has been notified again via Telegram. "
        "Pipeline continues as normal."
    ),
    (
        "WARNING (Strike 3 of 3): This action has been attempted THREE TIMES. "
        "This is the final warning before the action is allowed on the next attempt. "
        "This touches .env files or GitHub Secrets. "
        "Only proceed on the 4th attempt if you are absolutely certain. "
        "Admin has been notified for the third time via Telegram. "
        "Pipeline continues as normal."
    ),
]

STRIKE_TELEGRAM_MESSAGES = [
    "",
    (
        "[GNI Admin Alert] Strike 1/3 - Admin action attempted\n"
        "Bug class: {bug_class}\n"
        "Affected: {affected_file}\n"
        "This touches secrets/credentials. Operator has been warned.\n"
        "Action NOT taken yet. Two more attempts before allowed."
    ),
    (
        "[GNI Admin Alert] Strike 2/3 - Admin action attempted AGAIN\n"
        "Bug class: {bug_class}\n"
        "Affected: {affected_file}\n"
        "This is the second attempt. One more before action is allowed.\n"
        "Verify the operator is authorised to proceed."
    ),
    (
        "[GNI Admin Alert] Strike 3/3 - FINAL WARNING\n"
        "Bug class: {bug_class}\n"
        "Affected: {affected_file}\n"
        "Next attempt will ALLOW this action to proceed.\n"
        "If this is not authorised, intervene now."
    ),
]

STRIKE4_TELEGRAM = (
    "[GNI Admin Alert] Action ALLOWED - 4th confirmation received\n"
    "Bug class: {bug_class}\n"
    "Affected: {affected_file}\n"
    "The operator confirmed 4 times. Action is now proceeding.\n"
    "Review the code_fix_suggestions table for full details."
)


def _send_telegram(message):
    # Send to ADMIN private chat only -- never to public channel
    admin_chat = TELEGRAM_ADMIN_CHAT_ID or TELEGRAM_CHAT_ID
    if not TELEGRAM_BOT_TOKEN or not admin_chat:
        return
    try:
        requests.post(
            "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage",
            json={"chat_id": admin_chat, "text": message,
                  "parse_mode": "HTML"},
            timeout=10,
        )
    except Exception:
        pass


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


def _is_admin_required(bug_class):
    return bug_class in ADMIN_REQUIRED_CLASSES


def _handle_strike(client, suggestion_id, bug_class, affected_file, current_strike):
    """
    Handle the strike system for admin-required actions.
    Returns True if action is allowed (strike 4), False if still protected.
    Pipeline continues regardless -- this is info only.
    """
    new_strike = current_strike + 1

    # Update strike count in DB
    try:
        client.table("code_fix_suggestions").update(
            {"strike_count": new_strike,
             "last_strike_at": datetime.now(timezone.utc).isoformat()}
        ).eq("id", suggestion_id).execute()
    except Exception:
        pass

    if new_strike <= 3:
        # Show warning to operator
        print("")
        print("  " + "=" * 60)
        print("  " + STRIKE_WARNINGS[new_strike])
        print("  " + "=" * 60)
        print("")

        # Notify admin via Telegram
        tg_msg = STRIKE_TELEGRAM_MESSAGES[new_strike].format(
            bug_class=bug_class,
            affected_file=affected_file,
        )
        _send_telegram(tg_msg)
        print("  Admin notified via Telegram (Strike " + str(new_strike) + "/3)")
        return False  # Action NOT allowed yet

    else:
        # Strike 4 -- action allowed
        print("")
        print("  " + "=" * 60)
        print("  ACTION ALLOWED: 4th confirmation received.")
        print("  Admin is being notified that action is proceeding.")
        print("  " + "=" * 60)
        print("")

        tg_msg = STRIKE4_TELEGRAM.format(
            bug_class=bug_class,
            affected_file=affected_file,
        )
        _send_telegram(tg_msg)

        # Update status to allowed
        try:
            client.table("code_fix_suggestions").update(
                {"status": "admin_allowed",
                 "reviewed_at": datetime.now(timezone.utc).isoformat()}
            ).eq("id", suggestion_id).execute()
        except Exception:
            pass

        return True  # Action allowed


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

        admin_req = _is_admin_required(bug["class"])

        # Check for existing suggestion
        try:
            existing = client.table("code_fix_suggestions").select("id, strike_count, status") \
                .eq("bug_class", bug["class"]) \
                .in_("status", ["pending", "admin_required"]) \
                .execute()
        except Exception:
            existing = type("obj", (object,), {"data": []})()  # empty result

        if existing.data:
            row = existing.data[0]
            current_strike = row.get("strike_count", 0)

            if admin_req:
                # Run strike system
                allowed = _handle_strike(
                    client, row["id"], bug["class"],
                    bug["affected_file"], current_strike
                )
                if allowed:
                    print("  Action allowed after 4 confirmations: " + bug["class"])
                else:
                    print("  Admin-required action protected (strike " +
                          str(current_strike + 1) + "/3): " + bug["class"])
            else:
                print("  Skipping " + bug["class"] + " - already pending")
            continue

        # New suggestion
        print("  Generating suggestion for: " + bug["class"])
        fix_text = _call_groq_for_fix(bug["class"], error_message, bug["affected_file"])
        if not fix_text:
            fix_text = bug["description"] + " - manual review required"

        record = {
            "bug_class": bug["class"],
            "error_message": error_message[:500],
            "suggested_fix": fix_text,
            "affected_file": bug["affected_file"],
            "status": "admin_required" if admin_req else "pending",
            "admin_required": admin_req,
            "strike_count": 0,
        }

        try:
            result = client.table("code_fix_suggestions").insert(record).execute()
            suggestions.append(record)

            if admin_req and result.data:
                # First time seen -- run strike system immediately (Strike 1)
                _handle_strike(
                    client, result.data[0]["id"],
                    bug["class"], bug["affected_file"], 0
                )
            else:
                print("  Saved: " + bug["class"])
        except Exception as e:
            print("  Warning: Could not save suggestion: " + str(e))

    if suggestions:
        print(str(len(suggestions)) + " suggestion(s) processed")
    return suggestions


def get_pending_suggestions():
    client = _get_client()
    if not client:
        return []
    try:
        result = client.table("code_fix_suggestions").select("*") \
            .in_("status", ["pending", "admin_required"]) \
            .order("created_at", desc=True).execute()
        return result.data or []
    except Exception:
        return []


if __name__ == "__main__":
    print("\nGNI Code Fix Suggester - Manual Run\n")
    run_code_fix_suggester()
    pending = get_pending_suggestions()
    print("\nPending: " + str(len(pending)))
    for s in pending:
        admin_flag = " [ADMIN REQUIRED - Strike " + str(s.get("strike_count", 0)) + "/3]" if s.get("admin_required") else ""
        print("  [" + s["bug_class"] + "]" + admin_flag + " " + s["suggested_fix"][:80])
