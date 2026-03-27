export const dynamic = 'force-dynamic'
import { createClient } from '@supabase/supabase-js'
import { NextResponse } from 'next/server'
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)
export async function GET() {
  try {
    const [adaptive, reports] = await Promise.all([
      supabase.from('groq_daily_usage').select('*').eq('pipeline', 'gni_adaptive').order('created_at', { ascending: false }).limit(50),
      supabase.from('reports').select('id,title,escalation_score,escalation_level,created_at').eq('pipeline_type', 'gni_adaptive').order('created_at', { ascending: false }).limit(20),
    ])
    return NextResponse.json(
      { runs: adaptive.data || [], reports: reports.data || [] },
      { headers: { 'Cache-Control': 'no-store' } }
    )
  } catch {
    return NextResponse.json({ runs: [], reports: [] }, { status: 500 })
  }
}