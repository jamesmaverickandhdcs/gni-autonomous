export const dynamic = 'force-dynamic'
import { createClient } from '@supabase/supabase-js'
import { NextRequest, NextResponse } from 'next/server'

// ============================================================
// GNI Telegram Webhook — S21-5
// Receives admin replies for reserve source selection.
// Admin replies 1-5 to activate a reserve source.
// Security: verifies X-Telegram-Bot-Api-Secret-Token header.
// ============================================================

const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_KEY!
)

const WEBHOOK_SECRET    = process.env.TELEGRAM_WEBHOOK_SECRET || ''
const BOT_TOKEN         = process.env.TELEGRAM_BOT_TOKEN || ''
const ADMIN_ID          = process.env.TELEGRAM_ADMIN_ID || ''

// Reserve sources — must match source_health_monitor.py exactly
const GEO_RESERVES = [
  { name: 'Global Voices',     url: 'https://globalvoices.org/feed/',                         pillar: 'geo', democracy_score: 88 },
  { name: 'The Independent',   url: 'https://www.independent.co.uk/news/world/rss',           pillar: 'geo', democracy_score: 82 },
  { name: 'Radio Free Europe', url: 'https://www.rferl.org/api/epiqq',                        pillar: 'geo', democracy_score: 85 },
  { name: 'New York Times',    url: 'https://rss.nytimes.com/services/xml/rss/nyt/World.xml', pillar: 'geo', democracy_score: 81 },
  { name: 'Washington Post',   url: 'https://feeds.washingtonpost.com/rss/world',             pillar: 'geo', democracy_score: 79 },
]

const FIN_RESERVES = [
  { name: 'Wall Street Journal', url: 'https://feeds.a.dj.com/rss/RSSWorldNews.xml', pillar: 'fin', democracy_score: 76 },
  { name: 'Newsweek',            url: 'https://www.newsweek.com/rss',                pillar: 'fin', democracy_score: 68 },
]

const TECH_RESERVES = [
  { name: 'The Verge',    url: 'https://www.theverge.com/rss/index.xml', pillar: 'tech', democracy_score: 63 },
  { name: 'Dark Reading', url: 'https://www.darkreading.com/rss.xml',    pillar: 'tech', democracy_score: 75 },
]

function getReservesForPillar(pillar: string) {
  if (pillar === 'geo')  return GEO_RESERVES
  if (pillar === 'fin')  return FIN_RESERVES
  if (pillar === 'tech') return TECH_RESERVES
  return GEO_RESERVES
}

async function sendAdminMessage(text: string): Promise<void> {
  if (!BOT_TOKEN || !ADMIN_ID) return
  try {
    await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: ADMIN_ID,
        text,
        parse_mode: 'HTML',
      }),
    })
  } catch {
    // Silent — webhook response already sent
  }
}

async function processReserveChoice(choice: number): Promise<string> {
  // Find most recent pending/alerted reserve record
  const { data: pending, error } = await supabase
    .from('source_reserves')
    .select('id, primary_source')
    .in('status', ['pending', 'alerted'])
    .order('last_alerted_at', { ascending: false })
    .limit(1)

  if (error || !pending || pending.length === 0) {
    return '⚠️ No pending reserve selection found. Source may already be resolved.'
  }

  const record      = pending[0]
  const recordId    = record.id
  const primary     = record.primary_source

  // Find pillar for this primary source
  // We store pillar in source_reserves — fetch it
  const { data: fullRecord } = await supabase
    .from('source_reserves')
    .select('pillar')
    .eq('id', recordId)
    .single()

  const pillar   = fullRecord?.pillar || 'geo'
  const reserves = getReservesForPillar(pillar)

  if (choice < 1 || choice > reserves.length) {
    return `❌ Invalid choice: ${choice}. Please reply with 1-${reserves.length}.`
  }

  const selected = reserves[choice - 1]
  const now      = new Date().toISOString()

  // Activate reserve in Supabase
  const { error: updateError } = await supabase
    .from('source_reserves')
    .update({
      reserve_source: selected.name,
      status:         'active',
      activated_at:   now,
    })
    .eq('id', recordId)

  if (updateError) {
    return '❌ Failed to activate reserve. Please try again.'
  }

  return (
    `✅ <b>Reserve activated!</b>\n` +
    `Primary: ${primary} (DOWN)\n` +
    `Reserve: ${selected.name} (ACTIVE)\n` +
    `Democracy score: ${selected.democracy_score}%\n` +
    `Will be used in next pipeline run automatically.`
  )
}

export async function POST(request: NextRequest): Promise<NextResponse> {
  // ── Security: verify Telegram secret token ──────────────
  const secretHeader = request.headers.get('x-telegram-bot-api-secret-token')
  if (!WEBHOOK_SECRET || secretHeader !== WEBHOOK_SECRET) {
    console.error('Webhook: Invalid or missing secret token')
    return NextResponse.json({ ok: false }, { status: 403 })
  }

  interface TelegramUpdate { message?: { from?: { id?: number }; text?: string } }
  let body: TelegramUpdate
  try {
    body = await request.json()
  } catch {
    return NextResponse.json({ ok: false }, { status: 400 })
  }

  // ── Extract message ───────────────────────────────────────
  const message = body?.message
  if (!message) {
    // Callback query or other update — ignore
    return NextResponse.json({ ok: true })
  }

  const fromId  = String(message?.from?.id || '')
  const text    = (message?.text || '').trim()

  // ── Security: only process messages from admin ────────────
  if (!ADMIN_ID || fromId !== ADMIN_ID) {
    console.log(`Webhook: Ignoring message from non-admin: ${fromId}`)
    return NextResponse.json({ ok: true })
  }

  // ── Process numeric reply (1-5) ───────────────────────────
  const choice = parseInt(text, 10)
  if (!isNaN(choice) && choice >= 1 && choice <= 5) {
    console.log(`Webhook: Admin chose reserve ${choice}`)
    const responseMsg = await processReserveChoice(choice)
    await sendAdminMessage(responseMsg)
    return NextResponse.json({ ok: true })
  }

  // ── Unknown message — guide admin ─────────────────────────
  if (text && !/^\s*$/.test(text)) {
    await sendAdminMessage(
      '⚠️ Unrecognised reply.\n' +
      'If a source is down, reply with a number (1-5) to select a reserve.\n' +
      'Wait for the next alert if you are unsure.'
    )
  }

  return NextResponse.json({ ok: true })
}
