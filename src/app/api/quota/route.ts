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
      .from('groq_daily_usage')
      .select('pipeline, tokens_used, requests_used, created_at, account')   // S48: account-aware quota
      .order('created_at', { ascending: false })
      .limit(500)
    if (error) throw error
    // S48: per-account token sums for TODAY (UTC). ADDITIVE -- `usage` unchanged for existing consumers.
    const usage = data || []
    const today = new Date().toISOString().split('T')[0]
    const byAccountToday: Record<string, number> = {}
    let todayTokens = 0
    for (const u of usage as Array<{ created_at?: string; account?: string; tokens_used?: number }>) {
      if (typeof u.created_at === 'string' && u.created_at.startsWith(today)) {
        const acct = u.account || 'unknown'
        byAccountToday[acct] = (byAccountToday[acct] || 0) + (u.tokens_used || 0)
        todayTokens += (u.tokens_used || 0)
      }
    }
    return NextResponse.json(
      {
        usage,
        by_account_today: byAccountToday,
        daily_limit: 100000,
        today_tokens: todayTokens,
        used_today: todayTokens,
        hard_limit: 100000,
        safe_ceiling: 85000,
      },
      { headers: { 'Cache-Control': 'no-store' } }
    )
  } catch {
    return NextResponse.json({ usage: [] }, { status: 500 })
  }
}