export const dynamic = 'force-dynamic'
import { NextRequest, NextResponse } from 'next/server'
import { validateApiKey } from '@/lib/auth'

export async function GET(request: NextRequest) {
  const authError = validateApiKey(request)
  if (authError) return authError

  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || ''
  const supabaseKey = process.env.SUPABASE_SERVICE_KEY || ''
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
      // S106: the RANK is by raw magnitude. The capped score sat at 10.0 on 262 of 263 runs, so
      // ranking by it put every run at 'top 0%'. Runs written before S90 carry no raw value and
      // are not ranked; with no raw value on the latest report, no rank is published.
      // total_non_zero keeps its pre-S106 meaning (reports with a non-zero capped score):
      // /developer-hub reads it as its report count.
      const [cappedRes, rawRes] = await Promise.all([
        fetch(supabaseUrl + '/rest/v1/reports?select=escalation_score&escalation_score=gt.0',
              { headers, cache: 'no-store' }),
        fetch(supabaseUrl + '/rest/v1/reports?select=escalation_score_raw&escalation_score_raw=not.is.null',
              { headers, cache: 'no-store' }),
      ])
      const capped = await cappedRes.json()
      const raws = await rawRes.json()
      const latestRaw = data[0].escalation_score_raw
      const totalNonZero = Array.isArray(capped) ? capped.length : 0
      if (latestRaw != null && Array.isArray(raws) && raws.length > 0) {
        const below = raws.filter((r: { escalation_score_raw: number }) => r.escalation_score_raw <= latestRaw).length
        baseline = { score: latestRaw, percentile: Math.round((below / raws.length) * 100),
                     raw_total: raws.length, total_non_zero: totalNonZero }
      } else if (totalNonZero > 0) {
        baseline = { score: 0, percentile: 0, raw_total: 0, total_non_zero: totalNonZero }
      }
    }

    // S106, item 9.22(b) kin: the home page rendered the LENGTH of this limit=10 query as its
    // report count. The exact count comes from the database, not from the page.
    // A failed count leaves total null (the page shows a dash); it never fails the reports.
    let total: number | null = null
    try {
      const countRes = await fetch(supabaseUrl + '/rest/v1/reports?select=id',
        { method: 'HEAD', headers: { ...headers, Prefer: 'count=exact' }, cache: 'no-store' })
      const range = countRes.headers.get('content-range')
      if (range && range.includes('/')) {
        const n = parseInt(range.split('/')[1], 10)
        total = Number.isFinite(n) ? n : null
      }
    } catch { total = null }
    return NextResponse.json({ reports: data, baseline, total }, { headers: { 'Cache-Control': 'no-store' } })
  } catch {
    return NextResponse.json({ error: 'Failed to fetch reports' }, { status: 500 })
  }
}