export const dynamic = 'force-dynamic'

﻿import { createNoStoreClient } from '@/lib/supabaseNoStore'
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
    const { data: allData, error } = await supabase
      .from('prediction_outcomes')
      .select('*')
      .eq('status', 'measured')
      .order('run_at', { ascending: false })
    const data = (allData || []).slice(0, 50)

    if (error) throw error

    const outcomes = data || []
    const allOutcomes = allData || []
    const total = allOutcomes.length

    const avgScore = total > 0
      ? Math.round(allOutcomes.reduce((s, o) => s + (o.accuracy_score || 0), 0) / total * 100)
      : 0

    const has3d = allOutcomes.filter(o => o.direction_correct_3d !== null)
    const correct3d = has3d.filter(o => o.direction_correct_3d === true).length
    const accuracy3d = has3d.length > 0 ? Math.round(correct3d / has3d.length * 100) : 0

    const has7d = allOutcomes.filter(o => o.direction_correct_7d !== null)
    const correct7d = has7d.filter(o => o.direction_correct_7d === true).length
    const accuracy7d = has7d.length > 0 ? Math.round(correct7d / has7d.length * 100) : 0

    // Build timeline — oldest first for chart
    const timeline = [...outcomes]
      .sort((a, b) => new Date(a.measured_at).getTime() - new Date(b.measured_at).getTime())
      .map(o => ({
        date: o.measured_at?.slice(0, 10),
        accuracy_score: Math.round((o.accuracy_score || 0) * 100),
        sentiment: o.predicted_sentiment || 'Neutral',
        black_swan: o.black_swan_flag || false,
      }))

    return NextResponse.json({
      outcomes,
      timeline,
      summary: {
        total,
        avg_score: avgScore,
        accuracy_3d: accuracy3d,
        accuracy_7d: accuracy7d,
        pending_review: allOutcomes.filter(o => o.human_review_needed).length,
      }
    }, { headers: { 'Cache-Control': 'no-store' } })

  } catch {
    return NextResponse.json({ error: 'Failed to fetch outcomes' }, { status: 500 })
  }
}
