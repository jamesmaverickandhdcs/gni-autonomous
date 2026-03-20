# ============================================================
# GNI Immutable Audit Trail — Day 16
# Cryptographic hash chain for report integrity
# Each entry hashes: event_data + previous_hash
# Tamper detection: any change breaks the chain
# ============================================================

import os
import json
import hashlib
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")

GENESIS_HASH = "0" * 64  # Starting hash for first entry


def _get_client():
    try:
        from supabase import create_client
        if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
            return None
        return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    except Exception:
        return None


def _compute_hash(event_type: str, event_data: dict, previous_hash: str) -> str:
    """Compute SHA-256 hash of event + previous hash."""
    payload = json.dumps({
        "event_type": event_type,
        "event_data": event_data,
        "previous_hash": previous_hash,
    }, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _get_latest_hash() -> str:
    """Get the hash of the most recent audit entry."""
    client = _get_client()
    if not client:
        return GENESIS_HASH
    try:
        result = client.table("audit_trail")             .select("hash")             .order("created_at", desc=True)             .limit(1)             .execute()
        if result.data:
            return result.data[0]["hash"]
        return GENESIS_HASH
    except Exception:
        return GENESIS_HASH


def log_audit_event(
    event_type: str,
    event_data: dict,
    report_id: str = None,
) -> str | None:
    """
    Log an immutable audit event.
    Returns the hash of this entry or None on failure.

    Event types:
        REPORT_SAVED — report written to Supabase
        PIPELINE_RUN — pipeline execution record
        QUALITY_SCORED — quality scoring completed
        MAD_VERDICT — MAD protocol verdict
        ESCALATION — escalation score computed
        SECURITY_FLAG — injection/semantic validation issue
        DECEPTION_FLAG — coordination detected
        SYSTEM_START — pipeline startup
    """
    client = _get_client()
    if not client:
        return None

    try:
        previous_hash = _get_latest_hash()
        current_hash = _compute_hash(event_type, event_data, previous_hash)

        client.table("audit_trail").insert({
            "report_id": report_id,
            "event_type": event_type,
            "event_data": event_data,
            "hash": current_hash,
            "previous_hash": previous_hash,
        }).execute()

        return current_hash

    except Exception as e:
        print(f"  ⚠️  Audit log failed: {e}")
        return None


def verify_chain_integrity() -> dict:
    """
    Verify the entire audit chain is unbroken.
    Returns dict with is_valid, total_entries, broken_at.
    """
    client = _get_client()
    if not client:
        return {"is_valid": False, "error": "No Supabase connection"}

    try:
        result = client.table("audit_trail")             .select("id, event_type, event_data, hash, previous_hash, created_at")             .order("created_at", desc=False)             .execute()

        entries = result.data or []
        if not entries:
            return {"is_valid": True, "total_entries": 0, "message": "Empty chain"}

        broken_at = None
        for i, entry in enumerate(entries):
            expected_prev = GENESIS_HASH if i == 0 else entries[i-1]["hash"]
            if entry["previous_hash"] != expected_prev:
                broken_at = entry["id"]
                break

            # Recompute hash
            computed = _compute_hash(
                entry["event_type"],
                entry["event_data"],
                entry["previous_hash"]
            )
            if computed != entry["hash"]:
                broken_at = entry["id"]
                break

        return {
            "is_valid": broken_at is None,
            "total_entries": len(entries),
            "broken_at": broken_at,
            "latest_hash": entries[-1]["hash"][:16] + "..." if entries else None,
        }

    except Exception as e:
        return {"is_valid": False, "error": str(e)}


def get_recent_audit_events(limit: int = 10) -> list:
    """Get recent audit events for health page."""
    client = _get_client()
    if not client:
        return []
    try:
        result = client.table("audit_trail")             .select("event_type, hash, created_at, report_id")             .order("created_at", desc=True)             .limit(limit)             .execute()
        return result.data or []
    except Exception:
        return []


if __name__ == "__main__":
    print("\U0001f512 GNI Immutable Audit Trail — Test Run\n")

    # Log test events
    h1 = log_audit_event("SYSTEM_START", {"version": "Day 16", "sources": 13})
    print(f"  Event 1 hash: {h1[:16] if h1 else 'FAILED'}...")

    h2 = log_audit_event("PIPELINE_RUN", {"articles": 242, "status": "success"})
    print(f"  Event 2 hash: {h2[:16] if h2 else 'FAILED'}...")

    h3 = log_audit_event("REPORT_SAVED", {"quality_score": 9.25, "sentiment": "Bearish"}, report_id=None)
    print(f"  Event 3 hash: {h3[:16] if h3 else 'FAILED'}...")

    # Verify chain
    result = verify_chain_integrity()
    print(f"\n  Chain valid:   {result['is_valid']}")
    print(f"  Total entries: {result['total_entries']}")
    print(f"  Latest hash:   {result.get('latest_hash', 'N/A')}")
