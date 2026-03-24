import { NextResponse } from 'next/server'
import { createClient } from '@supabase/supabase-js'

export async function GET() {
  try {
    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''
    )
    const { data: logs } = await supabase
      .from('keyword_security_log')
      .select('*')
      .order('created_at', { ascending: false })
      .limit(100)
    const { data: keywords } = await supabase
      .from('emerging_keywords')
      .select('*')
      .order('frequency_count', { ascending: false })
      .limit(50)
    const logData = logs || []
    const stats = {
      total_processed: logData.length,
      layer1_blocked: logData.filter((l: Record<string, unknown>) => !l.layer1_passed).length,
      layer2_blocked: logData.filter((l: Record<string, unknown>) => l.layer1_passed && !l.layer2_passed).length,
      layer4_blocked: logData.filter((l: Record<string, unknown>) => l.layer2_passed && !l.layer4_passed).length,
      layer6_blocked: logData.filter((l: Record<string, unknown>) => l.layer4_passed && !l.layer6_passed).length,
      security_veto: logData.filter((l: Record<string, unknown>) => l.security_veto).length,
      auto_rejected: logData.filter((l: Record<string, unknown>) => l.final_decision === 'AUTO_REJECT').length,
      recommended: logData.filter((l: Record<string, unknown>) => l.final_decision === 'RECOMMEND').length,
      vote_3_0: logData.filter((l: Record<string, unknown>) => l.vote_result === '3-0').length,
      vote_2_1: logData.filter((l: Record<string, unknown>) => l.vote_result === '2-1').length,
      vote_1_2: logData.filter((l: Record<string, unknown>) => l.vote_result === '1-2').length,
      vote_0_3: logData.filter((l: Record<string, unknown>) => l.vote_result === '0-3').length,
    }
    return NextResponse.json({ logs: logData, keywords: keywords || [], stats })
  } catch (e) {
    console.error('keyword-intelligence API error:', e)
    return NextResponse.json({ logs: [], keywords: [], stats: {} })
  }
}
