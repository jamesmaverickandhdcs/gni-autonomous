export const dynamic = 'force-dynamic'
import { createClient } from '@supabase/supabase-js'
import { NextResponse } from 'next/server'
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)
export async function GET() {
  try {
    const [adaptive, adaptive2, reports] = await Promise.all([
      // Try both column names
      supabase.from('groq_daily_usage').select('*')
        .eq('pipeline', 'gni_adaptive')
        .order('created_at', { ascending: false }).limit(50),
      supabase.from('groq_daily_usage').select('*')
        .eq('pipeline', 'gni-adaptive')
        .order('created_at', { ascending: false }).limit(50),
      supabase.from('reports').select('id,title,escalation_score,escalation_level,created_at,pipeline_type')
        .eq('pipeline_type', 'gni_adaptive')
        .order('created_at', { ascending: false }).limit(20),
    ])
    // Combine results from both column name attempts
    const runs = [...(adaptive.data || []), ...(adaptive2.data || [])]
    return NextResponse.json(
      { runs, reports: reports.data || [], note: runs.length === 0 ? 'No adaptive runs logged yet -- adaptive pipeline may not have triggered or log_usage() may need pipeline column fix' : null },
      { headers: { 'Cache-Control': 'no-store' } }
    )
  } catch {
    return NextResponse.json({ runs: [], reports: [] }, { status: 500 })
  }
}
