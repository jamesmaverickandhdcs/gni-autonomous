import { NextRequest, NextResponse } from 'next/server'
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_KEY!
)

const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN || ''
const TELEGRAM_ADMIN_CHAT_ID = process.env.TELEGRAM_ADMIN_CHAT_ID || process.env.TELEGRAM_CHAT_ID || ''
const TELEGRAM_WEBHOOK_SECRET = process.env.TELEGRAM_WEBHOOK_SECRET || ''

const VALID_ACTIONS = ['kw_approve', 'kw_watch', 'kw_reject'] as const
type KwAction = typeof VALID_ACTIONS[number]

// Security: validate UUID format
function isValidUUID(str: string): boolean {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/.test(str)
}

async function answerCallback(callbackQueryId: string, text: string) {
  await fetch(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/answerCallbackQuery`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ callback_query_id: callbackQueryId, text }),
  })
}

async function editMessage(chatId: string, messageId: number, text: string) {
  await fetch(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/editMessageText`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: chatId,
      message_id: messageId,
      text,
    }),
  })
}

export async function POST(request: NextRequest) {
  try {
    // Security: verify webhook secret header
    const secret = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
    if (TELEGRAM_WEBHOOK_SECRET && secret !== TELEGRAM_WEBHOOK_SECRET) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await request.json()
    const callbackQuery = body?.callback_query
    if (!callbackQuery) {
      return NextResponse.json({ ok: true })
    }

    const callbackQueryId = callbackQuery.id
    const fromId = String(callbackQuery.from?.id || '')
    const data = callbackQuery.data || ''
    const messageId = callbackQuery.message?.message_id
    const chatId = String(callbackQuery.message?.chat?.id || '')

    // Security: only admin can approve/reject
    if (TELEGRAM_ADMIN_CHAT_ID && fromId !== TELEGRAM_ADMIN_CHAT_ID) {
      await answerCallback(callbackQueryId, '⛔ Unauthorized')
      return NextResponse.json({ ok: true })
    }

    // Security: parse and validate callback data
    // Format: kw_approve_UUID or kw_watch_UUID or kw_reject_UUID
    const parts = data.split('_')
    if (parts.length < 3 || parts[0] !== 'kw') {
      await answerCallback(callbackQueryId, '❌ Invalid callback')
      return NextResponse.json({ ok: true })
    }

    const action = (parts[0] + '_' + parts[1]) as KwAction
    const keywordId = parts.slice(2).join('_') // UUID may contain hyphens

    if (!VALID_ACTIONS.includes(action)) {
      await answerCallback(callbackQueryId, '❌ Invalid action')
      return NextResponse.json({ ok: true })
    }

    // Security: validate UUID format -- never raw keyword text
    if (!isValidUUID(keywordId)) {
      await answerCallback(callbackQueryId, '❌ Invalid ID format')
      return NextResponse.json({ ok: true })
    }

    // Fetch keyword record
    const { data: kwData, error } = await supabase
      .from('emerging_keywords')
      .select('id, keyword, status')
      .eq('id', keywordId)
      .single()

    if (error || !kwData) {
      await answerCallback(callbackQueryId, '❌ Keyword not found')
      return NextResponse.json({ ok: true })
    }

    const keyword = kwData.keyword

    // Apply action
    let newStatus = ''
    let confirmText = ''
    const updateData: Record<string, unknown> = {
      reviewed: true,
      last_seen: new Date().toISOString(),
    }

    if (action === 'kw_approve') {
      newStatus = 'approved'
      confirmText = '✅ Approved: "' + keyword + '"'
      updateData.status = 'approved'
    } else if (action === 'kw_watch') {
      newStatus = 'watching'
      confirmText = '⏳ Watching: "' + keyword + '"'
      updateData.status = 'watching'
      updateData.watching_since = new Date().toISOString()
      updateData.watching_days = 0
    } else if (action === 'kw_reject') {
      newStatus = 'rejected'
      confirmText = '❌ Rejected: "' + keyword + '"'
      updateData.status = 'rejected'
      updateData.rejected_at = new Date().toISOString()
      // Save current frequency for re-emergence detection
      const { data: current } = await supabase
        .from('emerging_keywords')
        .select('frequency_count')
        .eq('id', keywordId)
        .single()
      if (current) {
        updateData.rejected_frequency = current.frequency_count
      }
    }

    // Update Supabase
    await supabase
      .from('emerging_keywords')
      .update(updateData)
      .eq('id', keywordId)

    // Answer callback -- removes loading state
    await answerCallback(callbackQueryId, confirmText)

    // Edit original message to show result (removes buttons)
    if (messageId && chatId) {
      await editMessage(
        chatId,
        messageId,
        confirmText + '\n\nKeyword: "' + keyword + '"\nStatus: ' + newStatus.toUpperCase()
      )
    }

    return NextResponse.json({ ok: true })

  } catch (err) {
    console.error('Telegram callback error:', err)
    return NextResponse.json({ error: 'Internal error' }, { status: 500 })
  }
}
