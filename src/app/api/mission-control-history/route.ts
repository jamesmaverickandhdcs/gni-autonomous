export const dynamic = 'force-dynamic'
import { createClient } from '@supabase/supabase-js'
import { NextResponse } from 'next/server'


export async function GET() {
  const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)
  try {
    const { data, error } = await supabase
      .from('mission_control_log')
      .select('id, checked_at, overall_status, issues_found, auto_healed, telegram_sent')
      .order('checked_at', { ascending: false })
      .limit(50)
    if (error) throw error
    return NextResponse.json({ history: data || [] })
  } catch (err) {
    console.error('Self-check history error:', err)
    return NextResponse.json({ error: 'Failed to fetch history' }, { status: 500 })
  }
}
