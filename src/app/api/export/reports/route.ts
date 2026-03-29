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
  const { searchParams } = new URL(request.url)
  const format = searchParams.get('format') || 'json'
  const days = parseInt(searchParams.get('days') || '30')

  try {
    const safeDays = Math.min(Math.max(days, 1), 90) // cap 1-90 days
    const since = new Date()
    since.setDate(since.getDate() - safeDays)

    const { data, error } = await supabase
      .from('reports')
      .select('id,title,summary,sentiment,sentiment_score,sentiment_score_lower,sentiment_score_upper,confidence_interval_width,analysis_runs,risk_level,escalation_score,escalation_level,mad_verdict,mad_confidence,mad_action_recommendation,tickers_affected,location_name,lat,lng,llm_source,created_at')
      .gte('created_at', since.toISOString())
      .order('created_at', { ascending: false })

    if (error) throw error

    if (format === 'csv') {
      if (!data || data.length === 0) return new NextResponse('No data', { status: 404 })
      const headers = Object.keys(data[0])
      const csv = [
        headers.join(','),
        ...data.map(row => headers.map(h => {
          const val = (row as Record<string, unknown>)[h]
          if (val === null || val === undefined) return ''
          if (Array.isArray(val)) return '"' + val.join(';') + '"'
          const str = String(val)
          return str.includes(',') || str.includes('"') || str.includes('\n')
            ? '"' + str.replace(/"/g, '""') + '"'
            : str
        }).join(','))
      ].join('\n')

      return new NextResponse(csv, {
        headers: {
          'Content-Type': 'text/csv',
          'Content-Disposition': 'attachment; filename="gni_reports_' + days + 'd.csv"',
          'Cache-Control': 'no-store'
        }
      })
    }

    return NextResponse.json({ reports: data, count: data?.length || 0, days }, {
      headers: { 'Cache-Control': 'no-store' }
    })
  } catch (err) {
    console.error('Export reports error:', err)
    return NextResponse.json({ error: 'Export failed' }, { status: 500 })
  }
}
