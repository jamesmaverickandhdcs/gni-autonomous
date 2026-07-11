export const dynamic = 'force-dynamic'
import { NextRequest, NextResponse } from 'next/server'
import { createNoStoreClient } from '@/lib/supabaseNoStore'
import { validateApiKey } from '@/lib/auth'


export async function GET(request: NextRequest) {
  const authError = validateApiKey(request)
  if (authError) return authError
  try {
    const supabase = createNoStoreClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''
    )
    // Get last 10 runs per source
    const { data: rows } = await supabase
      .from('source_health')
      .select('source_name, pillar, article_count, raw_count, fetch_ok, served_by, run_at, status, alert_sent')
      .order('run_at', { ascending: false })
      .limit(500)

    if (!rows) return NextResponse.json({ sources: [] })

    // Group by source
    const grouped: Record<string, {
      name: string
      pillar: string
      runs: {
        run_at: string
        article_count: number
        raw_count: number | null
        fetch_ok: boolean | null
        served_by: string | null
        alert_sent: boolean
      }[]
    }> = {}

    for (const row of rows) {
      if (!grouped[row.source_name]) {
        grouped[row.source_name] = {
          name: row.source_name,
          pillar: row.pillar,
          runs: [],
        }
      }
      if (grouped[row.source_name].runs.length < 10) {
        grouped[row.source_name].runs.push({
          run_at: row.run_at,
          article_count: row.article_count,
          raw_count: row.raw_count ?? null,
          fetch_ok: row.fetch_ok ?? null,
          served_by: row.served_by ?? null,
          alert_sent: row.alert_sent || false,
        })
      }
    }

    // Calculate stats per source
    const sources = Object.values(grouped).map(src => {
      const counts = src.runs.map(r => r.article_count)
      const current = counts[0] ?? 0
      const avg = counts.length > 1
        ? Math.round(counts.slice(1).reduce((a, b) => a + b, 0) / (counts.length - 1))
        : current
      const everFailed = src.runs.some(r => r.alert_sent)

      // Status is derived from the latest run only. article_count is post-gate
      // yield, so it cannot distinguish a dead feed from one whose entries the
      // gate ate; raw_count/fetch_ok/served_by carry the transport truth.
      const latest = src.runs[0]
      const rawCount = latest?.raw_count ?? 0
      const fetchOk = latest?.fetch_ok
      let status: string
      if (latest?.served_by != null) {
        // A reserve served this slot: fetch_ok/raw_count describe the reserve,
        // not the primary, so they must not be read as the primary's health.
        status = 'reserve-masked'
      } else if (fetchOk === false) {
        status = 'transport-down'
      } else if (fetchOk === true) {
        if (rawCount === 0) status = 'silent'
        else if (current === 0) status = 'stale-gated'
        else status = 'healthy'
      } else {
        // Legacy row written before fetch_ok/served_by existed.
        status = current === 0 ? 'down' : current < avg * 0.5 ? 'degraded' : 'healthy'
      }

      return {
        name: src.name,
        pillar: src.pillar,
        current,
        avg,
        status,
        everFailed,
        runs: src.runs,
        lastSeen: src.runs[0]?.run_at || '',
      }
    }).sort((a, b) => {
      // Sort: most actionable failures first, healthy last
      const order = {
        'transport-down': 0,
        'reserve-masked': 1,
        'silent': 2,
        'stale-gated': 3,
        'down': 4,
        'degraded': 5,
        'healthy': 6,
      }
      return (order[a.status as keyof typeof order] ?? 6) - (order[b.status as keyof typeof order] ?? 6)
    })

    return NextResponse.json({ sources })
  } catch (err) {
    console.error('source-health API error:', err)
    return NextResponse.json({ sources: [] })
  }
}
