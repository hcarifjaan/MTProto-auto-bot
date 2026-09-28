import os
import requests
import feedparser
import random

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_NAME = os.getenv("CHANNEL_NAME")

# 3 Mukhtalif Crypto News RSS Feeds
NEWS_RSS_URLS = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
    "https://decrypt.co/feed"
]

def fetch_latest_news():
    try:
        all_entries = []
        # Sabhi websites se entries collect karein
        for rss_url in NEWS_RSS_URLS:
            feed = feedparser.parse(rss_url)
            if feed.entries:
                # Har feed se pehli 3-3 fresh entries le lein
                all_entries.extend(feed.entries[:3])

        if not all_entries:
            return None, None, None

        # Randomly ek fresh news select karein taake har baar alag website se aaye
        random_entry = random.choice(all_entries)
        title = random_entry.title
        summary = random_entry.get("summary", "")

        # Image URL extract karne ki koshish
        image_url = None
        if 'media_thumbnail' in random_entry and len(random_entry.media_thumbnail) > 0:
            image_url = random_entry.media_thumbnail[0]['url']
        elif 'media_content' in random_entry and len(random_entry.media_content) > 0:
            image_url = random_entry.media_content[0]['url']
        elif 'links' in random_entry:
            for link in random_entry.links:
                if link.get('type', '').startswith('image/'):
                    image_url = link.href
                    break

        return title, summary, image_url
    except Exception as e:
        print(f"News fetch error: {e}")
        return None, None, None

def main():
    SECRET = "ee104462821249bd7ac519130220c25d097777772e636c6f7564666c6172652e636f6d"
    
    P1 = f"https://t.me/proxy?server=ajfastproxy.duckdns.org&port=8443&secret={SECRET}"
    P2 = f"https://t.me/proxy?server=arif007fastproxy.duckdns.org&port=8443&secret={SECRET}"
    P3 = f"https://t.me/proxy?server=arifproxy.duckdns.org&port=8443&secret={SECRET}"
    P4 = f"https://t.me/proxy?server=fastproxt.duckdns.org&port=8443&secret={SECRET}"
    P5 = f"https://t.me/proxy?server=jaanproxy.duckdns.org&port=8443&secret={SECRET}"

    title, summary, image_url = fetch_latest_news()
    
    if not title:
        print("No news found.")
        return

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
