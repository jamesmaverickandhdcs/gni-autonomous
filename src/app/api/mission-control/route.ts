export const dynamic = 'force-dynamic'
import { createClient } from '@supabase/supabase-js'
import { NextRequest, NextResponse } from 'next/server'


const INTERNAL_KEY = process.env.SELF_CHECK_INTERNAL_KEY || 'gni-internal-missioncontrol'

async function sendTelegram(message: string) {
  const token = process.env.TELEGRAM_BOT_TOKEN
  const chatId = process.env.TELEGRAM_ADMIN_CHAT_ID || process.env.TELEGRAM_QSChannel_ID
  if (!token || !chatId) return
  try {
    await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: chatId, text: message, parse_mode: 'HTML' })
    })
  } catch (e) { console.error('Telegram error:', e) }
}

async function wasTelegramSentRecently(): Promise<boolean> {
  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
  try {
    const twoHoursAgo = new Date(Date.now() - 2 * 3600000).toISOString()
    const { data } = await supabase.from('mission_control_log')
      .select('id').eq('telegram_sent', true).gte('checked_at', twoHoursAgo).limit(1)
    return (data || []).length > 0
  } catch { return false }
}

export async function GET(request: NextRequest) {
  const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)
  const isInternal = request.headers.get('X-Internal-Key') === INTERNAL_KEY

  // Public access: return last cached result only
  if (!isInternal) {
    try {
      const { data } = await supabase.from('mission_control_log')
        .select('*').order('checked_at', { ascending: false }).limit(1)
      if (data && data.length > 0) return NextResponse.json({ ...data[0], cached: true })
      return NextResponse.json({ overall_status: 'UNKNOWN', cached: true })
    } catch {
      return NextResponse.json({ overall_status: 'UNKNOWN', cached: true })
    }
  }

  // Internal check
  const startTime = Date.now()
  const checks: Record<string, { status: string; message: string }> = {}
  let issuesFound = 0
  let telegramSent = false
  const baseUrl = process.env.NEXT_PUBLIC_APP_URL || 'https://gni-autonomous.vercel.app'

  // Check 1: Supabase connection (UNIQUE -- no existing page tests this)
  try {
    const { error } = await supabase.from('reports').select('id').limit(1)
    if (error) throw error
    checks['supabase_connection'] = { status: 'OK', message: 'Supabase connected successfully' }
  } catch (e) {
    checks['supabase_connection'] = { status: 'CRITICAL', message: 'Supabase connection failed: ' + (e instanceof Error ? e.message : String(e)) }
    issuesFound++
  }

  // Check 2: Latest report age (UNIQUE aggregation)
  try {
    const { data, error } = await supabase.from('reports')
      .select('created_at').order('created_at', { ascending: false }).limit(1)
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
    checks['latest_report'] = { status: 'CRITICAL', message: 'Failed: ' + (e instanceof Error ? e.message : String(e)) }
    issuesFound++
  }

  // Check 3: Quota status -- call existing /api/quota (NO DUPLICATION)
  try {
    const res = await fetch(`${baseUrl}/api/quota`, { signal: AbortSignal.timeout(5000) })
    const data = await res.json()
    const usage = data.usage || []
    const today = new Date().toISOString().split('T')[0]
    const todayUsage = usage.filter((u: {created_at: string}) => u.created_at.startsWith(today))
    const totalTokens = todayUsage.reduce((s: number, u: {tokens_used: number}) => s + (u.tokens_used || 0), 0)
    const pct = Math.round((totalTokens / 100000) * 100)
    // Check pipeline recency from same data
    const pipelineRuns = usage.filter((u: {pipeline: string, created_at: string}) =>
      u.pipeline === 'gni_pipeline' &&
      new Date(u.created_at).getTime() > Date.now() - 20 * 3600000
    )
    const madRuns = usage.filter((u: {pipeline: string, created_at: string}) =>
      u.pipeline === 'gni_mad' &&
      new Date(u.created_at).getTime() > Date.now() - 20 * 3600000
    )
    if (pct >= 90) {
      checks['groq_quota'] = { status: 'CRITICAL', message: `Quota at ${pct}% -- ${totalTokens}/100000 tokens today` }
      issuesFound++
    } else if (pct >= 70) {
      checks['groq_quota'] = { status: 'WARNING', message: `Quota at ${pct}% -- monitor closely` }
      issuesFound++
    } else {
      checks['groq_quota'] = { status: 'OK', message: `Quota at ${pct}% -- ${totalTokens}/100000 tokens today` }
    }
    checks['pipeline_recent'] = pipelineRuns.length > 0
      ? { status: 'OK', message: 'gni_pipeline ran within last 20 hours' }
      : { status: 'WARNING', message: 'No gni_pipeline run in last 20 hours -- check sacred cron' }
    checks['mad_recent'] = madRuns.length > 0
      ? { status: 'OK', message: 'gni_mad ran within last 20 hours' }
      : { status: 'WARNING', message: 'No gni_mad run in last 20 hours -- check sacred cron' }
    if (pipelineRuns.length === 0) issuesFound++
    if (madRuns.length === 0) issuesFound++
  } catch (e) {
    checks['groq_quota'] = { status: 'WARNING', message: 'Could not reach /api/quota: ' + (e instanceof Error ? e.message : String(e)) }
    checks['pipeline_recent'] = { status: 'WARNING', message: 'Could not verify pipeline run' }
    checks['mad_recent'] = { status: 'WARNING', message: 'Could not verify MAD run' }
    issuesFound++
  }

  // Check 4: Source health -- call existing /api/source-health (NO DUPLICATION)
  try {
    const res = await fetch(`${baseUrl}/api/source-health`, { headers: { 'X-GNI-Key': process.env.GNI_API_KEYS?.split(',')[0] || '' }, signal: AbortSignal.timeout(5000) })
    const data = await res.json()
    const sources = data.sources || []
    const healthy = sources.filter((s: {status: string}) => s.status === 'healthy').length
    const total = sources.length
    if (total === 0) {
      checks['source_health'] = { status: 'WARNING', message: 'No source health data available' }
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
    checks['source_health'] = { status: 'WARNING', message: 'Could not reach /api/source-health: ' + (e instanceof Error ? e.message : String(e)) }
  }

  // Determine overall status
  const hasCritical = Object.values(checks).some(c => c.status === 'CRITICAL')
  const hasWarning = Object.values(checks).some(c => c.status === 'WARNING')
  const overallStatus = hasCritical ? 'CRITICAL' : hasWarning ? 'WARNING' : 'HEALTHY'

  // Send Telegram -- max once per 2 hours (deduplication)
  if (issuesFound > 0) {
    const recentAlert = await wasTelegramSentRecently()
    if (!recentAlert) {
      const lines = Object.entries(checks)
        .filter(([, v]) => v.status !== 'OK')
        .map(([k, v]) => `${v.status === 'CRITICAL' ? '??' : '??'} ${k}: ${v.message}`)
        .join('\n')
      const msg = `??? <b>GNI Mission Control: ${overallStatus}</b>\n${issuesFound} issue(s) found\n\n${lines}\n\nTime: ${new Date().toISOString()}`
      await sendTelegram(msg)
      telegramSent = true
    }
  }

  // Save to mission_control_log
  try {
    await supabase.from('mission_control_log').insert({
      overall_status: overallStatus,
      checks,
      issues_found: issuesFound,
      auto_healed: 0,
      telegram_sent: telegramSent
    })
  } catch (e) { console.error('Save failed:', e) }

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
