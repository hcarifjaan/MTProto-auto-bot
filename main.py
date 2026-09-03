import os
import requests
import re
import random

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_NAME = os.getenv("CHANNEL_NAME")

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

    # Matching exact layout format
    text = (
        "⚡ <b>Fast MTProto Proxy</b> ⚡\n\n"
        f"<b><a href=\"{p1}\">پروکسی</a> | <a href=\"{p2}\">پروکسی</a> | <a href=\"{p3}\">پروکسی</a></b>\n"
        f"<b><a href=\"{p4}\">پروکسی</a> | <a href=\"{p5}\">پروکسی</a> | <a href=\"{p6}\">پروکسی</a></b>\n"
        f"<b><a href=\"{p7}\">پروکسی</a> | <a href=\"{p8}\">پروکسی</a> | <a href=\"{p9}\">پروکسی</a></b>\n"
        f"<b><a href=\"{p10}\">پروکسی</a> | <a href=\"{p11}\">پروکسی</a> | <a href=\"{p12}\">پروکسی</a></b>\n\n"
        f"🚀 <b><a href=\"{p1}\">Connect Proxy</a></b>"
    )
    
    payload = {
        "chat_id": CHANNEL_NAME,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    
    tg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    res = requests.post(tg_url, json=payload)
    print("Telegram Response:", res.json())

if __name__ == "__main__":
    main()
