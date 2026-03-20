import { createClient } from '@supabase/supabase-js'
import { NextResponse } from 'next/server'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

export async function GET() {
  try {
    const [runsRes, reportsRes, weightsRes] = await Promise.all([
      supabase.from('pipeline_runs').select('*').order('run_at', { ascending: false }).limit(5),
      supabase.from('reports').select('quality_score, quality_breakdown, created_at, llm_source').order('created_at', { ascending: false }).limit(10),
      supabase.from('source_weights').select('*').order('weight', { ascending: false }),
    ])

    const runs = runsRes.data || []
    const reports = reportsRes.data || []
    const weights = weightsRes.data || []

    const lastRun = runs[0] || null
    const avgQuality = reports.length > 0
      ? reports.reduce((sum, r) => sum + (r.quality_score || 0), 0) / reports.length
      : 0

    return NextResponse.json({
      status: 'ok',
      last_run: lastRun,
      avg_quality_score: Math.round(avgQuality * 100) / 100,
      total_reports: reports.length,
      source_weights: weights,
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
