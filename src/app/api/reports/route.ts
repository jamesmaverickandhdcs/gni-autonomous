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
    const { data, error } = await supabase
      .from('reports')
      .select('*')
      .order('created_at', { ascending: false })
      .limit(10)

    if (error) throw error

    // Historical baseline: today's escalation score percentile
    let baseline = null
    if (data && data.length > 0) {
      const latestScore = data[0].escalation_score || 0
      const { data: allScores } = await supabase
        .from('reports')
        .select('escalation_score')
        .gt('escalation_score', 0)
      if (allScores && allScores.length > 0) {
        const total = allScores.length
        const below = allScores.filter((r: { escalation_score: number }) => r.escalation_score <= latestScore).length
        const percentile = Math.round((below / total) * 100)
        baseline = { score: latestScore, percentile, total_non_zero: total }
      }
    }
    return NextResponse.json({ reports: data, baseline }, { headers: { 'Cache-Control': 'no-store' } })
  } catch {
    return NextResponse.json(
      { error: 'Failed to fetch reports' },
      { status: 500 }
    )
  }
}