import os
import json
import re
import requests
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# GNI Nexus Analyzer — Day 4 (updated)
# Primary:  Groq API (GitHub Actions / cloud)
# Local:    Llama 3 8B via Ollama (local development)
# Auto-detects environment and uses appropriate LLM
# Myanmar summary generated as separate post-processing step
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3:8b"
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")  # L23: never hardcode model names
GROQ_MODEL_FALLBACK = os.getenv("GROQ_MODEL_FALLBACK", "llama-3.1-8b-instant")  # automatic failover
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS", "false").lower() == "true"


def _build_prompt(articles: list[dict], prompt_override: str = None) -> str:
    """Build analysis prompt from top articles."""
    articles_text = ""
    for i, a in enumerate(articles, 1):
        articles_text += f"""
Article {i}:
Source: {a['source']} ({a['bias']})
Title: {a['title'][:100]}
Summary: {a['summary'][:500]}
Tokens: {min(len(a['title'][:100]) + len(a['summary'][:500]), 600)} chars
---"""

    if prompt_override:
        n = len(articles)
        return prompt_override.format(n=n, articles=articles_text)
    return f"""You are GNI — Global Nexus Insights, an expert geopolitical and macroeconomic analyst.

Analyze the following {len(articles)} news articles and produce a structured JSON report.

ARTICLES:
{articles_text}

Respond ONLY with a valid JSON object in this exact format:
{{
  "title": "Brief title summarizing the main geopolitical theme (max 15 words)",
  "summary": "2-3 sentence English summary of the key event and its significance",
  "sentiment": "Bullish or Bearish or Neutral",
  "sentiment_score": 0.0,
  "source_consensus_score": 0.0,
  "location_name": "Single country name only — pick the MOST affected country (e.g. Iran, Ukraine, China). Never use regions like 'Middle East' or multiple countries.",
  "tickers_affected": ["SPY", "GLD"],
  "market_impact": "3-4 sentences explaining WHY this affects markets. Use causal language: because, therefore, as a result, driven by, consequently, leading to, due to. Explain the chain of causation from event to market outcome in detail.",
  "risk_level": "Low or Medium or High or Critical"
}}

Rules:
- sentiment_score: -1.0 (very bearish) to +1.0 (very bullish) for markets
- source_consensus_score: 0.0 to 1.0 (how much sources agree)
- tickers_affected: choose from [SPY, AAPL, JPM, XOM, GLD, USO, LMT, TLT, EWT, EWJ, FXI, DXY]
- Do NOT include myanmar_summary field
- Respond with JSON only — no extra text, no markdown, no explanation
"""


def _call_ollama(prompt: str) -> str | None:
    """Call local Ollama Llama 3."""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.3, "num_predict": 1200}
            },
            timeout=180
        )
        if response.status_code == 200:
            return response.json().get("response", "")
    except Exception as e:
        print(f"  ⚠️  Ollama error: {e}")
    return None


def _call_groq(prompt: str, model: str = None) -> str | None:
    """Call Groq API. Retries once with fallback model on failure (L33)."""
    if not GROQ_API_KEY:
        print("  ⚠️  No Groq API key found in .env")
        return None

    models_to_try = [model or GROQ_MODEL, GROQ_MODEL_FALLBACK]

    for attempt, model_name in enumerate(models_to_try, 1):
        try:
            response = requests.post(
                GROQ_URL,
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 2000
                },
                timeout=30
            )
            if response.status_code == 200:
                if attempt == 2:
                    print(f"  ⚠️  Primary model failed — used fallback: {model_name}")
                return response.json()["choices"][0]["message"]["content"]
            else:
                print(f"  ⚠️  Groq error (attempt {attempt}, model={model_name}): {response.status_code} {response.text[:100]}")
        except Exception as e:
            print(f"  ⚠️  Groq error (attempt {attempt}, model={model_name}): {e}")

        if attempt == 1:
            print(f"  🔄 Retrying with fallback model: {GROQ_MODEL_FALLBACK}")

    return None


def _parse_json_response(raw: str) -> dict | None:
    """
    Safely parse JSON from LLM response.

    Handles in order:
      1. Direct parse (clean response — the happy path)
      2. Markdown code fence stripping  (```json ... ```)
      3. Preamble/postamble trimming    (text before { or after })
      4. Truncation repair              (response cut off mid-string by token limit)
      5. Field-by-field regex extraction (last resort — returns partial report)

    FIX vs old version:
      OLD: counted total '"' characters to detect open string — WRONG.
           '"title": "foo"' has 4 quotes — even — falsely detected as closed.
      NEW: scans character by character to track actual string state.
    """
    if not raw:
        return None

    text = raw.strip()

    # ── Strategy 1: Direct parse ──────────────────────────────────────────
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # ── Strategy 2: Strip markdown code fences ────────────────────────────
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:])
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # ── Strategy 3: Extract the JSON object (trim preamble/postamble) ─────
    start = text.find("{")
    end = text.rfind("}") + 1
    if start >= 0 and end > start:
        try:
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass

    # ── Strategy 4: Repair truncated JSON ────────────────────────────────
    # The old version counted total '"' characters which is WRONG —
    # string values contain their own quote pairs that must not be counted.
    # We track actual parser state instead.
    if start >= 0:
        partial = text[start:]
        repaired = _repair_truncated_json(partial)
        if repaired:
            try:
                result = json.loads(repaired)
                # Fill in any missing required fields with safe defaults
                defaults = {
                    "title": "GNI Report",
                    "summary": "",
                    "sentiment": "Neutral",
                    "sentiment_score": 0.0,
                    "source_consensus_score": 0.5,
                    "location_name": "Global",
                    "tickers_affected": ["SPY"],
                    "market_impact": "",
                    "risk_level": "Medium",
                }
                for k, v in defaults.items():
                    if k not in result:
                        result[k] = v
                print("  ⚠️  JSON was truncated — repaired successfully")
                return result
            except json.JSONDecodeError:
                pass

    # ── Strategy 5: Field-by-field regex extraction ───────────────────────
    result = _extract_fields_regex(text)
    if result:
        print("  ⚠️  JSON could not be parsed — used regex field extraction")
        return result

    return None


def _repair_truncated_json(s: str) -> str | None:
    """
    Repair a JSON string that was cut off mid-way through a string value.

    Works by scanning character-by-character to track:
      - Whether we are currently inside a string value
      - Nesting depth of {} and []

    This is correct. The old approach of counting total '"' characters
    is broken because string values contain their own quote pairs.
    """
    s = s.rstrip()
    if not s:
        return None

    in_string = False
    escape_next = False
    brace_depth = 0
    bracket_depth = 0

    for ch in s:
        if escape_next:
            escape_next = False
            continue
        if ch == "\\" and in_string:
            escape_next = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            brace_depth += 1
        elif ch == "}":
            brace_depth -= 1
        elif ch == "[":
            bracket_depth += 1
        elif ch == "]":
            bracket_depth -= 1

    # If we ended inside a string, close it
    if in_string:
        s += '"'

    # Close any open arrays and objects
    s += "]" * max(0, bracket_depth)
    s += "}" * max(0, brace_depth)

    # Remove any trailing comma before a closing brace/bracket
    s = re.sub(r",\s*([}\]])", r"\1", s)

    return s


def _extract_fields_regex(raw: str) -> dict | None:
    """
    Last resort: extract known fields from malformed JSON using regex.
    Returns a minimal valid report if at least 'title' can be found.
    """
    def get_str(field: str) -> str:
        # Match "field": "value..." — stops at first unescaped closing quote
        m = re.search(rf'"{field}"\s*:\s*"((?:[^"\\]|\\.)*)"?', raw, re.DOTALL)
        return m.group(1).strip() if m else ""

    def get_num(field: str) -> float:
        m = re.search(rf'"{field}"\s*:\s*(-?[\d.]+)', raw)
        return float(m.group(1)) if m else 0.0

    title = get_str("title")
    if not title:
        return None

    return {
        "title":                 title,
        "summary":               get_str("summary") or "Analysis pending.",
        "sentiment":             get_str("sentiment") or "Neutral",
        "sentiment_score":       get_num("sentiment_score"),
        "source_consensus_score": get_num("source_consensus_score") or 0.5,
        "location_name":         get_str("location_name") or "Global",
        "tickers_affected":      ["SPY"],
        "market_impact":         get_str("market_impact") or "",
        "risk_level":            get_str("risk_level") or "Medium",
    }


def _generate_myanmar_summary(report: dict) -> str:
    """Generate a Burmese language summary as a separate post-processing step."""
    if not GROQ_API_KEY:
        return ""

    summary = report.get("summary", "")

    prompt = f"""Translate this EXACT text into Myanmar (Burmese) language. 
Translate word-for-word accurately. Do not summarize or change the meaning.
Respond with ONLY the Burmese translation, nothing else.

Text to translate:
{summary}"""

    try:
        response = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": GROQ_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 300
            },
            timeout=15
        )
        if response.status_code == 200:
            result = response.json()["choices"][0]["message"]["content"].strip()
            print(f"  ✅ Myanmar summary generated ({len(result)} chars)")
            return result
        else:
            print(f"  ⚠️  Myanmar summary failed: {response.status_code}")
            return ""
    except Exception as e:
        print(f"  ⚠️  Myanmar summary error: {e}")
        return ""




# Required fields: name -> (expected_type, validator_fn or None)
_REQUIRED_FIELDS = {
    "title":                 (str,   lambda v: len(v.strip()) > 0),
    "summary":               (str,   lambda v: len(v.strip()) > 0),
    "sentiment":             (str,   lambda v: v.strip() in ["Bullish", "Bearish", "Neutral"]),
    "sentiment_score":       (float, lambda v: -1.0 <= float(v) <= 1.0),
    "source_consensus_score":(float, lambda v: 0.0 <= float(v) <= 1.0),
    "location_name":         (str,   lambda v: len(v.strip()) > 0),
    "tickers_affected":      (list,  lambda v: len(v) > 0),
    "market_impact":         (str,   lambda v: len(v.strip()) > 0),
    "risk_level":            (str,   lambda v: v.strip() in ["Low", "Medium", "High", "Critical"]),
}


def _validate_report_schema(report: dict) -> dict | None:
    """
    Validate all required fields exist, have correct type, and pass range checks.
    Coerces numeric strings to float where possible.
    Returns corrected report, or None if critical fields cannot be fixed.
    """
    if not report:
        return None

    errors = []
    warnings = []

    for field, (expected_type, validator) in _REQUIRED_FIELDS.items():
        value = report.get(field)

        # Missing field
        if value is None:
            errors.append(f"Missing required field: {field}")
            continue

        # Coerce numeric strings to float
        if expected_type == float and isinstance(value, str):
            try:
                report[field] = float(value)
                value = report[field]
                warnings.append(f"Coerced {field} from str to float")
            except ValueError:
                errors.append(f"Cannot coerce {field} to float: {value!r}")
                continue

        # Type check
        if not isinstance(value, expected_type):
            errors.append(f"Wrong type for {field}: expected {expected_type.__name__}, got {type(value).__name__}")
            continue

        # Range/value check
        if validator:
            try:
                if not validator(value):
                    warnings.append(f"Invalid value for {field}: {value!r} — applying default")
                    # Apply safe defaults for fixable fields
                    if field == "sentiment":
                        report[field] = "Neutral"
                    elif field == "risk_level":
                        report[field] = "Medium"
                    elif field == "sentiment_score":
                        report[field] = max(-1.0, min(1.0, float(value)))
                    elif field == "source_consensus_score":
                        report[field] = max(0.0, min(1.0, float(value)))
            except Exception:
                warnings.append(f"Validator error for {field}: {value!r}")

    if warnings:
        for w in warnings:
            print(f"  ⚠️  Schema: {w}")

    if errors:
        print(f"  ❌ Schema validation failed: {errors}")
        return None

    return report

def analyze(articles: list[dict], prompt_override: str = None) -> dict | None:
    """
    Analyze top articles using appropriate LLM.
    GitHub Actions → Groq API directly (no Ollama timeout waste)
    Local development → Ollama first, Groq fallback
    """
    if not articles:
        print("  ⚠️  No articles to analyze")
        return None

    prompt = _build_prompt(articles, prompt_override=prompt_override)
    raw = None
    source_used = None

    if GITHUB_ACTIONS:
        # Cloud mode — Groq directly, no Ollama attempt
        print("  ☁️  GitHub Actions — using Groq API directly...")
        raw = _call_groq(prompt)
        source_used = "groq"
    else:
        # Local mode — Ollama first, Groq fallback
        print("  🧠 Calling Ollama (Llama 3 8B local)...")
        raw = _call_ollama(prompt)
        source_used = "ollama"

        if not raw:
            print("  🔄 Ollama unavailable — falling back to Groq API...")
            raw = _call_groq(prompt)
            source_used = "groq"

    if not raw:
        print("  ❌ Both Ollama and Groq failed")
        return None

    report = _parse_json_response(raw)
    if not report:
        print("  ❌ Failed to parse LLM response as JSON")
        print(f"  Raw response: {raw[:200]}")
        return None

    # Schema validation — enforce required fields and types
    report = _validate_report_schema(report)
    if not report:
        print("  ❌ Report failed schema validation — discarding")
        return None

    report["llm_source"] = source_used
    report["articles_analyzed"] = len(articles)
    report["sources_used"] = list(set(a["source"] for a in articles))

    # ── Myanmar Summary (separate Groq call) ──────────────────
    print("  🇲🇲 Generating Myanmar summary...")
    report["myanmar_summary"] = _generate_myanmar_summary(report)

    return report


if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from collectors.rss_collector import collect_articles
    from funnel.intelligence_funnel import run_funnel

    print("🧠 GNI Nexus Analyzer — Test Run\n")

    if GITHUB_ACTIONS:
        print("  Mode: GitHub Actions (Groq)\n")
    else:
        print("  Mode: Local (Ollama + Groq fallback)\n")
        try:
            r = requests.get("http://localhost:11434", timeout=3)
            print("  ✅ Ollama is running\n")
        except Exception:
            print("  ⚠️  Ollama not running — will use Groq fallback\n")

    raw = collect_articles(max_per_source=20)
    top = run_funnel(raw, top_n=10, max_per_source=3)

    print("\n🔬 Analyzing top articles...\n")
    report = analyze(top)

    if report:
        print("\n📊 GNI REPORT:")
        print(f"  Title:           {report.get('title')}")
        print(f"  Sentiment:       {report.get('sentiment')} ({report.get('sentiment_score')})")
        print(f"  Risk Level:      {report.get('risk_level')}")
        print(f"  Location:        {report.get('location_name')}")
        print(f"  Tickers:         {report.get('tickers_affected')}")
        print(f"  LLM Used:        {report.get('llm_source')}")
        print(f"  Market Impact:   {report.get('market_impact')}")
        print(f"\n  Summary:\n  {report.get('summary')}")
        print(f"\n  Myanmar Summary:\n  {report.get('myanmar_summary')}")
    else:
        print("  ❌ Analysis failed")
