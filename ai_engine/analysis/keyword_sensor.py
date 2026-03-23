# ============================================================
# GNI Keyword Sensor v2
# Detects emerging keywords in news feeds.
# Sends Telegram inline buttons for admin review.
# 4 statuses: candidate / watching / approved / rejected
# Re-emergence: rejected keywords re-elevated if trending rises 2x
# Security: full sanitisation against injection attacks
# L58: ASCII sanitisation before Groq prompts
# L60: Deterministic keyword matching only
# ============================================================

import os
import re
import json
import requests
from collections import Counter
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_ADMIN_CHAT_ID = os.getenv("TELEGRAM_ADMIN_CHAT_ID", "") or os.getenv("TELEGRAM_CHAT_ID", "")
APP_URL = os.getenv("NEXT_PUBLIC_APP_URL", "https://gni-autonomous.vercel.app")

MIN_ARTICLE_FREQUENCY = 3
MIN_SOURCE_COUNT = 2
MIN_WORD_LENGTH = 4
MAX_KEYWORD_LENGTH = 50
REEMERGENCE_MULTIPLIER = 2.0

STOP_WORDS = {
    "this", "that", "with", "from", "they", "have", "been", "were",
    "their", "there", "what", "when", "will", "would", "could", "should",
    "which", "after", "before", "about", "more", "also", "into", "over",
    "than", "then", "them", "these", "those", "some", "such", "only",
    "said", "says", "saying", "according", "report", "reports", "reported",
    "year", "years", "week", "weeks", "month", "months", "time", "times",
    "people", "country", "countries", "government", "governments",
    "world", "global", "international", "national", "local",
    "news", "latest", "update", "updates", "analysis", "opinion",
}

# Security: characters not allowed in keywords
INJECTION_CHARS = set("/\\<>{}=;\'\"!@#$%^&*()+[]|`~")


def _sanitise_keyword(raw: str) -> str:
    """
    Security: sanitise keyword text before saving or displaying.
    Allow only alphanumeric, spaces, and hyphens.
    Remove all injection-risk characters.
    Truncate to MAX_KEYWORD_LENGTH.
    L58: deterministic sanitisation, no LLM involvement.
    """
    # Remove injection characters
    clean = ""
    for ch in raw.lower():
        if ch.isalnum() or ch in (" ", "-"):
            clean += ch
    # Collapse multiple spaces
    clean = " ".join(clean.split())
    # Truncate
    clean = clean[:MAX_KEYWORD_LENGTH]
    return clean.strip()


def _is_safe_keyword(keyword: str) -> bool:
    """
    Security: validate keyword is safe before processing.
    Reject if contains injection patterns.
    L60: deterministic check only.
    """
    if not keyword or len(keyword) < MIN_WORD_LENGTH:
        return False
    if len(keyword) > MAX_KEYWORD_LENGTH:
        return False
    # Check for injection characters
    for ch in keyword:
        if ch in INJECTION_CHARS:
            return False
    # Check for injection patterns
    injection_patterns = [
        "ignore", "override", "jailbreak", "system:", "act as",
        "approve all", "reject all", "/approve", "/reject",
        "drop table", "select *", "insert into",
    ]
    lower = keyword.lower()
    for pattern in injection_patterns:
        if pattern in lower:
            return False
    return True


def _get_client():
    try:
        from supabase import create_client
        url = os.getenv("SUPABASE_URL", "")
        key = os.getenv("SUPABASE_SERVICE_KEY", "")
        if not url or not key:
            return None
        return create_client(url, key)
    except Exception:
        return None


def _get_existing_keywords() -> set:
    """Get all current keywords from funnel to avoid re-flagging known terms."""
    try:
        from funnel.intelligence_funnel import GEOPOLITICAL_KEYWORDS
        return set(kw.lower() for kw in GEOPOLITICAL_KEYWORDS)
    except Exception:
        return set()


def _extract_phrases(text: str) -> list:
    """Extract 1-3 word phrases, filtering stop words and unsafe characters."""
    # Security: strip HTML and injection chars first
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", " ", text)
    words = [w for w in text.split()
             if len(w) >= MIN_WORD_LENGTH
             and w not in STOP_WORDS
             and _is_safe_keyword(w)]

    phrases = list(words)
    for i in range(len(words) - 1):
        phrase = words[i] + " " + words[i+1]
        if len(phrase) >= 8 and _is_safe_keyword(phrase):
            phrases.append(phrase)
    for i in range(len(words) - 2):
        phrase = words[i] + " " + words[i+1] + " " + words[i+2]
        if len(phrase) >= 12 and _is_safe_keyword(phrase):
            phrases.append(phrase)
    return phrases


def _call_groq_for_definition(keyword: str, contexts: list) -> str:
    """Ask Groq to define keyword. L58: sanitise inputs before prompt."""
    if not GROQ_API_KEY or not contexts:
        return ""
    # L58: sanitise keyword and context before Groq prompt
    safe_keyword = keyword.encode("ascii", "ignore").decode("ascii")
    safe_contexts = []
    for ctx in contexts[:3]:
        safe_ctx = ctx.encode("ascii", "ignore").decode("ascii")[:200]
        safe_contexts.append(safe_ctx)
    context_text = "\n".join(safe_contexts)
    prompt = (
        "A new term is emerging in global news: '" + safe_keyword + "'\n\n"
        "Context examples:\n" + context_text + "\n\n"
        "In 2 sentences: (1) What does this term mean in real-world current usage? "
        "(2) Which pillar: Technology, Financial, or Geopolitical? "
        "Be specific and practical."
    )
    try:
        response = requests.post(
            GROQ_URL,
            headers={"Authorization": "Bearer " + GROQ_API_KEY,
                     "Content-Type": "application/json"},
            json={"model": GROQ_MODEL,
                  "messages": [{"role": "user", "content": prompt}],
                  "temperature": 0.3, "max_tokens": 150},
            timeout=15,
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("  Warning: Groq definition failed: " + str(e)[:50])
    return ""


def _suggest_pillar(definition: str) -> str:
    d = definition.lower()
    if any(w in d for w in ["technology", "cyber", "digital", "tech", "software", "ai", "data"]):
        return "tech"
    if any(w in d for w in ["financial", "economic", "market", "finance", "trade", "currency"]):
        return "fin"
    return "geo"


def _send_telegram_keyword_alert(keyword_id: str, keyword: str, frequency: int,
                                  source_count: int, definition: str, pillar: str,
                                  status: str = "candidate", watching_days: int = 0,
                                  reemergence: bool = False) -> str:
    """
    Send Telegram message with inline approve/watch/reject buttons.
    Security: keyword_id is UUID, never raw keyword text in callback data.
    Returns telegram_message_id for future updates.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_ADMIN_CHAT_ID:
        return ""

    pillar_emoji = {"geo": "🌍", "fin": "💰", "tech": "💻"}.get(pillar, "🌐")

    if reemergence:
        header = "🔄 Re-emerged keyword: \"" + keyword + "\""
        subtext = "Was rejected. Now trending again with higher frequency."
    elif status == "watching":
        header = "⏳ Still watching: \"" + keyword + "\""
        subtext = "Trending for " + str(watching_days) + " days and continuing."
    else:
        header = "🆕 New keyword detected: \"" + keyword + "\""
        subtext = "First detected in intelligence feeds."

    text = (
        header + "\n"
        + subtext + "\n\n"
        + pillar_emoji + " Pillar: " + pillar.upper()
        + " | Frequency: " + str(frequency)
        + " | Sources: " + str(source_count) + "\n\n"
        + "📖 Definition: " + (definition[:200] if definition else "Pending...") + "\n\n"
        + "Review at: " + APP_URL + "/keywords"
    )

    # Security: use keyword_id (UUID) in callback data, never raw keyword text
    keyboard = {
        "inline_keyboard": [[
            {"text": "✅ Approve", "callback_data": "kw_approve_" + keyword_id},
            {"text": "⏳ Watch",   "callback_data": "kw_watch_"   + keyword_id},
            {"text": "❌ Reject",  "callback_data": "kw_reject_"  + keyword_id},
        ]]
    }

    try:
        response = requests.post(
            "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage",
            json={
                "chat_id": TELEGRAM_ADMIN_CHAT_ID,
                "text": text,
                "reply_markup": keyboard,
            },
            timeout=10,
        )
        if response.status_code == 200:
            data = response.json()
            return str(data.get("result", {}).get("message_id", ""))
    except Exception as e:
        print("  Warning: Telegram keyword alert failed: " + str(e)[:60])
    return ""


def _check_reemergence(client, keyword: str, current_frequency: int) -> dict | None:
    """
    Check if a previously rejected keyword has re-emerged with higher frequency.
    Returns the existing row if re-emergence detected, else None.
    """
    try:
        result = client.table("emerging_keywords") \
            .select("id, status, rejected_frequency, reemergence_count, frequency_count") \
            .eq("keyword", keyword) \
            .eq("status", "rejected") \
            .execute()
        if result.data:
            row = result.data[0]
            rejected_freq = row.get("rejected_frequency") or row.get("frequency_count", 0)
            if rejected_freq > 0 and current_frequency >= rejected_freq * REEMERGENCE_MULTIPLIER:
                return row
    except Exception:
        pass
    return None


def _update_watching_keywords(client) -> None:
    """Update watching_days counter for all watching keywords."""
    try:
        result = client.table("emerging_keywords") \
            .select("id, watching_since, watching_days") \
            .eq("status", "watching") \
            .execute()
        for row in (result.data or []):
            since = row.get("watching_since")
            if since:
                try:
                    since_dt = datetime.fromisoformat(since.replace("Z", "+00:00"))
                    days = (datetime.now(timezone.utc) - since_dt).days
                    client.table("emerging_keywords") \
                        .update({"watching_days": days}) \
                        .eq("id", row["id"]) \
                        .execute()
                except Exception:
                    pass
    except Exception:
        pass


def run_keyword_sensor(articles: list) -> list:
    """
    Main entry point. Scan articles for emerging keywords.
    Sends Telegram alerts with inline approve/watch/reject buttons.
    Returns list of newly detected keyword candidates.
    """
    if not articles:
        return []

    existing_keywords = _get_existing_keywords()
    client = _get_client()

    # Update watching days for all watching keywords
    if client:
        _update_watching_keywords(client)

    phrase_counts = Counter()
    phrase_sources = {}
    phrase_contexts = {}

    for art in articles:
        text = art.get("title", "") + " " + art.get("summary", "")
        source = art.get("source", "Unknown")
        phrases = _extract_phrases(text)

        for phrase in phrases:
            if phrase in existing_keywords:
                continue
            phrase_counts[phrase] += 1
            if phrase not in phrase_sources:
                phrase_sources[phrase] = set()
            phrase_sources[phrase].add(source)
            if phrase not in phrase_contexts:
                phrase_contexts[phrase] = []
            if len(phrase_contexts[phrase]) < 3:
                phrase_contexts[phrase].append(text[:200])

    candidates = []
    for phrase, count in phrase_counts.most_common(50):
        if count < MIN_ARTICLE_FREQUENCY:
            break
        sources = phrase_sources.get(phrase, set())
        if len(sources) < MIN_SOURCE_COUNT:
            continue
        if count > 50:
            continue
        candidates.append({
            "keyword": phrase,
            "frequency": count,
            "sources": list(sources),
            "contexts": phrase_contexts.get(phrase, []),
        })

    if not candidates:
        print("  No new emerging keywords detected")
        return []

    print("  Detected " + str(len(candidates)) + " candidate keyword(s) -- checking against DB")

    saved = []
    for cand in candidates[:10]:
        keyword = _sanitise_keyword(cand["keyword"])
        if not keyword or not _is_safe_keyword(keyword):
            print("  Security: keyword rejected -- failed sanitisation: " + cand["keyword"][:30])
            continue

        if not client:
            continue

        try:
            # Check re-emergence first
            reemergence_row = _check_reemergence(client, keyword, cand["frequency"])
            if reemergence_row:
                # Re-elevate to watching
                client.table("emerging_keywords").update({
                    "status": "watching",
                    "frequency_count": reemergence_row["frequency_count"] + cand["frequency"],
                    "source_count": len(cand["sources"]),
                    "last_seen": datetime.now(timezone.utc).isoformat(),
                    "reemergence_count": (reemergence_row.get("reemergence_count") or 0) + 1,
                    "watching_since": datetime.now(timezone.utc).isoformat(),
                }).eq("id", reemergence_row["id"]).execute()

                # Get definition for re-emergence alert
                definition = _call_groq_for_definition(keyword, cand["contexts"])
                pillar = _suggest_pillar(definition)

                msg_id = _send_telegram_keyword_alert(
                    keyword_id=reemergence_row["id"],
                    keyword=keyword,
                    frequency=cand["frequency"],
                    source_count=len(cand["sources"]),
                    definition=definition,
                    pillar=pillar,
                    reemergence=True,
                )
                print("  Re-emerged keyword: '" + keyword + "' -- alert sent")
                saved.append(keyword)
                continue

            # Check if already tracked (candidate or watching)
            existing = client.table("emerging_keywords") \
                .select("id, frequency_count, last_seen, status, watching_days, watching_since") \
                .eq("keyword", keyword) \
                .execute()

            if existing.data:
                row = existing.data[0]
                watching_days = row.get("watching_days", 0)

                # Update frequency
                client.table("emerging_keywords").update({
                    "frequency_count": row["frequency_count"] + cand["frequency"],
                    "last_seen": datetime.now(timezone.utc).isoformat(),
                    "source_count": len(cand["sources"]),
                }).eq("id", row["id"]).execute()

                # Send watching alert if still in watching status
                if row["status"] == "watching" and watching_days > 0 and watching_days % 3 == 0:
                    definition = _call_groq_for_definition(keyword, cand["contexts"])
                    pillar = _suggest_pillar(definition)
                    _send_telegram_keyword_alert(
                        keyword_id=row["id"],
                        keyword=keyword,
                        frequency=cand["frequency"],
                        source_count=len(cand["sources"]),
                        definition=definition,
                        pillar=pillar,
                        status="watching",
                        watching_days=watching_days,
                    )
                    print("  Watching update: '" + keyword + "' day " + str(watching_days))
                continue

            # New keyword -- get Groq definition
            definition = _call_groq_for_definition(keyword, cand["contexts"])
            pillar = _suggest_pillar(definition)

            # Save to emerging_keywords
            result = client.table("emerging_keywords").insert({
                "keyword": keyword,
                "frequency_count": cand["frequency"],
                "source_count": len(cand["sources"]),
                "example_context": (cand["contexts"][0] if cand["contexts"] else "")[:500],
                "groq_definition": definition,
                "pillar_suggestion": pillar,
                "status": "candidate",
                "reviewed": False,
                "watching_days": 0,
            }).execute()

            if result.data:
                keyword_id = result.data[0]["id"]

                # Send Telegram alert with inline buttons
                msg_id = _send_telegram_keyword_alert(
                    keyword_id=keyword_id,
                    keyword=keyword,
                    frequency=cand["frequency"],
                    source_count=len(cand["sources"]),
                    definition=definition,
                    pillar=pillar,
                )

                # Save telegram message id for future updates
                if msg_id:
                    client.table("emerging_keywords").update({
                        "telegram_message_id": msg_id,
                    }).eq("id", keyword_id).execute()

                saved.append(keyword)
                print("  New keyword: '" + keyword + "' [" + pillar.upper() + "] freq=" + str(cand["frequency"]))

        except Exception as e:
            print("  Warning: keyword processing failed: " + str(e)[:60])

    if saved:
        print("  " + str(len(saved)) + " keyword(s) saved -- Telegram alerts sent")
    return saved
