export const dynamic = 'force-dynamic'

import { createClient } from '@supabase/supabase-js'
import { NextRequest, NextResponse } from 'next/server'
import { z } from 'zod'
import { validateApiKey } from '@/lib/auth'


const QuerySchema = z.object({
  run_id: z.string().uuid({ message: 'run_id must be a valid UUID' }),
})

export async function GET(request: NextRequest) {
  const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

  const authError = validateApiKey(request)
  if (authError) return authError
  const { searchParams } = new URL(request.url)

  const parsed = QuerySchema.safeParse({ run_id: searchParams.get('run_id') })
  if (!parsed.success) {
    return NextResponse.json(
      { error: 'Invalid parameters', details: parsed.error.flatten() },
      { status: 400 }
    )
  }

  const { run_id } = parsed.data

  try {
    const { data, error } = await supabase
      .from('pipeline_articles')
      .select('*')
      .eq('run_id', run_id)
      .order('stage3_score', { ascending: false })
    if (error) throw error
    return NextResponse.json({ articles: data }, { headers: { 'Cache-Control': 'no-store' } })
  } catch {
    return NextResponse.json({ error: 'Failed to fetch articles' }, { status: 500 })
  }
}
