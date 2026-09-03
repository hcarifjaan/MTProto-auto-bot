import os
import requests
import re

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_NAME = os.getenv("CHANNEL_NAME")

def get_proxies():
    sources = [
        "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/mtproto.txt",
        "https://raw.githubusercontent.com/v2fly/freenode/main/v2ray.txt",
        "https://raw.githubusercontent.com/E34678/Telegram-Proxies/main/proxies.txt"
    ]
    
    found_links = []
    
    for url in sources:
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                matches = re.findall(r'https://t\.me/proxy\?[^\s"\'<>]+', res.text)
                for m in matches:
                    clean_m = m.strip()
                    if clean_m not in found_links:
                        found_links.append(clean_m)
                    if len(found_links) >= 3:
                        break
        except Exception as e:
            print(f"Error fetching: {e}")
            
        if len(found_links) >= 3:
            break

    # Fallback agar scraper se links na milein
    fallback_link = "https://t.me/proxy?server=1.1.1.1&port=443&secret=ee00000000000000000000000000000000"
    while len(found_links) < 3:
        found_links.append(fallback_link)

    return found_links

def main():
    proxies = get_proxies()

    p1, p2, p3 = proxies[0], proxies[1], proxies[2]

    # Clean HTML code with valid non-empty links
    text = (
        "⚡ <b>Fast MTProto Proxy</b> ⚡\n\n"
        f"<b><a href=\"{p1}\">پروکسی</a> | <a href=\"{p2}\">پروکسی</a> | <a href=\"{p3}\">پروکسی</a></b>\n"
        f"<b><a href=\"{p1}\">پروکسی</a> | <a href=\"{p2}\">پروکسی</a> | <a href=\"{p3}\">پروکسی</a></b>\n\n"
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
