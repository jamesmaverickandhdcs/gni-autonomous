import { NextRequest, NextResponse } from 'next/server'
import { z } from 'zod'
import { validateApiKey } from '@/lib/auth'

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL || ''
const SUPABASE_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''

const VALID_RANGES = ['3d', '7d', '1m', '1y', '10y'] as const

const QuerySchema = z.object({
  ticker: z.string().regex(/^[\^A-Z0-9=][\^A-Z0-9\-\.=]{0,9}$/, { message: 'ticker must be 1-10 chars' }).default('SPY'),
  range: z.enum(VALID_RANGES).default('1y'),
})

const intervalMap: Record<string, string> = {
  '3d': '5m', '7d': '1h', '1m': '1d', '1y': '1wk', '10y': '1mo',
}
const rangeMap: Record<string, string> = {
  '3d': '5d', '7d': '7d', '1m': '1mo', '1y': '1y', '10y': '10y',
}

export const dynamic = 'force-dynamic'

async function fetchFromSupabase(ticker: string, range: string) {
  // P4 Stock Standby -- read cached prices from Supabase when Yahoo fails
  if (!SUPABASE_URL || !SUPABASE_KEY) return null
  try {
    const url = `${SUPABASE_URL}/rest/v1/stock_prices?ticker=eq.${ticker}&range=eq.${range}&select=*&limit=1`
    const res = await fetch(url, {
      headers: {
        'apikey': SUPABASE_KEY,
        'Authorization': `Bearer ${SUPABASE_KEY}`,
      },
      next: { revalidate: 300 }
    })
    if (!res.ok) return null
    const rows = await res.json()
    if (!rows || rows.length === 0) return null
    const row = rows[0]
    return {
      ticker: row.ticker,
      name: row.name,
      price: row.current_price,
      change: row.day_change?.toFixed(4) ?? '0',
      changePercent: row.day_change_percent?.toFixed(2) ?? '0',
      rangeChange: row.range_change?.toFixed(4) ?? '0',
      rangeChangePercent: row.range_change_percent?.toFixed(2) ?? '0',
      currency: row.currency || 'USD',
      chartData: typeof row.chart_data === 'string' ? JSON.parse(row.chart_data) : row.chart_data,
      cached: true,
      cachedAt: row.fetched_at,
    }
  } catch {
    return null
  }
}

async function fetchYahoo(ticker: string, period: string, interval: string) {
  const url = `https://query1.finance.yahoo.com/v8/finance/chart/${ticker}?interval=${interval}&range=${period}`
  const res = await fetch(url, {
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
      'Accept': 'application/json',
    },
    next: { revalidate: 300 } // 5 min cache for all ranges -- stand-by architecture
  })
  if (!res.ok) throw new Error(`Yahoo Finance returned ${res.status}`)
  const data = await res.json()
  return data?.chart?.result?.[0]
}

export async function GET(request: NextRequest) {

  const authError = validateApiKey(request)
  if (authError) return authError
  const { searchParams } = new URL(request.url)
  const parsed = QuerySchema.safeParse({
    ticker: searchParams.get('ticker') ?? undefined,
    range: searchParams.get('range') ?? undefined,
  })
  if (!parsed.success) {
    return NextResponse.json({ error: 'Invalid parameters' }, { status: 400 })
  }

  const { ticker, range } = parsed.data

  try {
    // Fetch chart data for selected range
    const result = await fetchYahoo(ticker, rangeMap[range], intervalMap[range])
    if (!result) throw new Error('No data returned')

    const meta = result.meta
    const timestamps = result.timestamp || []
    const closes = result.indicators?.quote?.[0]?.close || []

    const chartData = timestamps.map((ts: number, i: number) => ({
      date: new Date(ts * 1000).toISOString().split('T')[0],
      close: closes[i] ? Number(closes[i].toFixed(4)) : null,
    })).filter((d: { date: string; close: number | null }) => d.close !== null)

    // Always fetch 5d for true day change (previousClose = yesterday)
    let dayChange = '0.00'
    let dayChangePercent = '0.00'
    try {
      const dayResult = await fetchYahoo(ticker, '5d', '1d')
      if (dayResult) {
        const dayMeta = dayResult.meta
        const prev = dayMeta.chartPreviousClose || dayMeta.previousClose
        const curr = dayMeta.regularMarketPrice
        if (prev && curr) {
          dayChange = (curr - prev).toFixed(4)
          dayChangePercent = (((curr - prev) / prev) * 100).toFixed(2)
        }
      }
    } catch {
      // fallback: use 7d cache change
      dayChange = (meta.regularMarketPrice - meta.chartPreviousClose).toFixed(4)
      dayChangePercent = (((meta.regularMarketPrice - meta.chartPreviousClose) / meta.chartPreviousClose) * 100).toFixed(2)
    }

    // Range change (start of range to now)
    const firstClose = chartData.length > 0 ? chartData[0].close : null
    const lastPrice = meta.regularMarketPrice
    const rangeChange = firstClose ? (lastPrice - firstClose).toFixed(4) : '0'
    const rangeChangePercent = firstClose ? (((lastPrice - firstClose) / firstClose) * 100).toFixed(2) : '0'

    return NextResponse.json({
      ticker,
      name: meta.longName || meta.shortName || ticker,
      price: meta.regularMarketPrice,
      // Day change (always vs yesterday -- for listing table)
      change: dayChange,
      changePercent: dayChangePercent,
      // Range change (vs start of selected range -- for chart label)
      rangeChange,
      rangeChangePercent,
      currency: meta.currency || 'USD',
      chartData,
    }, { headers: { 'Cache-Control': 'no-store' } })

  } catch (err) {
    console.error('Stock API error -- trying Supabase standby:', err)
    // P4 Stock Standby -- fallback to cached Supabase data
    const cached = await fetchFromSupabase(ticker, range)
    if (cached) {
      console.log(`Stock API: serving cached data for ${ticker} ${range}`)
      return NextResponse.json(cached, { headers: { 'Cache-Control': 'no-store' } })
    }
    return NextResponse.json({ error: 'Failed to fetch stock data' }, { status: 500 })
  }
}
