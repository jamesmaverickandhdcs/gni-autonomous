import { createClient } from '@supabase/supabase-js'
import { NextResponse } from 'next/server'
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)
export async function GET() {
  try {
    const [runsRes, reportsRes, weightsRes, credibilityRes, promptsRes, alertsRes, freqRes, escalationRes] = await Promise.all([
      supabase.from('pipeline_runs').select('*').order('run_at', { ascending: false }).limit(5),
      supabase.from('reports').select('quality_score, quality_breakdown, created_at, llm_source').order('created_at', { ascending: false }).limit(10),
      supabase.from('source_weights').select('*').order('weight', { ascending: false }),
      supabase.from('source_credibility').select('*').order('credibility_score', { ascending: false }),
      supabase.from('prompt_variants').select('version, avg_quality_score, run_count, active').order('version'),
      supabase.from('health_alerts').select('*').order('created_at', { ascending: false }).limit(10),
      supabase.from('frequency_log').select('*').order('run_at', { ascending: false }).limit(5),
      supabase.from('reports').select('escalation_score, escalation_score_lower, escalation_score_upper, title, created_at').not('escalation_score', 'is', null).order('created_at', { ascending: false }).limit(1),
    ])
    const runs = runsRes.data || []
    const reports = reportsRes.data || []
    const weights = weightsRes.data || []
    const credibility = credibilityRes.data || []
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
