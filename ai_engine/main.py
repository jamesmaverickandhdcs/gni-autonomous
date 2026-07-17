# -*- coding: utf-8 -*-
import os
import time
import sys
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from collectors.rss_collector import collect_articles
from funnel.intelligence_funnel import run_funnel, INJECTION_PATTERNS
from analysis.nexus_analyzer import analyze, get_run_usage
from analysis.quality_scorer import score_report
# MAD protocol moved to mad_runner.py (GNI-R-110 -- separate pipeline)
# from analysis.mad_protocol import run_mad_protocol, _save_predictions
from analysis.semantic_validator import validate_report
from analysis.prompt_manager import seed_prompt_variants, get_active_prompt, update_prompt_score, update_mad_confidence, get_pillar_prompt
from analysis.credibility_model import seed_initial_credibility, update_credibility_scores
from analysis.historical_correlations import update_correlations, get_historical_context
from analysis.deception_detector import enrich_report_with_deception
from analysis.frequency_controller import get_recommended_interval, log_frequency_decision
from analysis.audit_trail import log_audit_event
from analysis.code_fix_suggester import run_code_fix_suggester
from analysis.source_health_monitor import run_source_health_check
# from analysis.keyword_sensor import run_keyword_sensor  # DISABLED: Groq quota saving
from analysis.staging_checker import run_staging_checks
from analysis.health_agent import run_health_checks
from analysis.weekly_digest import should_generate_digest, generate_weekly_digest
from analysis.escalation_scorer import score_escalation
from analysis.supabase_saver import (
    check_recent_duplicate,
    save_report,
    save_pillar_report,
    save_pipeline_run,
    save_pipeline_articles,
    save_article_events,
    save_runtime_log,
    get_pipeline_run_count,
)
from notifications.telegram_notifier import notify_report
from quota_guard import check_quota, log_usage

# ============================================================
# GNI Main Pipeline - Day 6
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
    print("?? GNI - Global Nexus Insights")
    print(f"   Pipeline Start: {run_at}")
    print("=" * 60)

    # -- Pre-flight: LLM Health Probe -----------------------
    # Catches Tier 3 failures before the pipeline starts.
    # If Groq is down, abort immediately ? no wasted compute.
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

    # GNI-R-112: Check quota before pipeline runs
    # sacred=True -- never blocks sacred runs, alerts only
    print("\n\U0001f6e1  Quota check (GNI-R-112)...")
    _quota = check_quota('gni_pipeline', sacred=True, account='not_mad')
    print("  " + _quota['reason'].split("\n")[0])
    print("  Used today: " + str(_quota['tokens_used']) + " tokens | Headroom: " + str(_quota['headroom']) + " tokens")

    try:
        # -- Step 1: Collect Articles ------------------------
        print("\n?? Step 1: Collecting RSS Articles...")
        t0 = time.time()
        articles, source_stats = collect_articles(max_per_source=20)
        step_timings["collection"] = round(time.time() - t0, 2)
        articles_collected = len(articles)

        # -- Source health check (RSS failure detection) --------
        from collectors.rss_collector import SOURCES as RSS_SOURCES
        print("\n  Checking source health...")
        run_source_health_check(articles, RSS_SOURCES, source_stats)

        # -- Emerging keyword detection --------------------------
        if GITHUB_ACTIONS:
            print("  Scanning for emerging keywords...")
            # run_keyword_sensor(articles)  # DISABLED: Groq quota saving

        if articles_collected < 10:
            raise Exception(f"Too few articles: {articles_collected}")

        # -- NN-PHI-5: Absence Detection -------------------
        try:
            from analysis.absence_detector import run_absence_detection
            _gaps = run_absence_detection(articles)
            if _gaps:
                _gap_msg = "  ⚠️  COVERAGE GAPS DETECTED:\n"
                for _g in _gaps[:3]:
                    _gap_msg += f"    [{_g['gap_severity']}] '{_g['keyword']}' — 7d_avg={_g['avg_7day']} today=0\n"
                print(_gap_msg)
                try:
                    from notifications.telegram_notifier import send_admin_message
                    _tg_gaps = "🚫 [GNI ABSENCE ALERT] Coverage gaps detected:\n"
                    for _g in _gaps[:5]:
                        _tg_gaps += f"[{_g['gap_severity']}] '{_g['keyword']}' — 7d avg {_g['avg_7day']} articles, today: {_g['today_count']}\n"
                    _tg_gaps += "\nAbsence is intelligence (PHI-003 NN-PHI-5)"
                    send_admin_message(_tg_gaps)
                except Exception:
                    pass
        except Exception as _e:
            print(f"  Warning: Absence detection failed: {str(_e)[:60]}")

        # -- Step 2: Intelligence Funnel ---------------------
        print("\n?? Step 2: Running Intelligence Funnel...")
        t0 = time.time()
        # S39: Cross-run URL deduplication -- load URLs selected in last 24h
        _recently_selected_urls = set()
        try:
            from supabase import create_client as _xr_sc
            from datetime import timedelta as _xr_td
            _xr_sb = _xr_sc(os.getenv("SUPABASE_URL", ""), os.getenv("SUPABASE_SERVICE_KEY", ""))
            _xr_cutoff = (datetime.now(timezone.utc) - _xr_td(hours=24)).isoformat()
            _xr_res = _xr_sb.table("pipeline_articles").select("url").eq("stage4_selected", True).gte("created_at", _xr_cutoff).execute()
            _recently_selected_urls = {r["url"] for r in (_xr_res.data or []) if r.get("url")}
            if _recently_selected_urls:
                print(f"  Cross-run dedup: {len(_recently_selected_urls)} recently-selected URLs loaded")
        except Exception as _xr_e:
            print(f"  Cross-run dedup: skipped ({str(_xr_e)[:60]})")
        top_n = 22 if GITHUB_ACTIONS else 22  # 14 geo + 4 tech + 4 fin (Three Pillar Reports)
        top_articles, trace = run_funnel(
            articles,
            top_n=top_n,
            max_per_source=2,  # D1: source diversity (PHI-003)
            excluded_urls=_recently_selected_urls
        )
        step_timings["funnel"] = round(time.time() - t0, 2)
        articles_after_funnel = len(top_articles)

        total_after_relevance = len([a for a in trace if a.get("stage1_passed")])
        total_after_dedup = len([a for a in trace if a.get("stage1_passed") and a.get("stage1b_passed", True) and a.get("stage2_passed")])

        if articles_after_funnel < 3:
            raise Exception(f"Too few after funnel: {articles_after_funnel}")

        # -- Step 2b: Report Deduplication ----------------
        print("\n?? Step 2b: Checking for Duplicate Topics...")
        duplicate = check_recent_duplicate(top_articles, hours=6)
        if duplicate:
            print(f"   ??  SKIPPED ? same topic covered {duplicate['created_at'][:16]}")
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
        print("   ? No duplicate ? proceeding with analysis")

        # -- Step 2c: Prompt A/B Selection ---------------
        seed_initial_credibility()
        seed_prompt_variants()
        # Use actual pipeline run count for true A/B alternation (L23: no hardcoded names)
        run_count_hash = get_pipeline_run_count()
        prompt_template, prompt_version = get_active_prompt(run_count_hash)

        # -- Step 3: AI Analysis -----------------------------
        print("\n?? Step 3: AI Analysis (Llama 3)...")
        t0 = time.time()
        report = analyze(top_articles, prompt_override=prompt_template)
        step_timings["analysis"] = round(time.time() - t0, 2)

        if not report:
            raise Exception("AI analysis returned no report")

        # -- Step 3b: Quality Scoring ---------------------
        print("\n?? Step 3b: Scoring Report Quality...")
        quality = score_report(report)
        report['quality_score']     = quality['quality_score']
        report['quality_breakdown'] = quality['quality_breakdown']
        report['quality_badge']     = quality['quality_badge']
        update_prompt_score(prompt_version, quality['quality_score'])

        # Item 15 S38: Feed quality score back into source weights
        # Closes the feedback loop -- good reports reward sources immediately
        # GPVS remains ground truth long-term; quality score = fast signal
        try:
            from analysis.source_weights import update_source_weight as _usw
            _qs = quality.get('quality_score', 0)
            if _qs >= 8.5:
                _magnitude = 0.85   # excellent report -- reward sources
            elif _qs >= 7.0:
                _magnitude = 0.60   # good report -- mild reward
            elif _qs < 6.5:
                _magnitude = 0.20   # poor report -- penalize sources
            else:
                _magnitude = None   # neutral -- no update
            if _magnitude is not None and top_articles:
                _sources_updated = set()
                for _art in top_articles:
                    _src = _art.get('source', '').lower().strip()
                    if _src and _src not in _sources_updated:
                        _usw(_src, _magnitude)
                        _sources_updated.add(_src)
                print(f"  📊 Quality feedback: {_qs:.2f}/10 → magnitude {_magnitude} → {len(_sources_updated)} sources updated")
        except Exception as _qfe:
            print(f"  Warning: Quality→source_weight feedback failed: {str(_qfe)[:60]}")
        run_count_hash_mod = run_count_hash % 10
        if run_count_hash_mod == 0:
            print("\n\U0001f4ca Updating source credibility scores...")
            update_credibility_scores()
            update_correlations()
            print("\n\U0001f916 Running Health Agent checks...")
            health = run_health_checks()
            print(f"   Health: {health['status']} ({health['checks_passed']}/{health['checks_total']} checks, {health['alert_count']} alerts)")
        if should_generate_digest():
            print("\n\U0001f4c5 Sunday detected ? generating weekly digest...")
            generate_weekly_digest(weeks_ago=1)

        # -- Step 3e: Semantic Validation ---------------
        print("\n?? Step 3e: Semantic Validation...")
        validation = validate_report(report)
        report = validation['fixed_report']
        if validation['warnings']:
            for w in validation['warnings']:
                print(f"   ??  {w}")
        if not validation['is_valid']:
            raise Exception(f"Report failed semantic validation: {validation['errors']}")
        print(f"   ? Semantic validation passed ({validation['checks_passed']}/{validation['total_checks']} checks)")

        # -- Step 3c: MAD Protocol (MOVED to mad_runner.py) ----
        # GNI-R-110: MAD runs as separate pipeline (gni_mad.yml)
        # 5 minutes after main pipeline -- clean Groq TPM window
        # mad_runner.py reads this report from Supabase and updates it
        print("\n???? Step 3c: MAD Protocol running separately (gni_mad.yml)")
        print("   GNI-R-110: MAD will run in 5 min with clean Groq TPM window")
        t0 = time.time()
        # Set safe defaults -- mad_runner.py will overwrite these
        report['mad_bull_case']             = ''
        report['mad_bear_case']             = ''
        report['mad_black_swan_case']       = ''
        report['mad_ostrich_case']          = ''
        report['mad_verdict']               = 'pending'
        report['mad_confidence']            = 0.5
        report['mad_blind_spot']            = ''
        report['mad_action_recommendation'] = ''
        report['short_focus_threats']       = ''
        report['long_shoot_threats']        = ''
        report['short_verify_days']         = 14
        report['long_verify_days']          = 180
        report['mad_round1_positions']      = {}
        report['mad_round2_positions']      = {}
        report['mad_round3_positions']      = {}
        report['mad_arb_feedbacks']         = {}
        report['mad_historian_case']        = ''
        report['mad_risk_case']             = ''
        # -- Step 3f: Deception Detection -----------------
        print("\n\U0001f575  Step 3f: Deception Detection...")
        report = enrich_report_with_deception(report, top_articles)

        report['mad_reasoning']  = ''

        # -- Step 3d: Escalation Scoring ------------------
        print("\n?? Step 3d: Scoring Escalation Risk...")
        escalation = score_escalation(top_articles, sentiment=report.get('sentiment'), risk_level=report.get('risk_level'))
        report['escalation_score'] = escalation['escalation_score']
        report['escalation_level'] = escalation['escalation_level']
        report['combo_bonus'] = escalation.get('combo_bonus', 0)
        recommended_interval = get_recommended_interval(escalation['escalation_level'], escalation['escalation_score'])
        log_frequency_decision(escalation['escalation_score'], escalation['escalation_level'], recommended_interval, f"Escalation {escalation['escalation_level']} {escalation['escalation_score']}/10")
        print(f"   ?  Next run recommended in {recommended_interval:.1f}h ({escalation['escalation_level']})")
        hist_context = get_historical_context(escalation['escalation_score'])
        if hist_context:
            report['historical_context'] = hist_context
            print(f"   ?? {hist_context}")
        print(f"   ? Escalation: {escalation['escalation_level']} ({escalation['escalation_score']}/10) ? {escalation['active_pillars']}/3 pillars active")

        # NP-2: Coverage gap detection -- absence is intelligence
        # If CRITICAL escalation but top articles don't cover the escalating region
        # that absence is a signal worth flagging to admin
        if escalation['escalation_level'] == 'CRITICAL':
            geo_signals = escalation.get('signals_found', {}).get('geopolitical', [])
            if geo_signals:
                combined_top = ' '.join([
                    f"{a.get('title','')} {a.get('summary','')}".lower()
                    for a in top_articles
                ])
                covered = [sig for sig in geo_signals if sig in combined_top]
                if not covered:
                    gap_msg = (
                        f"?? [GNI COVERAGE GAP] CRITICAL escalation detected\n"
                        f"Escalation signals: {', '.join(geo_signals[:5])}\n"
                        f"But NONE of these appear in the top {len(top_articles)} selected articles.\n"
                        f"Absence may indicate: source gap, filter bias, or narrative blind spot.\n"
                        f"Time: {datetime.now(timezone.utc).isoformat()}"
                    )
                    print(f"  ?? COVERAGE GAP: CRITICAL escalation signals not in top articles")
                    print(f"     Signals: {geo_signals[:5]}")
                    from notifications.telegram_notifier import send_admin_message
                    try:
                        send_admin_message(gap_msg)
                        print(f"  ?? Coverage gap alert sent to admin")
                    except Exception as _cg_err:
                        print(f"  Warning: Coverage gap alert failed: {str(_cg_err)[:60]}")

        step_timings["mad"] = round(time.time() - t0, 2)
        print("   ? MAD pending -- mad_runner.py will run in 5 minutes")

        # -- Step 4: Save Report
        print("\n?? Step 4: Saving Report to Supabase...")
        t0 = time.time()
        report_id = save_report(report, top_articles,
            quality_score=report.get('quality_score', 0),
            quality_breakdown=report.get('quality_breakdown', {}))
        step_timings["save"] = round(time.time() - t0, 2)

        if report_id:
            reports_saved = 1
            # Predictions saved by mad_runner.py after MAD completes
            # GNI-R-110: mad_runner.py handles prediction saving
            log_audit_event('REPORT_SAVED', {'quality_score': report.get('quality_score', 0), 'sentiment': report.get('sentiment', ''), 'escalation_level': report.get('escalation_level', ''), 'mad_verdict': report.get('mad_verdict', ''), 'deception_level': report.get('deception_level', '')}, report_id=report_id)

        print("\n?? Step 5: Saving Pipeline Run & Article Trace...")
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

        # S27-3: Update gni_stats table with live counters
        try:
            from supabase import create_client as _sc
            _sb2 = _sc(os.getenv('SUPABASE_URL',''), os.getenv('SUPABASE_SERVICE_KEY',''))
            # Read current stats
            _cur = _sb2.table('gni_stats').select('pipeline_runs,articles_analysed,reports_generated').eq('id', 1).execute()
            _row = (_cur.data or [{}])[0]
            _sb2.table('gni_stats').upsert({
                'id': 1,
                'pipeline_runs':     _row.get('pipeline_runs', 0) + 1,
                'articles_analysed': _row.get('articles_analysed', 0) + articles_collected,
                'reports_generated': _row.get('reports_generated', 0) + reports_saved,
                'injection_patterns': len(INJECTION_PATTERNS),
                'updated_at': datetime.now(timezone.utc).isoformat(),
            }).execute()
            print('  OK gni_stats updated')
        except Exception as _se:
            print('  WARNING: gni_stats update failed: ' + str(_se)[:60])

        if run_id and trace:
            save_pipeline_articles(run_id, trace)
            save_article_events(run_id, report_id, trace)

        # -- Step 4b: Three Pillar Reports (GNI-R-097 + GNI-R-098) ----------
        # After Step 5 so run_id is available. sleep(10) prevents Groq 429.
        if report_id and run_id and GITHUB_ACTIONS:
            print("\n?????? Step 4b: Running Three Pillar Reports...")
            _t4b = time.time()
            # GNI-R-097: sleep(120) before first pillar.
            # Step 3 burns ~3 Groq calls (primary analysis + 2 CI runs).
            # MAD moved to separate pipeline (GNI-R-110).
            # Groq free tier rate limit window needs 120s to reset fully.
            print("  Waiting 120s for Groq rate limit to reset after Step 3...")
            time.sleep(120)
            _pillar_buckets = {"geo": [], "tech": [], "fin": []}
            for _art in trace:
                if _art.get("stage4_selected"):
                    _p = _art.get("pillar", "geo").lower()
                    if _p in _pillar_buckets:
                        _pillar_buckets[_p].append(_art)
            for _pillar_idx, _pillar_name in enumerate(["geo", "tech", "fin"]):
                _p_arts = _pillar_buckets[_pillar_name]
                if not _p_arts:
                    print(f"  Warning: No {_pillar_name.upper()} articles -- skipping")
                    continue
                if _pillar_idx > 0:
                    print("  Waiting 45s for Groq rate limit reset between pillars...")
                    time.sleep(45)
                _p_prompt = get_pillar_prompt(_pillar_name)
                _p_report = analyze(_p_arts, prompt_override=_p_prompt, enable_ci=False)
                if _p_report:
                    save_pillar_report(_p_report, _pillar_name, run_id, report_id)
                else:
                    print(f"  Warning: {_pillar_name.upper()} pillar returned no report")
            step_timings["pillar"] = round(time.time() - _t4b, 2)
            print(f"  OK Three Pillar Reports complete ({step_timings['pillar']:.1f}s)")

        # -- Step 5b: Log Groq usage (GNI-R-124) ------------
        if GITHUB_ACTIONS:
            _client = _get_supabase_client() if False else None
            try:
                from supabase import create_client as _create_client
                _sb = _create_client(
                    os.getenv('SUPABASE_URL', ''),
                    os.getenv('SUPABASE_SERVICE_KEY', '')
                )
                _run_tokens, _run_calls = get_run_usage()
                print(f'  Real Groq usage this run: {_run_tokens} tokens across {_run_calls} calls')
                log_usage(_sb, 'gni_pipeline', _run_tokens, _run_calls, run_id or '', account='not_mad')
            except Exception as _e:
                print('  WARNING: Could not log usage: ' + str(_e)[:60])

        # -- Step 6: Telegram Notification ------------------
        if report and report_id:
            notify_report(report, top_articles)

        # -- Step 6b: Article Forensic Trace (XLSX) --
        # Generates full pipeline audit trail and sends to admin Telegram
        # Silent failure -- never breaks the pipeline
        if run_id and trace and GITHUB_ACTIONS:
            try:
                from analysis.gni_forensic_trace import run_forensic_trace_pipeline
                _pipeline_meta = {
                    'run_id':               run_id or '',
                    'articles_collected':   articles_collected,
                    'after_relevance':      total_after_relevance,
                    'after_1b':             len([a for a in trace if a.get('stage1b_passed', True) and a.get('stage1_passed')]),
                    'after_dedup':          total_after_dedup,
                    'articles_after_funnel': articles_after_funnel,
                    'total_seconds':        round((datetime.now(timezone.utc) - run_start).total_seconds(), 2),
                }
                run_forensic_trace_pipeline(trace, run_id, run_at, _pipeline_meta)
            except Exception as _fte:
                print(f'  Warning: Forensic trace failed: {str(_fte)[:60]}')

    except Exception as e:
        status = "failed"
        error_message = str(e)
        print(f"\n? Pipeline error: {e}")

    finally:
        # -- Step 7: Save Runtime Log ------------------------
        total_seconds = round(
            (datetime.now(timezone.utc) - run_start).total_seconds(), 2
        )
        print(f"\n?? Step 7: Saving Runtime Log...")
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
            print("\n?? Post-pipeline: staging regression check...")
            staging = run_staging_checks()
            if staging['failed'] > 0:
                print(f"  ??  Staging check: {staging['failed']} page(s) failed")
            else:
                print(f"  ? Staging check: all {staging['total']} pages OK")


        # -- Phase 1 code fix suggester ---------------
        if GITHUB_ACTIONS:
            print("\n?? Checking for fix suggestions...")
            run_code_fix_suggester()
        return status == "success"


if __name__ == "__main__":
    success = run_pipeline()
    sys.exit(0 if success else 1)



