import os
import requests
import re
import random
import feedparser

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_NAME = os.getenv("CHANNEL_NAME")

# Latest News RSS Feed
NEWS_RSS_URL = "https://feeds.bbci.co.uk/news/world/rss.xml"

def fetch_latest_news():
    """BBC RSS Feed se latest news title, summary aur image extract karta hai."""
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

def get_exact_working_proxies():
    # Exact DD-secret required for goooalir servers
    SECRET = "dd104462821249bd7ac519130220c25d09"
    PORT = "8443"

    # Known live high-speed servers from this provider
    subdomains = [
        "AZADI", "napoli", "sefid", "behtarin", 
        "leomessi", "AVA", "nigan", "narooo", 
        "esteghlal", "zemestan", "perspolis"
    ]

    # Try scraping fresh subdomains directly from public TG channel mirrors
    scraped_subdomains = []
    try:
        res = requests.get("https://t.me/s/ProxyMTProto", timeout=5)
        if res.status_code == 200:
            matches = re.findall(r'server=([a-zA-Z0-9\.-]+)\.goooalir\.co\.uk', res.text)
            for m in matches:
                if m not in scraped_subdomains:
                    scraped_subdomains.append(m)
    except Exception as e:
        print(f"Scrape warning: {e}")

    # Combine scraped + verified list
    all_subdomains = scraped_subdomains + [s for s in subdomains if s not in scraped_subdomains]
    random.shuffle(all_subdomains)

    # Build active links with exact secret
    proxy_links = []
    for sub in all_subdomains[:12]:
        link = f"https://t.me/proxy?server={sub}.goooalir.co.uk&port={PORT}&secret={SECRET}"
        proxy_links.append(link)

    return proxy_links

def main():
    proxies = get_exact_working_proxies()

    p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12 = (proxies + proxies[:12])[:12]

    # Latest News fetch karein
    title, summary, image_url = fetch_latest_news()

    # News section ka text (agar news mil jaye)
    news_section = ""
    if title:
        news_section = f"📰 <b>{title}</b>\n\n"
        if summary:
            news_section += f"{summary}\n\n"
        news_section += "-----------------------------------\n\n"

    # Aap ka original exact layout format
    proxy_text = (
        "⚡⚡ <b>MTProto Fast Proxy</b> ⚡⚡\n\n"
        f"<b><a href=\"{p1}\">Proxy</a> | <a href=\"{p2}\">پروکسی</a> | <a href=\"{p3}\">Proxy</a></b>\n"
        f"<b><a href=\"{p4}\">Proxy</a> | <a href=\"{p5}\">پروکسی</a> | <a href=\"{p6}\">Proxy</a></b>\n"
        f"<b><a href=\"{p7}\">Proxy</a> | <a href=\"{p8}\">پروکسی</a> | <a href=\"{p9}\">Proxy</a></b>\n"
        f"<b><a href=\"{p10}\">Proxy</a> | <a href=\"{p11}\">پروکسی</a> | <a href=\"{p12}\">Proxy</a></b>\n\n"
        f"🚀 <b><a href=\"{p1}\">Connect Proxy</a></b>🌍\n\n"
        "<b>📢 Connect to any proxy. Use Telegram without a VPN. Fast and free. 🚀</b>\n\n"
        "<b>چینل کو سبسکرائب کریں</b>"
    )

    final_caption = news_section + proxy_text

    # Telegram Send Request (Photo agar majood ho, warna Text)
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
