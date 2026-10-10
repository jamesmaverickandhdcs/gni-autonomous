export const dynamic = 'force-dynamic'
import { NextRequest, NextResponse } from 'next/server'
import { createNoStoreClient } from '@/lib/supabaseNoStore'
import { validateApiKey } from '@/lib/auth'

export async function GET(request: NextRequest) {
  const authError = validateApiKey(request)
  if (authError) return authError
  try {
    const supabase = createNoStoreClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''
    )
    const [corr, patterns] = await Promise.all([
      supabase.from('historical_correlations').select('*').order('avg_escalation_score', { ascending: false }),
      supabase.from('correlation_patterns').select('*').order('sample_count', { ascending: false }),
    ])
    // S110 9.5 (F18): the writer appends one row per level at every refresh (no unique key),
    // so this table holds every snapshot since March. Show the LATEST refresh only - the rows
    // sharing the newest last_updated. Keeping the largest row per level mixed snapshots months
    // apart, and the header summed outcomes no longer stored (422 shown, 271 in the table).
    type Row = { last_updated: string; avg_escalation_score: number }
    const rows: Row[] = corr.data || []
    const latest = rows.reduce((m, r) => (r.last_updated > m ? r.last_updated : m), '')
    const snapshot = rows
      .filter(r => r.last_updated === latest)
      .sort((a, b) => (b.avg_escalation_score || 0) - (a.avg_escalation_score || 0))
    return NextResponse.json({ correlations: snapshot, snapshot_at: latest || null, patterns: patterns.data || [] })
  } catch {
    return NextResponse.json({ correlations: [], patterns: [] })
  }
}
