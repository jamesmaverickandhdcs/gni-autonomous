export const dynamic = 'force-dynamic'
import { NextResponse } from 'next/server'
import { createClient } from '@supabase/supabase-js'


export async function GET() {
  try {
    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''
    )
    // Get last 10 runs per source
    const { data: rows } = await supabase
      .from('source_health')
      .select('source_name, pillar, article_count, run_at, status, alert_sent')
      .order('run_at', { ascending: false })
      .limit(500)

    if (!rows) return NextResponse.json({ sources: [] })

    // Group by source
    const grouped: Record<string, {
      name: string
      pillar: string
      runs: { run_at: string; article_count: number; alert_sent: boolean }[]
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
      const status = current === 0 ? 'down' : current < avg * 0.5 ? 'degraded' : 'healthy'
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
      // Sort: down first, then degraded, then healthy
      const order = { down: 0, degraded: 1, healthy: 2 }
      return (order[a.status as keyof typeof order] ?? 2) - (order[b.status as keyof typeof order] ?? 2)
    })

    return NextResponse.json({ sources })
  } catch (err) {
    console.error('source-health API error:', err)
    return NextResponse.json({ sources: [] })
  }
}
