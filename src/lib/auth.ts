import { NextRequest, NextResponse } from 'next/server'

const VALID_KEYS = (process.env.GNI_API_KEYS || '').split(',').map(k => k.trim()).filter(Boolean)
const INTERNAL_KEY = process.env.SELF_CHECK_INTERNAL_KEY || ''

export function validateApiKey(request: NextRequest): NextResponse | null {
  // Allow internal key (Mission Control / GitHub Actions)
  const internalKey = request.headers.get('X-Internal-Key')
  if (internalKey && internalKey === INTERNAL_KEY) return null

  // Allow same-origin requests (from GNI_Autonomous web pages)
  const origin = request.headers.get('origin') || ''
  const referer = request.headers.get('referer') || ''
  if (
    origin.includes('gni-autonomous.vercel.app') ||
    referer.includes('gni-autonomous.vercel.app')
  ) return null

  // Check X-GNI-Key
  const key = request.headers.get('X-GNI-Key')
  if (!key) {
    return NextResponse.json(
      { error: 'API key required. Add X-GNI-Key header.' },
      { status: 401 }
    )
  }

  if (VALID_KEYS.length > 0 && !VALID_KEYS.includes(key)) {
    return NextResponse.json(
      { error: 'Invalid API key.' },
      { status: 401 }
    )
  }

  return null
}
