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
      .from('pillar_reports')
      .select('*')
      .order('created_at', { ascending: false })
      .limit(30)
    if (error) throw error
    return NextResponse.json({ reports: data || [] }, { headers: { 'Cache-Control': 'no-store' } })
  } catch {
    return NextResponse.json({ reports: [] }, { status: 500 })
  }
}