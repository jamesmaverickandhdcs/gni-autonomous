export const dynamic = 'force-dynamic'
import { createNoStoreClient } from '@/lib/supabaseNoStore'
import { NextRequest, NextResponse } from 'next/server'
import { validateApiKey } from '@/lib/auth'
export async function GET(request: NextRequest) {
  const supabase = createNoStoreClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_KEY!
)
  const authError = validateApiKey(request)
  if (authError) return authError
  try {
    const { data, error } = await supabase
      .from('debate_predictions')
      .select('*')
      // W10: exclude quarantined fossil rows (verified_by='fossil_error_row');
      // null-safe OR -- a bare .neq() would silently drop all NULL verified_by rows
      .or('verified_by.is.null,verified_by.neq.fossil_error_row')
      .order('created_at', { ascending: false })
      .limit(1000)
    if (error) throw error
    // S110 9.5 (F19): the list above is the newest 1000 rows and the table held 1299 non-fossil rows on
    // 2026-10-10, so its length is not a count (R-S106-3). Exact counts under the same filter.
    const fossil = 'verified_by.is.null,verified_by.neq.fossil_error_row'
    const head = () => supabase.from('debate_predictions').select('id', { count: 'exact', head: true }).or(fossil)
    const [all, pend, ver, mat, notm, inc] = await Promise.all([
      head(),
      head().is('verified_at', null),
      head().not('verified_at', 'is', null),
      head().not('verified_at', 'is', null).eq('accurate', true),
      head().not('verified_at', 'is', null).eq('accurate', false),
      head().not('verified_at', 'is', null).is('accurate', null),
    ])
    const counts = [all, pend, ver, mat, notm, inc].some(r => r.error || r.count == null) ? null : {
      total: all.count, pending: pend.count, verified: ver.count, materialized: mat.count,
      not_materialized: notm.count, inconclusive: inc.count,
    }
    return NextResponse.json({ predictions: data || [], counts }, { headers: { 'Cache-Control': 'no-store' } })
  } catch {
    return NextResponse.json({ predictions: [] }, { status: 500 })
  }
}