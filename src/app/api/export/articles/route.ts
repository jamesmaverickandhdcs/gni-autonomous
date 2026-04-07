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
  const { searchParams } = new URL(request.url)
  const format = searchParams.get('format') || 'json'
  const runId = searchParams.get('run_id')

  try {
    let query = supabase
      .from('pipeline_articles')
      .select('id,run_id,source,title,url,summary,stage3_score,stage4_rank,stage4_selected,created_at')
      .order('created_at', { ascending: false })
      .limit(200) // safety cap

    if (runId) query = query.eq('run_id', runId)

    const { data, error } = await query
    if (error) throw error

    if (format === 'csv') {
      if (!data || data.length === 0) return new NextResponse('No data', { status: 404 })
      const headers = Object.keys(data[0])
      const csv = [
        headers.join(','),
        ...data.map(row => headers.map(h => {
          const val = (row as Record<string, unknown>)[h]
          if (val === null || val === undefined) return ''
          const str = String(val)
          return str.includes(',') || str.includes('"') || str.includes('\n')
            ? '"' + str.replace(/"/g, '""') + '"'
            : str
        }).join(','))
      ].join('\n')

      return new NextResponse(csv, {
        headers: {
          'Content-Type': 'text/csv',
          'Content-Disposition': 'attachment; filename="gni_articles.csv"',
          'Cache-Control': 'no-store'
        }
      })
    }

    return NextResponse.json({ articles: data, count: data?.length || 0 }, {
      headers: { 'Cache-Control': 'no-store' }
    })
  } catch (err) {
    console.error('Export articles error:', err)
    return NextResponse.json({ error: 'Export failed' }, { status: 500 })
  }
}
