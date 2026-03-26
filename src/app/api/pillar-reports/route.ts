import { NextResponse } from 'next/server'
import { createClient } from '@supabase/supabase-js'

export async function GET() {
  try {
    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''
    )
    const { data, error } = await supabase
      .from('pillar_reports')
      .select('*')
      .order('created_at', { ascending: false })
      .limit(9)
    if (error) throw error
    return NextResponse.json({ reports: data || [] }, { headers: { 'Cache-Control': 'no-store' } })
  } catch (e) {
    console.error('pillar-reports API error:', e)
    return NextResponse.json({ reports: [] }, { headers: { 'Cache-Control': 'no-store' } })
  }
}
