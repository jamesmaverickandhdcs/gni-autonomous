import os
import time
import sys
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from collectors.rss_collector import collect_articles
from funnel.intelligence_funnel import run_funnel
from analysis.nexus_analyzer import analyze
from analysis.quality_scorer import score_report
from analysis.mad_protocol import run_mad_protocol, _save_predictions
from analysis.semantic_validator import validate_report
from analysis.prompt_manager import seed_prompt_variants, get_active_prompt, update_prompt_score, update_mad_confidence
from analysis.credibility_model import seed_initial_credibility, update_credibility_scores
from analysis.historical_correlations import update_correlations, get_historical_context
from analysis.deception_detector import enrich_report_with_deception
from analysis.frequency_controller import get_recommended_interval, log_frequency_decision
from analysis.audit_trail import log_audit_event
from analysis.code_fix_suggester import run_code_fix_suggester
from analysis.source_health_monitor import run_source_health_check
from analysis.keyword_sensor import run_keyword_sensor
from analysis.staging_checker import run_staging_checks
from analysis.health_agent import run_health_checks
from analysis.weekly_digest import should_generate_digest, generate_weekly_digest
from analysis.escalation_scorer import score_escalation
from analysis.supabase_saver import (
    check_recent_duplicate,
    save_report,
    save_pipeline_run,
    save_pipeline_articles,
    save_article_events,
    save_runtime_log,
    get_pipeline_run_count,
)
from notifications.telegram_notifier import notify_report

# ============================================================
# GNI Main Pipeline â€” Day 6
# Full orchestration with Explainable AI article trace
# ============================================================

GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS", "false").lower() == "true"


def run_pipeline():
    run_start = datetime.now(timezone.utc)
    run_at = run_start.isoformat()
    step_timings = {}
    status = "success"
    error_message = ""
    articles_collected = 0
    articles_after_funnel = 0
    total_after_relevance = 0
    total_after_dedup = 0
    reports_saved = 0
    report_id = None
    run_id = None
    trace = []
    report = None
    top_articles = []

    print("=" * 60)
    print("ðŸŒ GNI â€” Global Nexus Insights")
    print(f"   Pipeline Start: {run_at}")
    print("=" * 60)

    # -- Pre-flight: LLM Health Probe -----------------------
    # Catches Tier 3 failures before the pipeline starts.
    # If Groq is down, abort immediately — no wasted compute.
    print("\n\U0001f52c Pre-flight: LLM health probe...")
    from analysis.llm_health_probe import run_llm_health_probe
    probe = run_llm_health_probe()
    if not probe["healthy"]:
        _probe_error = probe.get("error", "LLM probe failed")
        print(f"  \u274c LLM probe FAILED \u2014 aborting pipeline: {_probe_error}")
        log_audit_event("TIER3_PROBE_FAILED", {"error": _probe_error})
        save_runtime_log(
            run_at=run_at,
            total_seconds=0,
            articles_collected=0,
            articles_after_funnel=0,
            reports_saved=0,
            step_timings={},
            status="failed",
            error_message=f"LLM probe failed: {_probe_error}",
        )
        return False
    if probe["fallback_ok"] and probe["model_used"]:
        os.environ["GROQ_MODEL"] = probe["model_used"]
        print(f"  \u26a0\ufe0f  GROQ_MODEL set to fallback: {probe['model_used']}")
        log_audit_event("GROQ_MODEL_FALLBACK_ACTIVE", {"model": probe["model_used"]})

    try:
        # â”€â”€ Step 1: Collect Articles â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        print("\nðŸ“¡ Step 1: Collecting RSS Articles...")
        t0 = time.time()
        articles = collect_articles(max_per_source=20)
        step_timings["collection"] = round(time.time() - t0, 2)
        articles_collected = len(articles)

        # -- Source health check (RSS failure detection) --------
        from collectors.rss_collector import SOURCES as RSS_SOURCES
        print("\n  Checking source health...")
        run_source_health_check(articles, RSS_SOURCES)

        # -- Emerging keyword detection --------------------------
        if GITHUB_ACTIONS:
            print("  Scanning for emerging keywords...")
            run_keyword_sensor(articles)

        if articles_collected < 10:
            raise Exception(f"Too few articles: {articles_collected}")

        # â”€â”€ Step 2: Intelligence Funnel â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        print("\nðŸ”½ Step 2: Running Intelligence Funnel...")
        t0 = time.time()
        top_n = 5 if GITHUB_ACTIONS else 10
        top_articles, trace = run_funnel(
            articles,
            top_n=top_n,
            max_per_source=3
        )
        step_timings["funnel"] = round(time.time() - t0, 2)
        articles_after_funnel = len(top_articles)

        total_after_relevance = len([a for a in trace if a.get("stage1_passed")])
        total_after_dedup = len([a for a in trace if a.get("stage2_passed")])

        if articles_after_funnel < 3:
            raise Exception(f"Too few after funnel: {articles_after_funnel}")

        # -- Step 2b: Report Deduplication ----------------
        print("\n🔄 Step 2b: Checking for Duplicate Topics...")
        duplicate = check_recent_duplicate(top_articles, hours=6, overlap_threshold=0.7)
        if duplicate:
            print(f"   ⚠️  SKIPPED — same topic covered {duplicate['created_at'][:16]}")
            print(f"   Recent: {duplicate['title'][:60]}")
            save_runtime_log(
                run_at=run_at,
                total_seconds=round((datetime.now(timezone.utc) - run_start).total_seconds(), 2),
                articles_collected=articles_collected,
                articles_after_funnel=articles_after_funnel,
                reports_saved=0,
                step_timings=step_timings,
                status="success",
                error_message=f"Duplicate topic: {duplicate['title'][:80]}",
            )
            return True
        print("   ✅ No duplicate — proceeding with analysis")

        # -- Step 2c: Prompt A/B Selection ---------------
        seed_initial_credibility()
        seed_prompt_variants()
        # Use actual pipeline run count for true A/B alternation (L23: no hardcoded names)
        run_count_hash = get_pipeline_run_count()
        prompt_template, prompt_version = get_active_prompt(run_count_hash)

        # â”€â”€ Step 3: AI Analysis â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        print("\nðŸ§  Step 3: AI Analysis (Llama 3)...")
        t0 = time.time()
        report = analyze(top_articles, prompt_override=prompt_template)
        step_timings["analysis"] = round(time.time() - t0, 2)

        if not report:
            raise Exception("AI analysis returned no report")

        # -- Step 3b: Quality Scoring ---------------------
        print("\n📊 Step 3b: Scoring Report Quality...")
        quality = score_report(report)
        report['quality_score']     = quality['quality_score']
        report['quality_breakdown'] = quality['quality_breakdown']
        report['quality_badge']     = quality['quality_badge']
        update_prompt_score(prompt_version, quality['quality_score'])
        run_count_hash_mod = run_count_hash % 10
        if run_count_hash_mod == 0:
            print("\n\U0001f4ca Updating source credibility scores...")
            update_credibility_scores()
            update_correlations()
            print("\n\U0001f916 Running Health Agent checks...")
            health = run_health_checks()
            print(f"   Health: {health['status']} ({health['checks_passed']}/{health['checks_total']} checks, {health['alert_count']} alerts)")
        if should_generate_digest():
            print("\n\U0001f4c5 Sunday detected — generating weekly digest...")
            generate_weekly_digest(weeks_ago=1)

        # -- Step 3e: Semantic Validation ---------------
        print("\n🧪 Step 3e: Semantic Validation...")
        validation = validate_report(report)
        report = validation['fixed_report']
        if validation['warnings']:
            for w in validation['warnings']:
                print(f"   ⚠️  {w}")
        if not validation['is_valid']:
            raise Exception(f"Report failed semantic validation: {validation['errors']}")
        print(f"   ✅ Semantic validation passed ({validation['checks_passed']}/{validation['total_checks']} checks)")

        # -- Step 3c: MAD Protocol ------------------------
        print("\n🐂🐻 Step 3c: Running Quadratic MAD Protocol...")
        t0 = time.time()
        # Quadratic MAD: pass ALL relevant articles (301) + report_id for prediction saving
        all_relevant = [a for a in trace if a.get('stage1_passed', False)]
        mad_result = run_mad_protocol(report, all_articles=all_relevant)
        # Unpack all Quadratic MAD fields
        report['mad_bull_case']             = mad_result.get('mad_bull_case', '')
        report['mad_bear_case']             = mad_result.get('mad_bear_case', '')
        report['mad_black_swan_case']        = mad_result.get('mad_black_swan_case', '')
        report['mad_ostrich_case']           = mad_result.get('mad_ostrich_case', '')
        report['mad_verdict']               = mad_result.get('mad_verdict', 'neutral')
        report['mad_confidence']            = mad_result.get('mad_confidence', 0.5)
        report['mad_blind_spot']            = mad_result.get('mad_blind_spot', '')
        report['mad_action_recommendation'] = mad_result.get('mad_action_recommendation', '')
        report['short_focus_threats']       = mad_result.get('short_focus_threats', '')
        report['long_shoot_threats']        = mad_result.get('long_shoot_threats', '')
        report['short_verify_days']         = mad_result.get('short_verify_days', 14)
        report['long_verify_days']          = mad_result.get('long_verify_days', 180)
        report['mad_round1_positions']      = mad_result.get('mad_round1_positions', {})
        report['mad_round2_positions']      = mad_result.get('mad_round2_positions', {})
        report['mad_round3_positions']      = mad_result.get('mad_round3_positions', {})
        report['mad_arb_feedbacks']         = mad_result.get('mad_arb_feedbacks', {})
        report['mad_historian_case']        = mad_result.get('mad_historian_case', '')
        report['mad_risk_case']             = mad_result.get('mad_risk_case', '')
        # -- Step 3f: Deception Detection -----------------
        print("\n\U0001f575  Step 3f: Deception Detection...")
        report = enrich_report_with_deception(report, top_articles)

        report['mad_reasoning']  = mad_result.get('mad_reasoning', '')

        # -- Step 3d: Escalation Scoring ------------------
        print("\n🚨 Step 3d: Scoring Escalation Risk...")
        escalation = score_escalation(top_articles)
        report['escalation_score'] = escalation['escalation_score']
        report['escalation_level'] = escalation['escalation_level']
        recommended_interval = get_recommended_interval(escalation['escalation_level'], escalation['escalation_score'])
        log_frequency_decision(escalation['escalation_score'], escalation['escalation_level'], recommended_interval, f"Escalation {escalation['escalation_level']} {escalation['escalation_score']}/10")
        print(f"   ⏱  Next run recommended in {recommended_interval:.1f}h ({escalation['escalation_level']})")
        hist_context = get_historical_context(escalation['escalation_score'])
        if hist_context:
            report['historical_context'] = hist_context
            print(f"   📊 {hist_context}")
        print(f"   ✅ Escalation: {escalation['escalation_level']} ({escalation['escalation_score']}/10) — {escalation['active_pillars']}/3 pillars active")
        step_timings["mad"] = round(time.time() - t0, 2)
        print(f"   ✅ MAD verdict: {report['mad_verdict']} ({report['mad_confidence']:.0%} confidence)")
        update_mad_confidence(prompt_version, report['mad_confidence'])

        # ── Step 4: Save Report
        print("\nðŸ’¾ Step 4: Saving Report to Supabase...")
        t0 = time.time()
        report_id = save_report(report, top_articles,
            quality_score=report.get('quality_score', 0),
            quality_breakdown=report.get('quality_breakdown', {}))
        step_timings["save"] = round(time.time() - t0, 2)

        if report_id:
            reports_saved = 1
            # Save debate predictions now that we have real report_id
            _save_predictions(
                report_id=report_id,
                short=report.get('short_focus_threats', ''),
                long_s=report.get('long_shoot_threats', ''),
                short_days=report.get('short_verify_days', 14),
                long_days=report.get('long_verify_days', 180),
                round3=report.get('mad_round3_positions', {}),
            )
            log_audit_event('REPORT_SAVED', {'quality_score': report.get('quality_score', 0), 'sentiment': report.get('sentiment', ''), 'escalation_level': report.get('escalation_level', ''), 'mad_verdict': report.get('mad_verdict', ''), 'deception_level': report.get('deception_level', '')}, report_id=report_id)

        # â”€â”€ Step 5: Save Pipeline Run & Article Trace â”€â”€â”€â”€â”€â”€â”€
        print("\nðŸ“Š Step 5: Saving Pipeline Run & Article Trace...")
        total_seconds_so_far = round(
            (datetime.now(timezone.utc) - run_start).total_seconds(), 2
        )
        run_id = save_pipeline_run(
            run_at=run_at,
            report_id=report_id,
            total_collected=articles_collected,
            total_after_relevance=total_after_relevance,
            total_after_dedup=total_after_dedup,
            total_after_funnel=articles_after_funnel,
            llm_source=report.get("llm_source", "unknown") if report else "unknown",
            status="success",
            duration_seconds=total_seconds_so_far,
        )

        if run_id and trace:
            save_pipeline_articles(run_id, trace)
            save_article_events(run_id, report_id, trace)

        # â”€â”€ Step 6: Telegram Notification â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        if report and report_id:
            notify_report(report, top_articles)

    except Exception as e:
        status = "failed"
        error_message = str(e)
        print(f"\nâŒ Pipeline error: {e}")

    finally:
        # â”€â”€ Step 7: Save Runtime Log â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        total_seconds = round(
            (datetime.now(timezone.utc) - run_start).total_seconds(), 2
        )
        print(f"\nðŸ“‹ Step 7: Saving Runtime Log...")
        save_runtime_log(
            run_at=run_at,
            total_seconds=total_seconds,
            articles_collected=articles_collected,
            articles_after_funnel=articles_after_funnel,
            reports_saved=reports_saved,
            step_timings=step_timings,
            status=status,
            error_message=error_message,
        )

        print("\n" + "=" * 60)
        print(f"  Status:             {status.upper()}")
        print(f"  Total Time:         {total_seconds}s")
        print(f"  Articles Collected: {articles_collected}")
        print(f"  After Funnel:       {articles_after_funnel}")
        print(f"  Reports Saved:      {reports_saved}")
        print(f"  Pipeline Run ID:    {run_id[:8] if run_id else 'N/A'}...")
        print(f"  Article Trace:      {len(trace)} articles documented")
        print(f"  Step Timings:       {step_timings}")
        print("=" * 60)

        # -- Staging regression check ------------------
        if status == "success" and GITHUB_ACTIONS:
            print("\n📸 Post-pipeline: staging regression check...")
            staging = run_staging_checks()
            if staging['failed'] > 0:
                print(f"  ⚠️  Staging check: {staging['failed']} page(s) failed")
            else:
                print(f"  ✅ Staging check: all {staging['total']} pages OK")


        # -- Phase 1 code fix suggester ---------------
        if GITHUB_ACTIONS:
            print("\n🔧 Checking for fix suggestions...")
            run_code_fix_suggester()
        return status == "success"


if __name__ == "__main__":
    success = run_pipeline()
    sys.exit(0 if success else 1)



