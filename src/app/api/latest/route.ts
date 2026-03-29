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
    // Latest report
    const { data: reports } = await supabase
      .from('reports')
      .select('id,title,summary,sentiment,sentiment_score,escalation_score,escalation_level,mad_verdict,mad_confidence,mad_action_recommendation,mad_blind_spot,tickers_affected,risk_level,created_at')
      .order('created_at', { ascending: false })
      .limit(1)
    const latest = reports?.[0] || null

    // Pillar reports
    const { data: pillars } = await supabase
      .from('pillar_reports')
      .select('pillar,title,sentiment,risk_level,sentiment_score')
      .order('created_at', { ascending: false })
      .limit(3)

    // Quota
    const { data: quota } = await supabase
      .from('groq_daily_usage')
      .select('tokens_used,pipeline_type,created_at')
      .order('created_at', { ascending: false })
      .limit(10)

    const tokensToday = quota?.reduce((s: number, r: { tokens_used: number }) => s + (r.tokens_used || 0), 0) || 0

    return NextResponse.json({
      gni_state: {
        report: latest,
        pillars: pillars || [],
        quota: {
          tokens_used_today: tokensToday,
          hard_limit: 100000,
          safe_ceiling: 85000,
          percent_used: Math.round((tokensToday / 100000) * 100)
        },
        generated_at: new Date().toISOString()
      }
    }, { headers: { 'Cache-Control': 'no-store' } })
  } catch {
    return NextResponse.json({ error: 'Failed to fetch GNI state' }, { status: 500 })
  }
}
