export const dynamic = 'force-dynamic'
import { createNoStoreClient } from '@/lib/supabaseNoStore'
import { NextRequest, NextResponse } from 'next/server'
import { validateApiKey } from '@/lib/auth'
export async function GET(request: NextRequest) {
  const supabase = createNoStoreClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_KEY!
)
  const authError = validateApiKey(request)
  if (authError) return authError
  try {
    // S106, item 9.22(b): counts come from the RUN table, exactly. The activity log
    // (groq_daily_usage) holds a row only when a run performed an analysis, and its LENGTH
    // was rendered as "Adaptive Runs". Adaptive writes report_id=None on every run row, so
    // "reports written by adaptive" is counted from the run table too, never assumed.
    // The activity rows are fetched 50 per name for display; their COUNT is asked exactly,
    // because the S106 live read showed the page printing '50 entries' for an 85-row log.
    const [adaptive, adaptive2, reports, total, withReport, last, activity] = await Promise.all([
      // Try both column names
      supabase.from('groq_daily_usage').select('*')
        .eq('pipeline', 'gni_adaptive')
        .order('created_at', { ascending: false }).limit(50),
      supabase.from('groq_daily_usage').select('*')
        .eq('pipeline', 'gni-adaptive')
        .order('created_at', { ascending: false }).limit(50),
      supabase.from('reports').select('id,title,escalation_score,escalation_score_raw,escalation_level,created_at')
        .order('created_at', { ascending: false }).limit(20),
      supabase.from('pipeline_runs').select('id', { count: 'exact', head: true })
        .eq('pipeline_type', 'adaptive'),
      supabase.from('pipeline_runs').select('id', { count: 'exact', head: true })
        .eq('pipeline_type', 'adaptive').not('report_id', 'is', null),
      supabase.from('pipeline_runs').select('run_at')
        .eq('pipeline_type', 'adaptive').order('run_at', { ascending: false }).limit(1),
      supabase.from('groq_daily_usage').select('id', { count: 'exact', head: true })
        .in('pipeline', ['gni_adaptive', 'gni-adaptive']),
    ])
    // Combine results from both column name attempts
    const runs = [...(adaptive.data || []), ...(adaptive2.data || [])]
      .sort((a, b) => (a.created_at < b.created_at ? 1 : -1))
    return NextResponse.json(
      { runs, reports: reports.data || [],
        adaptive_total: total.count ?? null,
        activity_total: activity.count ?? null,
        adaptive_reports: withReport.count ?? null,
        last_adaptive_run: last.data && last.data.length > 0 ? last.data[0].run_at : null,
        note: runs.length === 0 ? 'No adaptive runs logged yet -- adaptive pipeline may not have triggered or log_usage() may need pipeline column fix' : null },
      { headers: { 'Cache-Control': 'no-store' } }
    )
  } catch {
    return NextResponse.json({ runs: [], reports: [] }, { status: 500 })
  }
}
