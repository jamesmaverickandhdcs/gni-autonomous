export const dynamic = 'force-dynamic'
import { createClient } from '@supabase/supabase-js'
import { NextResponse } from 'next/server'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

async function sendTelegram(message: string) {
  const token = process.env.TELEGRAM_BOT_TOKEN
  const chatId = process.env.TELEGRAM_CHAT_ID
  if (!token || !chatId) return
  try {
    await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: chatId, text: message, parse_mode: 'HTML' })
    })
  } catch (e) { console.error('Telegram error:', e) }
}

export async function GET() {
  const startTime = Date.now()
  const checks: Record<string, { status: string; message: string }> = {}
  let issuesFound = 0
  let telegramSent = false

  // Check 1: Supabase connection
  try {
    const { error } = await supabase.from('reports').select('id').limit(1)
    if (error) throw error
    checks['supabase_connection'] = { status: 'OK', message: 'Supabase connected successfully' }
  } catch (e) {
    checks['supabase_connection'] = { status: 'CRITICAL', message: 'Supabase connection failed: ' + (e instanceof Error ? e.message : JSON.stringify(e)) }
    issuesFound++
  }

  // Check 2: Latest report < 24 hours old
  try {
    const { data, error } = await supabase
      .from('reports').select('created_at').order('created_at', { ascending: false }).limit(1)
    if (error) throw error
    if (!data || data.length === 0) {
      checks['latest_report'] = { status: 'CRITICAL', message: 'No reports found in database' }
      issuesFound++
    } else {
      const hoursOld = Math.round((Date.now() - new Date(data[0].created_at).getTime()) / 3600000)
      if (hoursOld > 24) {
        checks['latest_report'] = { status: 'WARNING', message: `Latest report is ${hoursOld} hours old -- pipeline may have missed a run` }
        issuesFound++
      } else {
        checks['latest_report'] = { status: 'OK', message: `Latest report is ${hoursOld} hours old` }
      }
    }
  } catch (e) {
    checks['latest_report'] = { status: 'CRITICAL', message: 'Failed to fetch latest report: ' + (e instanceof Error ? e.message : JSON.stringify(e)) }
    issuesFound++
  }

  // Check 3: Groq quota
  try {
    const today = new Date().toISOString().split('T')[0]
    const { data, error } = await supabase.from('groq_daily_usage').select('tokens_used').gte('created_at', today)
    if (error) throw error
    const totalTokens = (data || []).reduce((sum: number, row: { tokens_used: number }) => sum + (row.tokens_used || 0), 0)
    const pct = Math.round((totalTokens / 100000) * 100)
    if (pct >= 90) {
      checks['groq_quota'] = { status: 'CRITICAL', message: `Quota at ${pct}% -- ${totalTokens}/100000 tokens used today` }
      issuesFound++
    } else if (pct >= 70) {
      checks['groq_quota'] = { status: 'WARNING', message: `Quota at ${pct}% -- monitor closely` }
      issuesFound++
    } else {
      checks['groq_quota'] = { status: 'OK', message: `Quota at ${pct}% -- ${totalTokens}/100000 tokens` }
    }
  } catch (e) {
    checks['groq_quota'] = { status: 'WARNING', message: 'Could not check quota: ' + (e instanceof Error ? e.message : JSON.stringify(e)) }
  }

  // Check 4: Source health
  try {
    const { data, error } = await supabase.from('source_health').select('status').order('created_at', { ascending: false }).limit(25)
    if (error) throw error
    const sources = data || []
    const healthy = sources.filter((s: { status: string }) => s.status === 'healthy').length
    const total = sources.length
    if (total === 0) {
      checks['source_health'] = { status: 'WARNING', message: 'No source health data found' }
    } else if (healthy < total * 0.5) {
      checks['source_health'] = { status: 'CRITICAL', message: `Only ${healthy}/${total} sources healthy` }
      issuesFound++
    } else if (healthy < total * 0.8) {
      checks['source_health'] = { status: 'WARNING', message: `${healthy}/${total} sources healthy -- some degraded` }
      issuesFound++
    } else {
      checks['source_health'] = { status: 'OK', message: `${healthy}/${total} sources healthy` }
    }
  } catch (e) {
    checks['source_health'] = { status: 'WARNING', message: 'Could not check sources: ' + (e instanceof Error ? e.message : JSON.stringify(e)) }
  }

  // Check 5: Pipeline ran in last 12 hours
  try {
    const twelveHoursAgo = new Date(Date.now() - 12 * 3600000).toISOString()
    const { data, error } = await supabase.from('groq_daily_usage')
      .select('created_at').eq('pipeline_type', 'gni_pipeline').gte('created_at', twelveHoursAgo).limit(1)
    if (error) throw error
    if (!data || data.length === 0) {
      checks['pipeline_recent'] = { status: 'WARNING', message: 'No pipeline run in last 12 hours' }
      issuesFound++
    } else {
      checks['pipeline_recent'] = { status: 'OK', message: 'Pipeline ran within last 12 hours' }
    }
  } catch (e) {
    checks['pipeline_recent'] = { status: 'WARNING', message: 'Could not check pipeline: ' + (e instanceof Error ? e.message : JSON.stringify(e)) }
  }

  // Check 6: MAD debate ran in last 12 hours
  try {
    const twelveHoursAgo = new Date(Date.now() - 12 * 3600000).toISOString()
    const { data, error } = await supabase.from('groq_daily_usage')
      .select('created_at').eq('pipeline_type', 'gni_mad').gte('created_at', twelveHoursAgo).limit(1)
    if (error) throw error
    if (!data || data.length === 0) {
      checks['mad_recent'] = { status: 'WARNING', message: 'No MAD debate in last 12 hours' }
      issuesFound++
    } else {
      checks['mad_recent'] = { status: 'OK', message: 'MAD debate ran within last 12 hours' }
    }
  } catch (e) {
    checks['mad_recent'] = { status: 'WARNING', message: 'Could not check MAD runs: ' + (e instanceof Error ? e.message : JSON.stringify(e)) }
  }

  // Determine overall status
  const hasCritical = Object.values(checks).some(c => c.status === 'CRITICAL')
  const hasWarning = Object.values(checks).some(c => c.status === 'WARNING')
  const overallStatus = hasCritical ? 'CRITICAL' : hasWarning ? 'WARNING' : 'HEALTHY'

  // Send Telegram if issues found
  if (issuesFound > 0) {
    const lines = Object.entries(checks)
      .filter(([, v]) => v.status !== 'OK')
      .map(([k, v]) => `${v.status === 'CRITICAL' ? '??' : '??'} ${k}: ${v.message}`)
      .join('\n')
    const msg = `??? <b>GNI Self-Check Alert</b>\nStatus: <b>${overallStatus}</b> | Issues: ${issuesFound}\n\n${lines}\n\nTime: ${new Date().toISOString()}`
    await sendTelegram(msg)
    telegramSent = true
  }

  // Save to self_check_log
  try {
    await supabase.from('self_check_log').insert({
      overall_status: overallStatus,
      checks,
      issues_found: issuesFound,
      auto_healed: 0,
      telegram_sent: telegramSent
    })
  } catch (e) { console.error('Failed to save self-check log:', e) }

  return NextResponse.json({
    overall_status: overallStatus,
    issues_found: issuesFound,
    auto_healed: 0,
    telegram_sent: telegramSent,
    duration_ms: Date.now() - startTime,
    checked_at: new Date().toISOString(),
    checks
  })
}
