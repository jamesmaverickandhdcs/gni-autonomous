export const dynamic = 'force-dynamic'
import { createClient } from '@supabase/supabase-js'
import { NextRequest, NextResponse } from 'next/server'
import { validateApiKey } from '@/lib/auth'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

export async function GET(request: NextRequest) {
  const authError = validateApiKey(request)
  if (authError) return authError
  try {
    // Last report time
    const { data: reports } = await supabase
      .from('reports')
      .select('created_at,escalation_level')
      .order('created_at', { ascending: false })
      .limit(1)
    const lastReport = reports?.[0] || null

    // Source health
    const { data: sources } = await supabase
      .from('source_health')
      .select('status')
    const healthy = sources?.filter((s: { status: string }) => s.status === 'healthy').length || 0
    const degraded = sources?.filter((s: { status: string }) => s.status === 'degraded').length || 0
    const down = sources?.filter((s: { status: string }) => s.status === 'down').length || 0

    // Quota today
    const { data: quota } = await supabase
      .from('groq_daily_usage')
      .select('tokens_used')
      .order('created_at', { ascending: false })
      .limit(10)
    const tokensToday = quota?.reduce((s: number, r: { tokens_used: number }) => s + (r.tokens_used || 0), 0) || 0

    // Pipeline last runs
    const { data: pipelines } = await supabase
      .from('groq_daily_usage')
      .select('pipeline_type,created_at,tokens_used')
      .order('created_at', { ascending: false })
      .limit(20)

    const pipelineStatus: Record<string, string> = {}
    const seen = new Set()
    for (const p of (pipelines || [])) {
      if (!seen.has(p.pipeline_type)) {
        seen.add(p.pipeline_type)
        pipelineStatus[p.pipeline_type] = p.created_at
      }
    }

    const minutesSinceReport = lastReport
      ? Math.round((Date.now() - new Date(lastReport.created_at).getTime()) / 60000)
      : null

    return NextResponse.json({
      status: 'ok',
      autonomy_level: 'L7',
      self_healing: 'L3.5',
      monthly_cost: '$0.00',
      last_report: {
        at: lastReport?.created_at || null,
        minutes_ago: minutesSinceReport,
        escalation_level: lastReport?.escalation_level || null
      },
      pipelines: pipelineStatus,
      sources: { healthy, degraded, down, total: (sources?.length || 0) },
      quota: {
        tokens_used_today: tokensToday,
        safe_ceiling: 85000,
        hard_limit: 100000,
        percent_used: Math.round((tokensToday / 100000) * 100),
        status: tokensToday < 85000 ? 'safe' : tokensToday < 100000 ? 'warning' : 'critical'
      },
      checked_at: new Date().toISOString()
    }, { headers: { 'Cache-Control': 'no-store' } })
  } catch {
    return NextResponse.json({ error: 'Failed to fetch status' }, { status: 500 })
  }
}
