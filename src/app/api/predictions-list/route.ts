export const dynamic = 'force-dynamic'
import { createClient } from '@supabase/supabase-js'
import { NextRequest, NextResponse } from 'next/server'
import { validateApiKey } from '@/lib/auth'
export async function GET(request: NextRequest) {
  const supabase = createClient(
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
    return NextResponse.json({ predictions: data || [] }, { headers: { 'Cache-Control': 'no-store' } })
  } catch {
    return NextResponse.json({ predictions: [] }, { status: 500 })
  }
}