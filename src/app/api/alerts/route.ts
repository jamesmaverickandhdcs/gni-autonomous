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
    const [alerts, usage] = await Promise.all([
      supabase.from('health_alerts').select('*').order('created_at', { ascending: false }).limit(100),
      supabase.from('groq_daily_usage').select('*').order('created_at', { ascending: false }).limit(50),
    ])
    return NextResponse.json(
      { alerts: alerts.data || [], usage: usage.data || [] },
      { headers: { 'Cache-Control': 'no-store' } }
    )
  } catch {
    return NextResponse.json({ alerts: [], usage: [] }, { status: 500 })
  }
}