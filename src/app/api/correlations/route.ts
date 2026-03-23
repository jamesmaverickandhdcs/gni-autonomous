import { NextResponse } from 'next/server'
import { createClient } from '@supabase/supabase-js'

export async function GET() {
  try {
    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''
    )
    const [corr, patterns] = await Promise.all([
      supabase.from('historical_correlations').select('*').order('avg_escalation_score', { ascending: false }),
      supabase.from('correlation_patterns').select('*').order('sample_count', { ascending: false }),
    ])
    return NextResponse.json({ correlations: corr.data || [], patterns: patterns.data || [] })
  } catch {
    return NextResponse.json({ correlations: [], patterns: [] })
  }
}
