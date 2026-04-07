export const dynamic = 'force-dynamic'
import { createClient } from '@supabase/supabase-js'
import { NextRequest, NextResponse } from 'next/server'
import { validateApiKey } from '@/lib/auth'


export async function GET(request: NextRequest) {
  const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

  const authError = validateApiKey(request)
  if (authError) return authError
  const { searchParams } = new URL(request.url)
  const days = parseInt(searchParams.get('days') || '7')

  try {
    const since = new Date()
    since.setDate(since.getDate() - days)

    const { data, error } = await supabase
      .from('article_events')
      .select('*')
      .gte('created_at', since.toISOString())
      .not('lat', 'is', null)
      .not('lng', 'is', null)
      .order('created_at', { ascending: false })
      .limit(200)

    if (error) throw error
    return NextResponse.json({ events: data })
  } catch {
    return NextResponse.json({ error: 'Failed to fetch events' }, { status: 500 })
  }
}