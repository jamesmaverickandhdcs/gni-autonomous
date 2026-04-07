import os
import requests
from datetime import datetime

# ============================================================
# GNI Telegram Notifier — Updated S21-2
# Channel: Clean 11 article links + web app intro only
# Admin: CRITICAL ALERT only (escalation >= 8)
# HEARTBEAT/ADAPTIVE/STATUS → admin via monitoring_pipeline.py
# ============================================================


def send_telegram_message(text: str) -> bool:
    """Send a message to the public Telegram channel."""
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_QSChannel_ID = os.getenv("TELEGRAM_QSChannel_ID")

    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_QSChannel_ID:
        print("  ⚠️  Telegram credentials not configured — skipping")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_QSChannel_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("  ✅ Channel message sent")
            return True
        else:
            print(f"  ⚠️  Telegram error: {response.status_code} {response.text[:100]}")
            return False
    except Exception as e:
        print(f"  ⚠️  Telegram exception: {e}")
        return False


def send_admin_message(text: str) -> bool:
    """Send message to admin only — never to public channel."""
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_ADMIN_ID = os.getenv("TELEGRAM_ADMIN_ID") or os.getenv("TELEGRAM_QSChannel_ID")

    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_ADMIN_ID:
        print("  ⚠️  Admin credentials not configured — skipping")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_ADMIN_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("  ✅ Admin message sent")
            return True
        else:
            print(f"  ⚠️  Admin Telegram error: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ⚠️  Admin Telegram exception: {e}")
        return False


def format_channel_message(report: dict, articles: list) -> str:
    """
    Format clean user-facing channel message.
    Shows: date/time + 11 article links + web app links + intro.
    Nothing else. Simple. User-friendly.
    """
    timestamp = datetime.now().strftime("%B %d, %Y | %H:%M UTC")
    total = len(articles)

    # Build article list with clickable links
    article_lines = ""
    for i, art in enumerate(articles, 1):
        source = art.get("source", "Unknown")
        title = art.get("title", "Untitled")
        score = art.get("stage3_score", 0)
        url = art.get("link") or art.get("url", "")

        # Truncate long titles
        if len(title) > 75:
            title = title[:72] + "..."

        if url:
            article_lines += (
                f"\n{i}. [{source}] "
                f"<a href=\"{url}\">{title}</a> "
                f"(Score: {score})"
            )
        else:
            article_lines += f"\n{i}. [{source}] {title} (Score: {score})"

    message = (
        "🌐 <b>GNI — Global Nexus Insights</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"📅 {timestamp}\n\n"
        f"Today's AI selected these {total} articles from 400+ "
        f"global sources — ranked by geopolitical significance:"
        f"{article_lines}\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🗺️ <a href=\"https://gni-autonomous.vercel.app/map\">Event Map</a>"
        " | 📈 <a href=\"https://gni-autonomous.vercel.app/stocks\">Stock Chart</a>"
        " | 🔍 <a href=\"https://gni-autonomous.vercel.app\">Dashboard</a>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "GNI turns 400+ daily articles into 1 intelligence report\n"
        "— free, autonomous, always on. No login needed.\n"
        "🌐 gni-autonomous.vercel.app"
    )

    return message


def send_critical_alert(report: dict) -> bool:
    """Send CRITICAL ALERT to admin only when escalation >= 8."""
    escalation_score = report.get("escalation_score", 0.0)
    escalation_level = report.get("escalation_level", "")

    alert_msg = (
        "🚨🚨🚨 <b>CRITICAL ALERT — GNI_Autonomous</b> 🚨🚨🚨\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"Escalation Score: <b>{escalation_score}/10 [{escalation_level}]</b>\n\n"
        f"<b>Report:</b> {report.get('title', '')}\n"
        f"<b>Sentiment:</b> {report.get('sentiment', '')}\n"
        f"<b>Risk Level:</b> {report.get('risk_level', '')}\n"
        f"<b>Location:</b> {report.get('location_name', '')}\n\n"
        "⚠️ All three GNI intelligence pillars are active.\n"
        "Immediate human review recommended.\n\n"
        "📊 <a href=\"https://gni-autonomous.vercel.app\">View Dashboard</a>"
        " | <a href=\"https://gni-autonomous.vercel.app/transparency\">Transparency</a>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "<i>⚠️ For informational purposes only. Not financial advice.</i>"
    )

    return send_admin_message(alert_msg)


def notify_report(report: dict, articles: list = None) -> bool:
    """
    Send Telegram notification after each pipeline run.

    Channel receives:
    - Clean 11 article links + Event Map + Stock Chart + Dashboard
    - Sweet intro about the web app

    Admin receives:
    - CRITICAL ALERT only (if escalation_score >= 8)

    Everything else (HEARTBEAT / ADAPTIVE / STATUS) is handled
    by monitoring_pipeline.py via _send_telegram() which already
    routes to TELEGRAM_ADMIN_ID when set.
    """
    print("\n📱 Sending Telegram Notification...")

    # CRITICAL ALERT → admin only
    escalation_score = report.get("escalation_score", 0.0)
    if escalation_score >= 8:
        print(f"  🚨 CRITICAL escalation {escalation_score}/10 → admin only")
        send_critical_alert(report)

    # Channel message → clean article list only
    if articles:
        msg = format_channel_message(report, articles)
        return send_telegram_message(msg)

    print("  ⚠️  No articles provided — skipping channel message")
    return True


if __name__ == "__main__":
    from dotenv import load_dotenv
    dotenv_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        '.env'
    )
    load_dotenv(dotenv_path)

    # Test with dummy data
    test_report = {
        "title": "Strait of Hormuz Closure Threatens Global Energy",
        "sentiment": "Bearish",
        "sentiment_score": -0.80,
        "risk_level": "High",
        "escalation_score": 10.0,
        "escalation_level": "CRITICAL",
        "location_name": "Iran",
    }
    test_articles = [
        {
            "source": "Al Jazeera",
            "title": "Iran launches missile strikes on Israel",
            "url": "https://aljazeera.com",
            "stage3_score": 18.8
        },
        {
            "source": "BBC",
            "title": "Oil prices surge amid Middle East tensions",
            "url": "https://bbc.com",
            "stage3_score": 17.5
        },
        {
            "source": "USNI News",
            "title": "IRGC Opens Tolled Passage for Merchant Ships",
            "url": "https://news.usni.org",
            "stage3_score": 16.9
        },
    ]
    notify_report(test_report, test_articles)