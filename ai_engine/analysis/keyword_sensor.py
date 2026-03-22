# ============================================================
# GNI Keyword Sensor
# Continuously detects emerging keywords and idioms in news feeds.
# Surfaces new terms for admin review -- never auto-adds to lists.
# ============================================================

import os
import re
import requests
from collections import Counter
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# Minimum thresholds for a term to be flagged
MIN_ARTICLE_FREQUENCY = 3   # appears in at least 3 articles per run
MIN_SOURCE_COUNT = 2        # appears across at least 2 different sources
MIN_WORD_LENGTH = 4         # minimum characters per word in phrase

# Stop words -- skip these entirely
STOP_WORDS = {
    'this', 'that', 'with', 'from', 'they', 'have', 'been', 'were',
    'their', 'there', 'what', 'when', 'will', 'would', 'could', 'should',
    'which', 'after', 'before', 'about', 'more', 'also', 'into', 'over',
    'than', 'then', 'them', 'these', 'those', 'some', 'such', 'only',
    'said', 'says', 'saying', 'according', 'report', 'reports', 'reported',
    'year', 'years', 'week', 'weeks', 'month', 'months', 'time', 'times',
    'people', 'country', 'countries', 'government', 'governments',
    'world', 'global', 'international', 'national', 'local',
    'news', 'latest', 'update', 'updates', 'analysis', 'opinion',
}

# All existing keywords -- new terms must not already be in these lists
# (imported dynamically to stay current with any additions)


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


def _get_existing_keywords() -> set:
    """Get all current keywords from the funnel to avoid re-flagging known terms."""
    try:
        from funnel.intelligence_funnel import (
            GEOPOLITICAL_KEYWORDS,
        )
        existing = set()
        for kw in GEOPOLITICAL_KEYWORDS:
            existing.add(kw.lower())
        return existing
    except Exception:
        return set()


def _extract_phrases(text: str) -> list:
    """Extract 1-3 word phrases from text, filtering stop words."""
    # Clean text
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', ' ', text)
    words = [w for w in text.split() if len(w) >= MIN_WORD_LENGTH and w not in STOP_WORDS]

    phrases = []

    # Unigrams
    phrases.extend(words)

    # Bigrams
    for i in range(len(words) - 1):
        phrase = words[i] + ' ' + words[i+1]
        if len(phrase) >= 8:  # minimum bigram length
            phrases.append(phrase)

    # Trigrams
    for i in range(len(words) - 2):
        phrase = words[i] + ' ' + words[i+1] + ' ' + words[i+2]
        if len(phrase) >= 12:  # minimum trigram length
            phrases.append(phrase)

    return phrases


def _call_groq_for_definition(keyword: str, contexts: list) -> str:
    """Ask Groq to define the keyword based on how it appears in context."""
    if not GROQ_API_KEY or not contexts:
        return ""

    context_text = "\n".join(contexts[:3])  # max 3 examples
    prompt = (
        "A new term is emerging in global news feeds: '" + keyword + "'\n\n"
        "It appears in these news contexts:\n" + context_text + "\n\n"
        "In 2 sentences: (1) What does this term mean in real-world current usage? "
        "(2) Which geopolitical pillar does it belong to: Technology, Financial, or Geopolitical? "
        "Be specific and practical. No academic language."
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
    """Infer pillar from Groq definition."""
    d = definition.lower()
    if any(w in d for w in ['technology', 'cyber', 'digital', 'tech', 'software', 'ai', 'data']):
        return 'tech'
    if any(w in d for w in ['financial', 'economic', 'market', 'finance', 'trade', 'currency']):
        return 'fin'
    return 'geo'


def run_keyword_sensor(articles: list) -> list:
    """
    Main entry point. Scan articles for emerging keywords.
    Returns list of newly detected keyword candidates.
    """
    if not articles:
        return []

    existing_keywords = _get_existing_keywords()
    client = _get_client()

    # Count phrase frequency and track sources + contexts
    phrase_counts = Counter()
    phrase_sources = {}  # phrase -> set of sources
    phrase_contexts = {}  # phrase -> list of example sentences

    for art in articles:
        text = art.get('title', '') + ' ' + art.get('summary', '')
        source = art.get('source', 'Unknown')
        phrases = _extract_phrases(text)

        for phrase in phrases:
            if phrase in existing_keywords:
                continue
            phrase_counts[phrase] += 1
            if phrase not in phrase_sources:
                phrase_sources[phrase] = set()
            phrase_sources[phrase].add(source)
            if phrase not in phrase_contexts and phrase in text.lower():
                phrase_contexts[phrase] = []
            if phrase in phrase_contexts and len(phrase_contexts[phrase]) < 3:
                phrase_contexts[phrase].append(text[:200])

    # Filter by thresholds
    candidates = []
    for phrase, count in phrase_counts.most_common(50):
        if count < MIN_ARTICLE_FREQUENCY:
            break  # sorted by count, so stop here
        sources = phrase_sources.get(phrase, set())
        if len(sources) < MIN_SOURCE_COUNT:
            continue
        # Skip if too common (likely already known)
        if count > 50:
            continue
        candidates.append({
            'keyword': phrase,
            'frequency': count,
            'sources': list(sources),
            'contexts': phrase_contexts.get(phrase, []),
        })

    if not candidates:
        print("  No new emerging keywords detected")
        return []

    print("  Detected " + str(len(candidates)) + " candidate keyword(s) -- checking against DB")

    saved = []
    for cand in candidates[:10]:  # max 10 per run to limit Groq calls
        keyword = cand['keyword']

        # Check if already in emerging_keywords table
        if client:
            try:
                existing = client.table("emerging_keywords") \
                    .select("id, frequency_count, last_seen") \
                    .eq("keyword", keyword) \
                    .execute()

                if existing.data:
                    # Update frequency and last_seen
                    row = existing.data[0]
                    client.table("emerging_keywords").update({
                        "frequency_count": row["frequency_count"] + cand["frequency"],
                        "last_seen": datetime.now(timezone.utc).isoformat(),
                        "source_count": len(cand["sources"]),
                    }).eq("id", row["id"]).execute()
                    continue  # already tracked
            except Exception:
                pass

        # New keyword -- get Groq definition
        definition = _call_groq_for_definition(keyword, cand['contexts'])
        pillar = _suggest_pillar(definition)

        # Save to emerging_keywords
        if client:
            try:
                client.table("emerging_keywords").insert({
                    "keyword": keyword,
                    "frequency_count": cand["frequency"],
                    "source_count": len(cand["sources"]),
                    "example_context": (cand["contexts"][0] if cand["contexts"] else "")[:500],
                    "groq_definition": definition,
                    "pillar_suggestion": pillar,
                    "status": "candidate",
                    "reviewed": False,
                }).execute()
                saved.append(keyword)
                print("  New keyword candidate: '" + keyword + "' [" + pillar.upper() + "] freq=" + str(cand["frequency"]))
            except Exception as e:
                print("  Warning: Could not save keyword: " + str(e)[:60])

    if saved:
        print("  " + str(len(saved)) + " new keyword(s) saved to emerging_keywords table")
    return saved


if __name__ == "__main__":
    print("\nGNI Keyword Sensor -- Manual Test\n")
    # Test with dummy articles
    test_articles = [
        {"title": "Polycrisis deepens as deglobalisation accelerates",
         "summary": "The polycrisis of simultaneous global failures is worsening.",
         "source": "BBC"},
        {"title": "Permacrisis in European energy markets",
         "summary": "Europe faces a permacrisis with no clear resolution path.",
         "source": "FT"},
        {"title": "Greenflation hits developing economies hardest",
         "summary": "Greenflation caused by energy transition is raising costs.",
         "source": "Economist"},
    ]
    results = run_keyword_sensor(test_articles)
    print("\nDetected: " + str(results))
