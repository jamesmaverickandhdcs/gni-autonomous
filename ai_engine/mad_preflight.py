# -*- coding: utf-8 -*-
# ============================================================
# GNI MAD Pre-Flight Check -- mad_preflight.py
# Run this BEFORE every manual MAD trigger.
# Prevents rushing into MAD without proper conditions.
#
# Usage:
#   python ai_engine/mad_preflight.py
#
# If all checks pass  → prints GO → safe to run mad_runner.py
# If any check fails  → prints STOP → follow instructions
#
# GNI-R-239: mad_preflight.py MUST be run before any manual
#            MAD trigger. Never skip. Never rush.
# ============================================================

import os
import sys
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

FRESH_WINDOW_MIN  = 35   # report must be younger than this
MIN_GAP_MIN       = 20   # must be 20+ min since Intelligence finished
QUOTA_SAFE        = 70000  # max tokens used before MAD runs

def _get_client():
    from supabase import create_client
    url = os.getenv('SUPABASE_URL', '')
    key = os.getenv('SUPABASE_SERVICE_KEY', '')
    if not url or not key:
        return None
    return create_client(url, key)

def _get_today_usage(client) -> int:
    today = datetime.now(timezone.utc).date().isoformat()
    try:
        result = client.table('groq_daily_usage') \
            .select('tokens_used') \
            .eq('usage_date', today) \
            .execute()
        return sum(row['tokens_used'] for row in (result.data or []))
    except Exception:
        return -1

def run_preflight() -> bool:
    print()
    print('=' * 54)
    print('  GNI MAD Pre-Flight Check')
    print(f'  {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}')
    print('=' * 54)

    checks = []
    instructions = []

    # ── Connect to Supabase ───────────────────────────────────
    client = _get_client()
    if not client:
        print('  ❌ ERROR: Cannot connect to Supabase')
        print('     Check SUPABASE_URL and SUPABASE_SERVICE_KEY in .env')
        return False

    # ── Check 1: Fresh report exists ─────────────────────────
    cutoff = (datetime.now(timezone.utc) - timedelta(minutes=FRESH_WINDOW_MIN)).isoformat()
    try:
        result = client.table('reports') \
            .select('id,title,created_at,mad_verdict') \
            .gte('created_at', cutoff) \
            .order('created_at', desc=True) \
            .limit(1) \
            .execute()

        if not result.data:
            age_result = client.table('reports') \
                .select('created_at,title') \
                .order('created_at', desc=True) \
                .limit(1) \
                .execute()
            if age_result.data:
                last = age_result.data[0]
                age_min = int((datetime.now(timezone.utc) -
                    datetime.fromisoformat(last['created_at'].replace('Z', '+00:00'))
                ).total_seconds() // 60)
                checks.append(('❌', f'No fresh report — latest is {age_min} min old (window={FRESH_WINDOW_MIN}min)'))
                instructions.append(f'→ Run Intelligence Pipeline first, wait 20 min after it finishes')
            else:
                checks.append(('❌', 'No reports found in Supabase at all'))
                instructions.append('→ Run Intelligence Pipeline first')
            fresh_report = None
        else:
            row = result.data[0]
            created = datetime.fromisoformat(row['created_at'].replace('Z', '+00:00'))
            age_min = int((datetime.now(timezone.utc) - created).total_seconds() // 60)
            verdict = row.get('mad_verdict')

            if verdict and verdict != 'pending':
                checks.append(('❌', f'Report already has MAD verdict: {verdict} ({age_min} min old)'))
                instructions.append('→ Run Intelligence Pipeline first to get a new unprocessed report')
                fresh_report = None
            else:
                checks.append(('✅', f'Fresh report found: {age_min} min old | verdict=None'))
                fresh_report = row

    except Exception as e:
        checks.append(('❌', f'Supabase error: {str(e)[:60]}'))
        instructions.append('→ Check Supabase connection')
        fresh_report = None

    # ── Check 2: 20 min gap since Intelligence finished ───────
    try:
        gap_result = client.table('pipeline_runs') \
            .select('created_at,pipeline_type') \
            .eq('pipeline_type', 'gni_pipeline') \
            .order('created_at', desc=True) \
            .limit(1) \
            .execute()

        if gap_result.data:
            last_run = datetime.fromisoformat(
                gap_result.data[0]['created_at'].replace('Z', '+00:00'))
            gap_min = int((datetime.now(timezone.utc) - last_run).total_seconds() // 60)
            if gap_min < MIN_GAP_MIN:
                checks.append(('⚠️ ', f'Intelligence finished {gap_min} min ago (need {MIN_GAP_MIN}+ min)'))
                wait = MIN_GAP_MIN - gap_min
                instructions.append(f'→ Wait {wait} more minutes before triggering MAD')
            else:
                checks.append(('✅', f'Gap since Intelligence: {gap_min} min (>= {MIN_GAP_MIN} min required)'))
        else:
            checks.append(('⚠️ ', 'Cannot verify Intelligence run time — pipeline_runs table empty'))
    except Exception as e:
        checks.append(('⚠️ ', f'Cannot check gap: {str(e)[:60]}'))

    # ── Check 3: Quota sufficient ─────────────────────────────
    tokens_used = _get_today_usage(client)
    if tokens_used == -1:
        checks.append(('⚠️ ', 'Cannot read quota — allowing with caution'))
    elif tokens_used > QUOTA_SAFE:
        checks.append(('❌', f'Quota too high: {tokens_used}/{QUOTA_SAFE} tokens used today'))
        instructions.append('→ Wait for midnight UTC quota reset')
    else:
        headroom = 85000 - tokens_used
        checks.append(('✅', f'Quota OK: {tokens_used} used | {headroom} headroom'))

    # ── Check 4: GROQ_MAD_MODEL set ──────────────────────────
    mad_model = os.getenv('GROQ_MAD_MODEL', '')
    groq_model = os.getenv('GROQ_MODEL', '')
    if mad_model:
        checks.append(('✅', f'GROQ_MAD_MODEL: {mad_model}'))
    elif groq_model:
        checks.append(('⚠️ ', f'GROQ_MAD_MODEL not set — will use GROQ_MODEL: {groq_model}'))
    else:
        checks.append(('❌', 'Neither GROQ_MAD_MODEL nor GROQ_MODEL set in .env'))
        instructions.append('→ Add GROQ_MAD_MODEL=openai/gpt-oss-120b to .env')

    # ── Check 5: Report title preview ────────────────────────
    if fresh_report:
        title = fresh_report.get('title', '')[:60]
        checks.append(('✅', f'Report: "{title}..."'))

    # ── Print Results ─────────────────────────────────────────
    print()
    for icon, msg in checks:
        print(f'  {icon} {msg}')

    # ── Decision ──────────────────────────────────────────────
    failures   = [c for c in checks if c[0] == '❌']
    warnings   = [c for c in checks if c[0] == '⚠️ ']

    print()
    print('=' * 54)

    if failures:
        print('  🛑 STOP — DO NOT RUN MAD')
        print()
        for inst in instructions:
            print(f'  {inst}')
        print('=' * 54)
        print()
        return False
    elif warnings:
        print('  ⚠️  PROCEED WITH CAUTION')
        if instructions:
            for inst in instructions:
                print(f'  {inst}')
        print()
        print('  Run: python ai_engine/mad_runner.py')
        print('=' * 54)
        print()
        return True
    else:
        print('  ✅ ALL CHECKS PASSED — GO!')
        print()
        print('  Run: python ai_engine/mad_runner.py')
        print('=' * 54)
        print()
        return True


if __name__ == '__main__':
    run_preflight()
