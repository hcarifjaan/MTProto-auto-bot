import os
import requests
import feedparser

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_NAME = os.getenv("CHANNEL_NAME")

# Latest News RSS Feed
NEWS_RSS_URL = "https://www.coindesk.com/arc/outboundfeeds/rss/"

def fetch_latest_news():
    """RSS Feed se latest news title, summary aur image extract karta hai."""
    try:
        feed = feedparser.parse(NEWS_RSS_URL)
        if not feed.entries:
            return None, None, None

        first_entry = feed.entries[0]
        title = first_entry.title
        summary = first_entry.get("summary", "")

        # Image URL extract karne ki koshish
        image_url = None
        if 'media_thumbnail' in first_entry and len(first_entry.media_thumbnail) > 0:
            image_url = first_entry.media_thumbnail[0]['url']
        elif 'media_content' in first_entry and len(first_entry.media_content) > 0:
            image_url = first_entry.media_content[0]['url']
        elif 'links' in first_entry:
            for link in first_entry.links:
                if link.get('type', '').startswith('image/'):
                    image_url = link.href
                    break

        return title, summary, image_url
    except Exception as e:
        print(f"News fetch error: {e}")
        return None, None, None

def main():
    # Aap ki apni Oracle Cloud MTProto Proxy link
    MY_PROXY = "https://t.me/proxy?server=92.5.166.165&port=443&secret=2e6aadc2a1d8277fbbd3a311a0592dfc"

    # Latest News fetch karein
    title, summary, image_url = fetch_latest_news()

    # News section ka text (agar news mil jaye)
    news_section = ""
    if title:
        news_section = f"📰 <b>{title}</b>\n\n"
        if summary:
            news_section += f"{summary}\n\n"
        news_section += "-----------------------------------\n\n"

    # Exact layout format aapki apni proxy ke sath
    proxy_text = (
        "⚡⚡ <b>MTProto Fast Proxy</b> ⚡⚡\n\n"
        f"<b><a href=\"{MY_PROXY}\">Proxy</a> | <a href=\"{MY_PROXY}\">پروکسی</a> | <a href=\"{MY_PROXY}\">Proxy</a></b>\n"
        f"<b><a href=\"{MY_PROXY}\">Proxy</a> | <a href=\"{MY_PROXY}\">پروکسی</a> | <a href=\"{MY_PROXY}\">Proxy</a></b>\n"
        f"<b><a href=\"{MY_PROXY}\">Proxy</a> | <a href=\"{MY_PROXY}\">پروکسی</a> | <a href=\"{MY_PROXY}\">Proxy</a></b>\n"
        f"<b><a href=\"{MY_PROXY}\">Proxy</a> | <a href=\"{MY_PROXY}\">پروکسی</a> | <a href=\"{MY_PROXY}\">Proxy</a></b>\n\n"
        f"🚀 <b><a href=\"{MY_PROXY}\">Connect Proxy</a></b> 🌍\n\n"
        "<b>📢 Connect to any proxy. Use Telegram without a VPN. Fast and free. 🚀</b>\n\n"
        "<b>چینل کو سبسکرائب کریں</b>"
    )

    final_caption = news_section + proxy_text

    # Telegram Send Request
    if image_url:
        tg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        payload = {
            "chat_id": CHANNEL_NAME,
            "photo": image_url,
            "caption": final_caption,
            "parse_mode": "HTML"
        }
    else:
        tg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHANNEL_NAME,
            "text": final_caption,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }

    res = requests.post(tg_url, json=payload)
    print("Telegram Response:", res.json())

if __name__ == "__main__":
    main()
