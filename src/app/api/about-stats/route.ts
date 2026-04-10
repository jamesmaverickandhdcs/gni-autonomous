import { NextResponse } from 'next/server'

export const dynamic = 'force-dynamic'

export async function GET() {
  try {
    const url = process.env.NEXT_PUBLIC_SUPABASE_URL
    const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
    if (!url || !key) {
      return NextResponse.json({ error: 'Missing env vars' }, { status: 500 })
    }
    const res = await fetch(
      `${url}/rest/v1/gni_stats?id=eq.1&select=pipeline_runs,articles_analysed,reports_generated,updated_at`,
      {
        headers: {
          'apikey': key,
          'Authorization': `Bearer ${key}`,
        },
        cache: 'no-store',
      }
    )
    if (!res.ok) {
      return NextResponse.json({ error: 'Supabase error' }, { status: 500 })
    }
    const data = await res.json()
    if (!data || data.length === 0) {
      return NextResponse.json({
        pipeline_runs: 0,
        articles_analysed: 0,
        reports_generated: 0,
      })
    }
    return NextResponse.json(data[0])
  } catch (e) {
    return NextResponse.json({ error: String(e) }, { status: 500 })
  }
}
