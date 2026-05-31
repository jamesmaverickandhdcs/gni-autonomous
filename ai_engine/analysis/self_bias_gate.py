# ============================================================
# GNI Self-Bias Gate -- PHI-003 self-audit
# "An anti-pretense instrument that is never itself audited
#  becomes the purest form of pretense." -- S39 fourth analyst
#
# GNI audits its sources (NN-PHI-5/6), its inputs (injection),
# its absences (NN-PHI-5). Nothing audited GNI's OWN OUTPUT for
# internal contradiction -- until the escalation latch broadcast
# manufactured fear for days while sentiment said calm.
#
# This gate reads GNI's recent reports and flags where the system
# contradicts itself or violates an NN-PHI. Findings are written to
# the tamper-evident audit_trail chain (SELF_BIAS_FLAG) so the audit
# of GNI cannot itself be quietly rewritten.
# ============================================================
import os
import sys
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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


def _fetch_recent_reports(hours: int = 24) -> list[dict]:
    """Pull reports written in the last `hours` for coherence auditing."""
    client = _get_client()
    if not client:
        return []
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
    try:
        result = client.table("reports") \
            .select("id, title, created_at, escalation_score, escalation_level, "
                    "sentiment, sentiment_score, risk_level, combo_bonus, "
                    "fff_human_path") \
            .gte("created_at", cutoff) \
            .order("created_at", desc=True) \
            .execute()
        return result.data or []
    except Exception as e:
        # combo_bonus may not be a stored column -- retry without it
        try:
            result = client.table("reports") \
                .select("id, title, created_at, escalation_score, escalation_level, "
                        "sentiment, sentiment_score, risk_level, fff_human_path") \
                .gte("created_at", cutoff) \
                .order("created_at", desc=True) \
                .execute()
            return result.data or []
        except Exception as e2:
            print(f"  Warning: Could not fetch reports: {str(e2)[:80]}")
            return []


# ---- Check 1: escalation must agree with honest sentiment/risk (NN-PHI-1) ----
def _check_escalation_sentiment(r: dict) -> dict | None:
    """
    Flag a report where escalation screams CRITICAL/HIGH while GNI's own
    LLM read says calm (Bullish/Neutral + Low/Medium). This is the bug the
    PHI-003 escalation gate fixed -- this check is its permanent regression
    guard. A flag here means either the gate regressed or was bypassed.
    """
    level = (r.get("escalation_level") or "").upper()
    sentiment = (r.get("sentiment") or "").strip().lower()
    risk = (r.get("risk_level") or "").strip().lower()

    if level not in ("CRITICAL", "HIGH"):
        return None
    calm_sentiment = sentiment in ("bullish", "neutral")
    calm_risk = risk in ("low", "medium")
    if not (calm_sentiment and calm_risk):
        return None

    # Ostrich guard: a genuine critical combo legitimately overrides a calm
    # read. If combo_bonus is stored and >= 3, this is NOT a contradiction.
    combo = r.get("combo_bonus")
    if combo is not None and combo >= 3:
        return None

    return {
        "check": "escalation_sentiment",
        "nn_phi": "NN-PHI-1",
        "report_id": r.get("id"),
        "title": (r.get("title") or "")[:80],
        "detail": (f"escalation={level} but sentiment={r.get('sentiment')} "
                   f"risk={r.get('risk_level')} -- manufactured fear (no critical combo)"),
        "escalation_score": r.get("escalation_score"),
    }


# ---- Check 2: every threat must have a path (NN-PHI-4) ----
def _check_threat_has_path(r: dict) -> dict | None:
    """
    Flag a High/Critical-risk report whose fff_human_path is empty or
    dismissive. NN-PHI-4: 'Every threat must have a path.' A threat with
    no path violates the core mission -- fear without agency.
    """
    risk = (r.get("risk_level") or "").strip().lower()
    if risk not in ("high", "critical"):
        return None

    path = (r.get("fff_human_path") or "").strip()
    if len(path) >= 40:  # a real path is a sentence or more
        return None

    return {
        "check": "threat_has_path",
        "nn_phi": "NN-PHI-4",
        "report_id": r.get("id"),
        "title": (r.get("title") or "")[:80],
        "detail": (f"risk={r.get('risk_level')} but fff_human_path is "
                   f"{'empty' if not path else 'too thin (' + str(len(path)) + ' chars)'} "
                   f"-- threat without a path"),
        "escalation_score": r.get("escalation_score"),
    }


# ---- Check 3: required output fields must not be silently empty (NN-PHI-1) ----
# Conservative whitelist -- only fields that are ALWAYS required on a real
# report. A blank here means GNI published incomplete intelligence as if
# complete -- a small pretense (PHI-001) and a Freedom-from-Fear failure if
# the missing field is the human path (PHI-003). Sibling-class of the
# published_at/url silent-empty bugs found by the S40 silent-fail sweep.
_REQUIRED_NONEMPTY = ("title", "sentiment", "risk_level")

def _check_required_field_empty(r: dict) -> dict | None:
    missing = [f for f in _REQUIRED_NONEMPTY if not (r.get(f) or "").strip()]
    if not missing:
        return None
    return {
        "check": "required_field_empty",
        "nn_phi": "NN-PHI-1",
        "report_id": r.get("id"),
        "title": (r.get("title") or "")[:80],
        "detail": ("required field(s) silently empty: " + ", ".join(missing) +
                   " -- incomplete intelligence presented as complete"),
        "escalation_score": r.get("escalation_score"),
    }


CHECKS = [
    _check_escalation_sentiment,
    _check_threat_has_path,
    _check_required_field_empty,
]


def _check_flatline(reports: list[dict]) -> list[dict]:
    """
    Set-level check (NN-PHI-1 + NN-PHI-3): a numeric field frozen bit-identical
    across many consecutive reports is the latch signature -- the escalation
    bug that broadcast CRITICAL 10.0 for days while the world changed. Genuine
    analysis always has some jitter; perfect constancy across N+ distinct runs
    is manufactured constancy, a pretense. Conservative: needs >= 4 reports and
    EXACT equality (mild stability does not trip it).
    """
    findings = []
    if len(reports) < 4:
        return findings
    for field in ("escalation_score", "sentiment_score"):
        vals = [r.get(field) for r in reports]
        if any(v is None for v in vals):
            continue
        if len(set(vals)) == 1:  # bit-identical across every report
            findings.append({
                "check": "flatline",
                "nn_phi": "NN-PHI-1/3",
                "report_id": reports[0].get("id"),
                "title": (reports[0].get("title") or "")[:80],
                "detail": (f"{field} frozen at {vals[0]} across {len(vals)} consecutive "
                           f"reports -- possible latch (manufactured constancy)"),
                "escalation_score": reports[0].get("escalation_score"),
            })
    return findings


def run_self_bias_audit(hours: int = 24) -> dict:
    """
    Main entry point. Reads recent reports, runs every coherence check,
    writes findings (or a clean record) to the tamper-evident audit_trail.

    Returns dict: {findings: [...], reports_audited: N, clean: bool}
    """
    print("  SELF-BIAS GATE: auditing GNI's own recent output...")
    reports = _fetch_recent_reports(hours)
    findings = []
    for r in reports:
        for check in CHECKS:
            f = check(r)
            if f:
                findings.append(f)

    # Set-level checks (compare across reports, not per-row)
    findings.extend(_check_flatline(reports))

    # Write to the tamper-evident chain -- the audit of GNI cannot be rewritten
    try:
        from analysis.audit_trail import log_audit_event
    except Exception:
        try:
            from audit_trail import log_audit_event
        except Exception:
            log_audit_event = None

    if log_audit_event:
        if findings:
            log_audit_event("SELF_BIAS_FLAG", {
                "reports_audited": len(reports),
                "finding_count": len(findings),
                "findings": findings,
            })
        else:
            # Absence of findings is itself recorded -- proves the gate ran
            log_audit_event("SELF_BIAS_AUDIT_CLEAN", {
                "reports_audited": len(reports),
                "window_hours": hours,
            })

    if findings:
        print(f"  SELF-BIAS GATE: {len(findings)} contradiction(s) in {len(reports)} reports")
        for f in findings:
            print(f"    [{f['nn_phi']}] {f['check']}: {f['detail']}")
    else:
        print(f"  SELF-BIAS GATE: clean -- {len(reports)} reports audited, no contradictions")

    return {
        "findings": findings,
        "reports_audited": len(reports),
        "clean": len(findings) == 0,
    }


if __name__ == "__main__":
    result = run_self_bias_audit()
    print(f"\nSelf-bias audit complete: "
          f"{result['reports_audited']} audited, "
          f"{len(result['findings'])} flagged, "
          f"clean={result['clean']}")
