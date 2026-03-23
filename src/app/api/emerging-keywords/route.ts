import { NextResponse } from 'next/server'
import { createClient } from '@supabase/supabase-js'


export async function GET() {
  try {
    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''
    )
    const { data } = await supabase
      .from('emerging_keywords')
      .select('*')
      .order('frequency_count', { ascending: false })
      .limit(100)
    return NextResponse.json({ keywords: data || [] })
  } catch {
    return NextResponse.json({ keywords: [] })
  }
}
