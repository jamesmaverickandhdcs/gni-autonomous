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

  try {
    const { data, error } = await supabase
      .from('debate_predictions')
      .select('*')
      .order('created_at', { ascending: false })

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
          'Content-Disposition': 'attachment; filename="gni_predictions.csv"',
          'Cache-Control': 'no-store'
        }
      })
    }

    return NextResponse.json({ predictions: data, count: data?.length || 0 }, {
      headers: { 'Cache-Control': 'no-store' }
    })
  } catch (err) {
    console.error('Export predictions error:', err)
    return NextResponse.json({ error: 'Export failed' }, { status: 500 })
  }
}
