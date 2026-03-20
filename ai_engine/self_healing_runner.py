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
