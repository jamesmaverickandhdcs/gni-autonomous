import { NextRequest, NextResponse } from 'next/server'

// SEC-3: NEXT_PUBLIC_GNI_API_KEY browser exposure -- monitored, accepted risk (GNI-R-SEC-3)
// Intentionally browser-exposed (Next.js NEXT_PUBLIC_ prefix by design).
// Leaked key grants: READ-ONLY access to public GNI data only.
// Leaked key cannot: write to DB, access Groq/Supabase/Telegram secrets.
// Export endpoints rate-limited 10 req/min (SEC-2). Real secrets are server-side only.


const VALID_KEYS = (process.env.GNI_API_KEYS || '').split(',').map((k: string) => k.trim()).filter(Boolean)
const INTERNAL_KEY = process.env.SELF_CHECK_INTERNAL_KEY || ''

// Rate limiting store -- 200 req/IP/hour for unauthenticated requests (GNI-R-150)
interface RateLimitEntry { count: number; windowStart: number }
const rateLimitStore = new Map<string, RateLimitEntry>()
const RATE_LIMIT_MAX = 200
const RATE_LIMIT_WINDOW_MS = 60 * 60 * 1000

function getClientIp(request: NextRequest): string {
  return (
    request.headers.get('x-forwarded-for')?.split(',')[0]?.trim() ||
    request.headers.get('x-real-ip') ||
    'unknown'
  )
}

function checkRateLimit(ip: string): boolean {
  const now = Date.now()
  const entry = rateLimitStore.get(ip)
  if (!entry || (now - entry.windowStart) > RATE_LIMIT_WINDOW_MS) {
    rateLimitStore.set(ip, { count: 1, windowStart: now })
    return true
  }
  if (entry.count >= RATE_LIMIT_MAX) return false
  entry.count += 1
  return true
}

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
  // Check X-GNI-Key -- authenticated requests exempt from rate limit
  const key = request.headers.get('X-GNI-Key')
  if (key && VALID_KEYS.includes(key)) return null
  // Unauthenticated request -- apply IP rate limit (GNI-R-150)
  const ip = getClientIp(request)
  if (!checkRateLimit(ip)) {
    return NextResponse.json(
      { error: 'Rate limit exceeded. Max 200 requests per hour per IP.' },
      { status: 429 }
    )
  }
  // No key or wrong key -- return 401
  if (!key) {
    return NextResponse.json(
      { error: 'API key required. Add X-GNI-Key header.' },
      { status: 401 }
    )
  }
  return NextResponse.json(
    { error: 'Invalid API key.' },
    { status: 401 }
  )
}
