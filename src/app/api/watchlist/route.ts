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
  try {
    const { data, error } = await supabase
      .from('watchlist')
      .select('*')
      .order('ticker', { ascending: true })
    if (error) throw error
    return NextResponse.json({ watchlist: data || [] })
  } catch (err) {
    console.error('Watchlist error:', err)
    return NextResponse.json({ error: 'Failed to fetch watchlist' }, { status: 500 })
  }
}
