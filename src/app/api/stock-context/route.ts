export const dynamic = 'force-dynamic'
import { NextRequest, NextResponse } from 'next/server'
import { createClient } from '@supabase/supabase-js'
import { z } from 'zod'
import { validateApiKey } from '@/lib/auth'


const contextCache: Record<string, { context: string, date: string }> = {}

const QuerySchema = z.object({
  ticker: z.string().regex(/^[\^A-Z0-9=\-\.]{1,12}$/, { message: 'ticker must be 1-12 chars: uppercase letters, numbers, ^, =, -, .' }).default('SPY'),
  change: z.string().regex(/^-?[0-9]+(\.[0-9]+)?$/, { message: 'change must be a numeric value' }).default('0'),
})

export async function GET(request: NextRequest) {
  const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

  const authError = validateApiKey(request)
  if (authError) return authError
  const { searchParams } = new URL(request.url)

  const parsed = QuerySchema.safeParse({
    ticker: searchParams.get('ticker') ?? undefined,
    change: searchParams.get('change') ?? undefined,
  })
  if (!parsed.success) {
    return NextResponse.json(
      { error: 'Invalid parameters', details: parsed.error.flatten() },
      { status: 400 }
    )
  }

  const { ticker, change: changePercent } = parsed.data
  const today = new Date().toISOString().split('T')[0]

  if (contextCache[ticker] && contextCache[ticker].date === today) {
    return NextResponse.json({ context: contextCache[ticker].context })
  }

  try {
    const { data: reports } = await supabase
      .from('reports')
      .select('title, summary, sentiment, risk_level, location_name, market_impact')
      .order('created_at', { ascending: false })
      .limit(1)

    const report = reports?.[0]
    if (!report) {
      return NextResponse.json({ context: 'No recent GNI report available for context.' })
    }

    const GROQ_API_KEY = process.env.GROQ_API_KEY
    if (!GROQ_API_KEY) {
      return NextResponse.json({ context: 'AI context unavailable.', debug: 'GROQ_API_KEY missing' })
    }

    const prompt = `You are a financial analyst assistant for GNI (Global Nexus Insights).

Latest GNI Intelligence Report:
- Title: ${report.title}
- Summary: ${report.summary}
- Sentiment: ${report.sentiment}
- Risk Level: ${report.risk_level}
- Location: ${report.location_name}
- Market Impact: ${report.market_impact}

The ticker ${ticker} has moved ${changePercent}% in the past 3 days.

In exactly 2 sentences, explain: (1) why ${ticker} moved in this direction based on the geopolitical context above, and (2) what this means for investors watching this instrument. Be specific and connect the geopolitical events to the price movement. Do not use disclaimers or preamble.`

    const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${GROQ_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: process.env.GROQ_MODEL || 'llama-3.3-70b-versatile',
        messages: [{ role: 'user', content: prompt }],
        max_tokens: 150,
        temperature: 0.3,
      })
    })

    const data = await response.json()
    const context = data.choices?.[0]?.message?.content?.trim() || 'AI context unavailable.'
    contextCache[ticker] = { context, date: today }
    return NextResponse.json({ context })

  } catch (err) {
    console.error('Stock context error:', err)
    return NextResponse.json({ context: 'AI context temporarily unavailable.' })
  }
}
