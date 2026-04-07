export const dynamic = 'force-dynamic'
import { NextRequest, NextResponse } from 'next/server'
import { validateApiKey } from '@/lib/auth'

export async function GET(request: NextRequest) {
  const authError = validateApiKey(request)
  if (authError) return authError

  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || ''
  const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''
  const headers = {
    apikey: supabaseKey,
    Authorization: 'Bearer ' + supabaseKey,
    Accept: 'application/json'
  }

  try {
    const res = await fetch(
      supabaseUrl + '/rest/v1/reports?select=*&order=created_at.desc&limit=10',
      { headers, cache: 'no-store' }
    )
    const data = await res.json()

    let baseline = null
    if (data && data.length > 0) {
      const latestScore = data[0].escalation_score || 0
      const scoresRes = await fetch(
        supabaseUrl + '/rest/v1/reports?select=escalation_score&escalation_score=gt.0',
        { headers, cache: 'no-store' }
      )
      const allScores = await scoresRes.json()
      if (allScores && allScores.length > 0) {
        const total = allScores.length
        const below = allScores.filter((r: { escalation_score: number }) => r.escalation_score <= latestScore).length
        const percentile = Math.round((below / total) * 100)
        baseline = { score: latestScore, percentile, total_non_zero: total }
      }
    }

    return NextResponse.json({ reports: data, baseline }, { headers: { 'Cache-Control': 'no-store' } })
  } catch {
    return NextResponse.json({ error: 'Failed to fetch reports' }, { status: 500 })
  }
}