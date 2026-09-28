import os
import requests
import feedparser
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_NAME = os.getenv("CHANNEL_NAME")

NEWS_RSS_URL = "https://www.coindesk.com/arc/outboundfeeds/rss/"
HISTORY_FILE = "last_posted.json"

def get_last_posted_title():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("title")
        except:
            return None
    return None

def save_last_posted_title(title):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump({"title": title}, f)

def fetch_latest_news():
    try:
        feed = feedparser.parse(NEWS_RSS_URL)
        if not feed.entries:
            return None, None, None, None

        last_title = get_last_posted_title()
        
        # Aisi entry dhoondें jo pehle post na hui ho
        target_entry = None
        for entry in feed.entries:
            if entry.title != last_title:
                target_entry = entry
                break
        
        # Agar saari entries purani hain, toh sab se pehli utha lein taake loop na ruke
        if not target_entry and feed.entries:
            target_entry = feed.entries[0]

        if not target_entry:
            return None, None, None, None

        title = target_entry.title
        summary = target_entry.get("summary", "")

        image_url = None
        if 'media_thumbnail' in target_entry and len(target_entry.media_thumbnail) > 0:
            image_url = target_entry.media_thumbnail[0]['url']
        elif 'media_content' in target_entry and len(target_entry.media_content) > 0:
            image_url = target_entry.media_content[0]['url']
        elif 'links' in target_entry:
            for link in target_entry.links:
                if link.get('type', '').startswith('image/'):
                    image_url = link.href
                    break

        return title, summary, image_url, title
    except Exception as e:
        print(f"News fetch error: {e}")
        return None, None, None, None

def main():
    SECRET = "ee104462821249bd7ac519130220c25d097777772e636c6f7564666c6172652e636f6d"
    
    P1 = f"https://t.me/proxy?server=ajfastproxy.duckdns.org&port=8443&secret={SECRET}"
    P2 = f"https://t.me/proxy?server=arif007fastproxy.duckdns.org&port=8443&secret={SECRET}"
    P3 = f"https://t.me/proxy?server=arifproxy.duckdns.org&port=8443&secret={SECRET}"
    P4 = f"https://t.me/proxy?server=fastproxt.duckdns.org&port=8443&secret={SECRET}"
    P5 = f"https://t.me/proxy?server=jaanproxy.duckdns.org&port=8443&secret={SECRET}"

    title, summary, image_url, current_title = fetch_latest_news()
    
    if not title:
        print("No news found.")
        return

    # Save current title to history so it won't repeat next time
    save_last_posted_title(current_title)

    news_section = f"📰 <b>{title}</b>\n\n"
    if summary:
        news_section += f"{summary}\n\n"
    news_section += "-----------------------------------\n\n"

    proxy_text = (
        "⚡⚡ <b>MTProto Fast Proxy</b> ⚡⚡\n\n"
        f"<b><a href=\"{P1}\">Proxy 1</a> | <a href=\"{P2}\">پروکسی 2</a> | <a href=\"{P3}\">Proxy 3</a></b>\n"
        f"<b><a href=\"{P4}\">Proxy 4</a> | <a href=\"{P5}\">پروکسی 5</a> | <a href=\"{P1}\">Proxy 1</a></b>\n"
        f"<b><a href=\"{P2}\">Proxy 2</a> | <a href=\"{P3}\">پروکسی 3</a> | <a href=\"{P4}\">Proxy 4</a></b>\n"
        f"<b><a href=\"{P5}\">Proxy 5</a> | <a href=\"{P1}\">پروکسی 1</a> | <a href=\"{P2}\">Proxy 2</a></b>\n\n"
        f"🚀 <b><a href=\"{P3}\">Connect Fast Proxy</a></b> 🌍\n\n"
        "<b>📢 Connect to any proxy. Use Telegram without a VPN. Fast and free. 🚀</b>\n\n"
        "<b>چینل کو سبسکرائب کریں</b>"
    )

    final_caption = news_section + proxy_text

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
