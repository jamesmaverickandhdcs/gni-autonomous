export const dynamic = 'force-dynamic'
﻿import { createNoStoreClient } from '@/lib/supabaseNoStore'
import { NextRequest, NextResponse } from 'next/server'
import { validateApiKey } from '@/lib/auth'

// I-9 / SRC-INTEGRITY commit 3 — the credibility board must show only LIVE-roster
// sources. Departed sources (Middle East Eye, Bloomberg, Fox News, SCMP, Straits
// Times, The Hindu, Reuters, Stimson) still hold source_credibility rows and were
// TOPPING the board with frozen scores.
//
// The roster lives in Python (rss_collector.SOURCES) and cannot be imported here,
// but main.py already mirrors it into Supabase every run: save_source_counts()
// iterates the full SOURCES list and writes one source_health row per roster
// source per run — including sources that fetched nothing (status 'empty'). So the
// newest run_at batch IS the live roster. Reading it keeps a single source of
// truth; a hand-maintained roster in TS would be the same dual-source-of-truth
// disease this whole workstream exists to kill.
//
// Case-folded on BOTH sides deliberately: source_health carries the collector's
// Title-Case names, while source_credibility holds a mix of Title-Case fossil rows
// and norm() lowercase rows until the dedupe SQL lands (I-4).
const normSource = (s: string) => (s || '').trim().toLowerCase()

export async function GET(request: NextRequest) {
  const supabase = createNoStoreClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_KEY!
)
  const authError = validateApiKey(request)
  if (authError) return authError
  try {
    const [runsRes, reportsRes, weightsRes, credibilityRes, promptsRes, alertsRes, freqRes, escalationRes, rosterRes] = await Promise.all([
      supabase.from('pipeline_runs').select('*').order('run_at', { ascending: false }).limit(5),
      supabase.from('reports').select('quality_score, quality_breakdown, created_at, llm_source').order('created_at', { ascending: false }).limit(10),
      supabase.from('source_weights').select('*').order('weight', { ascending: false }),
      supabase.from('source_credibility').select('*').order('credibility_score', { ascending: false }),
      supabase.from('prompt_variants').select('version, avg_quality_score, run_count, active').order('version'),
      supabase.from('health_alerts').select('*').order('created_at', { ascending: false }).limit(10),
      supabase.from('frequency_log').select('*').order('run_at', { ascending: false }).limit(5),
      supabase.from('reports').select('escalation_score, escalation_score_lower, escalation_score_upper, title, created_at').not('escalation_score', 'is', null).order('created_at', { ascending: false }).limit(1),
      supabase.from('source_health').select('source_name, run_at').order('run_at', { ascending: false }).limit(200),
    ])
    const runs = runsRes.data || []
    const reports = reportsRes.data || []
    const allWeights = weightsRes.data || []
    // Live roster = every source named by the most recent health run. One run's
    // rows all share a single run_at (save_source_counts stamps it once), so the
    // newest batch is a complete roster snapshot, not a partial one.
    const healthRows = rosterRes.data || []
    const latestRunAt = healthRows[0]?.run_at
    const liveRoster = new Set(
      healthRows.filter(r => r.run_at === latestRunAt).map(r => normSource(r.source_name))
    )
    // Fail OPEN: if the roster is unknowable (empty table, query error), serve the
    // board unfiltered rather than blanking it — an empty board renders as "No
    // credibility data yet", which would be a lie about a table that has rows.
    const allCredibility = credibilityRes.data || []
    const credibility = liveRoster.size > 0
      ? allCredibility.filter(r => liveRoster.has(normSource(r.source)))
      : allCredibility
    // HEALTH-W: weights board gets the same live-roster filter as the cred board
    // (C3 sibling). Same fail-open rule: unknowable roster serves unfiltered.
    const weights = liveRoster.size > 0
      ? allWeights.filter(r => liveRoster.has(normSource(r.source)))
      : allWeights
    const prompts = promptsRes.data || []
    const alerts = alertsRes.data || []
    const freqLog = freqRes.data || []
    const latestEscalation = escalationRes.data?.[0] || null
    const lastRun = runs[0] || null
    const validReports = reports.filter(r => r.quality_score > 0)
    const avgQuality = validReports.length > 0
      ? validReports.reduce((sum, r) => sum + (r.quality_score || 0), 0) / validReports.length
      : 0
    return NextResponse.json({
      status: 'ok',
      last_run: lastRun,
      avg_quality_score: Math.round(avgQuality * 100) / 100,
      total_reports: reports.length,
      source_weights: weights,
      source_credibility: credibility,
      prompt_variants: prompts,
      health_alerts: alerts,
      frequency_log: freqLog,
      latest_escalation: latestEscalation,
      recent_quality: reports.map(r => ({
        date: r.created_at,
        score: r.quality_score,
        llm: r.llm_source,
      })),
    })
  } catch {
    return NextResponse.json({ error: 'Failed to fetch health data' }, { status: 500 })
  }
}
