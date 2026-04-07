export const dynamic = 'force-dynamic'
import { createClient } from '@supabase/supabase-js'
import { NextRequest, NextResponse } from 'next/server'
import { validateApiKey } from '@/lib/auth'
export async function GET(request: NextRequest) {
  const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)
  const authError = validateApiKey(request)
  if (authError) return authError
  try {
    const { data } = await supabase
      .from('audit_trail')
      .select('*')
      .order('created_at', { ascending: false })
      .limit(20)
    return NextResponse.json({ entries: data || [] })
  } catch {
    return NextResponse.json({ entries: [] })
  }
}
