# ============================================================
# GNI LLM Health Probe
# Pre-run check: verify Groq responds with valid JSON
# before the full pipeline attempts expensive analysis.
# L23: Model name from env var — never hardcoded
# L33: llama-3.3-70b-versatile as Groq default
# ============================================================

import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_MODEL_FALLBACK = os.getenv("GROQ_MODEL_FALLBACK", "llama-3.1-8b-instant")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

_PROBE_PROMPT = 'You are a JSON API. Respond ONLY with this exact JSON, nothing else: {"status": "ok", "model": "ready"}'

_REQUIRED_KEYS = {"status", "model"}


def _call_probe(model, timeout=10):
    """Send probe to a single model. Returns parsed JSON or None."""
    try:
        response = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": _PROBE_PROMPT}],
                "temperature": 0.0,
                "max_tokens": 50,
            },
            timeout=timeout,
        )
        if response.status_code != 200:
            print(f"  ⚠️  Probe HTTP {response.status_code} for model {model}")
            return None

        raw = response.json()["choices"][0]["message"]["content"].strip()

        # Strip markdown fences if present
        if raw.startswith("```"):
            lines = raw.split("\n")
            raw = "\n".join(lines[1:]).replace("```", "").strip()

        parsed = json.loads(raw)
        if not _REQUIRED_KEYS.issubset(parsed.keys()):
            print(f"  ⚠️  Probe response missing required keys: {parsed}")
            return None

        return parsed

    except json.JSONDecodeError as e:
        print(f"  ⚠️  Probe JSON parse failed for {model}: {e}")
        return None
    except Exception as e:
        print(f"  ⚠️  Probe error for {model}: {e}")
        return None


def run_llm_health_probe():
    """
    Run LLM health probe before pipeline starts.
    Returns dict with healthy, model_used, primary_ok, fallback_ok, error.
    """
    if not GROQ_API_KEY:
        return {
            "healthy": False,
            "model_used": None,
            "primary_ok": False,
            "fallback_ok": False,
            "error": "No GROQ_API_KEY in environment",
        }

    print("  🧪 Checking Groq primary model...")

    result = _call_probe(GROQ_MODEL)
    if result:
        print(f"  ✅ Groq probe passed — primary model ready ({GROQ_MODEL})")
        return {
            "healthy": True,
            "model_used": GROQ_MODEL,
            "primary_ok": True,
            "fallback_ok": False,
            "error": None,
        }

    print(f"  ⚠️  Primary model failed — trying fallback ({GROQ_MODEL_FALLBACK})")

    result = _call_probe(GROQ_MODEL_FALLBACK)
    if result:
        print(f"  ✅ Groq probe passed — fallback model ready ({GROQ_MODEL_FALLBACK})")
        return {
            "healthy": True,
            "model_used": GROQ_MODEL_FALLBACK,
            "primary_ok": False,
            "fallback_ok": True,
            "error": f"Primary model {GROQ_MODEL} unavailable — using fallback",
        }

    error_msg = f"Both models failed probe: {GROQ_MODEL} and {GROQ_MODEL_FALLBACK}"
    print(f"  ❌ {error_msg}")
    return {
        "healthy": False,
        "model_used": None,
        "primary_ok": False,
        "fallback_ok": False,
        "error": error_msg,
    }


if __name__ == "__main__":
    print("\n🔬 GNI LLM Health Probe — Manual Test\n")
    probe = run_llm_health_probe()
    print(f"\n  Healthy:     {probe['healthy']}")
    print(f"  Model used:  {probe['model_used']}")
    print(f"  Primary ok:  {probe['primary_ok']}")
    print(f"  Fallback ok: {probe['fallback_ok']}")
    if probe['error']:
        print(f"  Error:       {probe['error']}")
