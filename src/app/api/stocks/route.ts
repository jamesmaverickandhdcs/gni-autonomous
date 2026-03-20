import { NextRequest, NextResponse } from 'next/server'
import { z } from 'zod'

const VALID_RANGES = ['3d', '7d', '1m', '1y', '10y'] as const

const QuerySchema = z.object({
  ticker: z.string().regex(/^[A-Z0-9]{1,10}$/, { message: 'ticker must be 1-10 uppercase alphanumeric chars' }).default('SPY'),
  range: z.enum(VALID_RANGES).default('10y'),
})

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)

  const parsed = QuerySchema.safeParse({
    ticker: searchParams.get('ticker') ?? undefined,
    range: searchParams.get('range') ?? undefined,
  })
  if (!parsed.success) {
    return NextResponse.json(
      { error: 'Invalid parameters', details: parsed.error.flatten() },
      { status: 400 }
    )
  }

  const { ticker, range } = parsed.data

  const intervalMap: Record<string, string> = {
    '3d': '5m', '7d': '1h', '1m': '1d', '1y': '1wk', '10y': '1mo',
  }
  const rangeMap: Record<string, string> = {
    '3d': '5d', '7d': '7d', '1m': '1mo', '1y': '1y', '10y': '10y',
  }

  const interval = intervalMap[range]
  const period = rangeMap[range]

  try {
    const url = `https://query1.finance.yahoo.com/v8/finance/chart/${ticker}?interval=${interval}&range=${period}`
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
      },
      next: { revalidate: range === '3d' || range === '7d' ? 300 : 3600 }
    })

    if (!response.ok) throw new Error(`Yahoo Finance returned ${response.status}`)

    const data = await response.json()
    const result = data?.chart?.result?.[0]
    if (!result) throw new Error('No data returned')

    const meta = result.meta
    const timestamps = result.timestamp || []
    const closes = result.indicators?.quote?.[0]?.close || []

    const chartData = timestamps.map((ts: number, i: number) => ({
      date: new Date(ts * 1000).toISOString().split('T')[0],
      close: closes[i] ? Number(closes[i].toFixed(2)) : null,
    })).filter((d: { date: string, close: number | null }) => d.close !== null)

    return NextResponse.json({
      ticker,
      name: meta.longName || meta.shortName || ticker,
      price: meta.regularMarketPrice,
      change: (meta.regularMarketPrice - meta.chartPreviousClose).toFixed(2),
      changePercent: (((meta.regularMarketPrice - meta.chartPreviousClose) / meta.chartPreviousClose) * 100).toFixed(2),
      currency: meta.currency || 'USD',
      chartData,
    })
  } catch (err) {
    console.error('Stock API error:', err)
    return NextResponse.json({ error: 'Failed to fetch stock data' }, { status: 500 })
  }
}
