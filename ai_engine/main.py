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
from analysis.mad_protocol import run_mad_protocol
from analysis.supabase_saver import (
    save_report,
    save_pipeline_run,
    save_pipeline_articles,
    save_article_events,
    save_runtime_log,
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

    try:
        # â”€â”€ Step 1: Collect Articles â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        print("\nðŸ“¡ Step 1: Collecting RSS Articles...")
        t0 = time.time()
        articles = collect_articles(max_per_source=20)
        step_timings["collection"] = round(time.time() - t0, 2)
        articles_collected = len(articles)

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

        # â”€â”€ Step 3: AI Analysis â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        print("\nðŸ§  Step 3: AI Analysis (Llama 3)...")
        t0 = time.time()
        report = analyze(top_articles)
        step_timings["analysis"] = round(time.time() - t0, 2)

        if not report:
            raise Exception("AI analysis returned no report")

        # -- Step 3b: Quality Scoring ---------------------
        print("\n📊 Step 3b: Scoring Report Quality...")
        quality = score_report(report)
        report['quality_score']     = quality['quality_score']
        report['quality_breakdown'] = quality['quality_breakdown']
        report['quality_badge']     = quality['quality_badge']

        # -- Step 3c: MAD Protocol ------------------------
        print("\n🐂🐻 Step 3c: Running MAD Protocol (Multi-Agent Debate)...")
        t0 = time.time()
        mad_result = run_mad_protocol(report)
        report['mad_bull_case']  = mad_result['mad_bull_case']
        report['mad_bear_case']  = mad_result['mad_bear_case']
        report['mad_verdict']    = mad_result['mad_verdict']
        report['mad_confidence'] = mad_result['mad_confidence']
        step_timings["mad"] = round(time.time() - t0, 2)
        print(f"   ✅ MAD verdict: {report['mad_verdict']} ({report['mad_confidence']:.0%} confidence)")

        # ── Step 4: Save Report
        print("\nðŸ’¾ Step 4: Saving Report to Supabase...")
        t0 = time.time()
        report_id = save_report(report, top_articles,
            quality_score=report.get('quality_score', 0),
            quality_breakdown=report.get('quality_breakdown', {}))
        step_timings["save"] = round(time.time() - t0, 2)

        if report_id:
            reports_saved = 1

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

        return status == "success"


if __name__ == "__main__":
    success = run_pipeline()
    sys.exit(0 if success else 1)



