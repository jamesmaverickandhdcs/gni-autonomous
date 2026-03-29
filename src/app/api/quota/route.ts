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
  try {
    const { data, error } = await supabase
      .from('groq_daily_usage')
      .select('pipeline, tokens_used, requests_used, created_at')
      .order('created_at', { ascending: false })
      .limit(200)
    if (error) throw error
    return NextResponse.json({ usage: data || [] }, { headers: { 'Cache-Control': 'no-store' } })
  } catch {
    return NextResponse.json({ usage: [] }, { status: 500 })
  }
}