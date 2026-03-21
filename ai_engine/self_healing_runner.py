# ============================================================
# GNI Self-Healing Runner — Day 16
# Wraps pipeline with auto-retry on Tier 1+2 failures
# Tier 1: Collection failures (RSS down) — retry 3x
# Tier 2: Funnel failures (no articles) — retry 2x
# Tier 3+: Analysis failures — do not retry (expensive)
# ============================================================

import os
import sys
import time
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()

# Max retries per tier
TIER1_MAX_RETRIES = 3  # RSS collection
TIER2_MAX_RETRIES = 2  # Intelligence funnel
RETRY_DELAY_SECONDS = 30  # Wait between retries


def run_with_self_healing():
    """
    Run the GNI pipeline with self-healing retry logic.
    Tier 1+2 failures are retried automatically.
    """
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    from analysis.audit_trail import log_audit_event

    log_audit_event("SYSTEM_START", {
        "version": "Day 16 — Self-Healing Runner",
        "tier1_retries": TIER1_MAX_RETRIES,
        "tier2_retries": TIER2_MAX_RETRIES,
    })

    # ── LLM Health Probe — Tier 3 pre-check ──────────────────
    # Check Groq is responding BEFORE the expensive pipeline runs.
    # Catches Tier 3 failures (model down, API outage) early.
    from analysis.llm_health_probe import run_llm_health_probe
    print("\n🔬 Pre-flight: LLM health probe...")
    probe = run_llm_health_probe()

    if not probe["healthy"]:
        error = probe.get("error", "LLM probe failed")
        print(f"  ❌ LLM probe FAILED — aborting pipeline: {error}")
        log_audit_event("TIER3_PROBE_FAILED", {"error": error})
        # Fire health alert via health_agent if available
        try:
            from analysis.health_agent import fire_health_alert
            fire_health_alert(
                check_name="LLM_PROBE_FAILED",
                details={"error": error, "primary_ok": probe["primary_ok"], "fallback_ok": probe["fallback_ok"]},
                severity="HIGH",
            )
        except Exception as alert_err:
            print(f"  ⚠️  Could not fire health alert: {alert_err}")
        return False

    # If fallback model is being used, set env so all modules use it
    if probe["fallback_ok"] and probe["model_used"]:
        os.environ["GROQ_MODEL"] = probe["model_used"]
        print(f"  ⚠️  GROQ_MODEL overridden to fallback: {probe['model_used']}")
        log_audit_event("GROQ_MODEL_FALLBACK_ACTIVE", {"model": probe["model_used"]})

    attempt = 0
    max_attempts = TIER1_MAX_RETRIES + 1

    while attempt <= max_attempts:
        attempt += 1
        print(f"\n\U0001f504 Pipeline attempt {attempt}/{max_attempts + 1}")

        try:
            from main import run_pipeline
            success = run_pipeline()

            if success:
                log_audit_event("PIPELINE_SUCCESS", {"attempt": attempt})
                return True
            else:
                print(f"  \u26a0\ufe0f  Pipeline returned failure on attempt {attempt}")
                log_audit_event("PIPELINE_FAILURE", {"attempt": attempt, "will_retry": attempt <= max_attempts})

        except Exception as e:
            error_msg = str(e)
            print(f"  \u274c Pipeline exception on attempt {attempt}: {error_msg[:100]}")
            log_audit_event("PIPELINE_ERROR", {"attempt": attempt, "error": error_msg[:200]})

            # Classify error tier
            if "Too few articles" in error_msg or "RSS" in error_msg or "collect" in error_msg.lower():
                tier = 1
                print(f"  \U0001f527 Tier 1 failure (collection) — will retry")
            elif "Too few after funnel" in error_msg or "funnel" in error_msg.lower():
                tier = 2
                print(f"  \U0001f527 Tier 2 failure (funnel) — will retry")
            else:
                tier = 3
                print(f"  \U0001f6d1 Tier 3+ failure (analysis) — no retry")
                log_audit_event("TIER3_FAILURE", {"error": error_msg[:200]})
                return False

        if attempt <= max_attempts:
            print(f"  \u23f1  Waiting {RETRY_DELAY_SECONDS}s before retry...")
            time.sleep(RETRY_DELAY_SECONDS)

    print(f"  \u274c All {max_attempts} attempts failed")
    log_audit_event("ALL_RETRIES_EXHAUSTED", {"attempts": attempt})
    return False


if __name__ == "__main__":
    success = run_with_self_healing()
    sys.exit(0 if success else 1)
