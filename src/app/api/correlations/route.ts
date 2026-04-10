export const dynamic = 'force-dynamic'
import { NextRequest, NextResponse } from 'next/server'
import { createClient } from '@supabase/supabase-js'
import { validateApiKey } from '@/lib/auth'

export async function GET(request: NextRequest) {
  const authError = validateApiKey(request)
  if (authError) return authError
  try {
    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''
    )
    const [corr, patterns] = await Promise.all([
      supabase.from('historical_correlations').select('*').order('avg_escalation_score', { ascending: false }),
      supabase.from('correlation_patterns').select('*').order('sample_count', { ascending: false }),
    ])
    // Deduplicate by escalation_level — keep highest sample_count per level
    const seen = new Set<string>()
    const deduped = (corr.data || [])
      .sort((a: {sample_count: number}, b: {sample_count: number}) => (b.sample_count || 0) - (a.sample_count || 0))
      .filter((row: {escalation_level: string}) => {
        if (seen.has(row.escalation_level)) return false
        seen.add(row.escalation_level)
        return true
      })
      .sort((a: {avg_escalation_score: number}, b: {avg_escalation_score: number}) => (b.avg_escalation_score || 0) - (a.avg_escalation_score || 0))
    return NextResponse.json({ correlations: deduped, patterns: patterns.data || [] })
  } catch {
    return NextResponse.json({ correlations: [], patterns: [] })
  }
}
