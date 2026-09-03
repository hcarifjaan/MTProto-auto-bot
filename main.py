import os
import requests
import re

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_NAME = os.getenv("CHANNEL_NAME")

def get_live_proxies():
    # Active high-uptime sources for MTProto
    sources = [
        "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/mtproto",
        "https://raw.githubusercontent.com/mftsp/tg-proxies/main/proxies.txt",
        "https://raw.githubusercontent.com/MahdiBland/ShadowsocksAggregator/master/sub/sub_merge.txt",
        "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/mtproto.txt"
    ]
    
    found_links = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    for url in sources:
        try:
            res = requests.get(url, headers=headers, timeout=8)
            if res.status_code == 200 and res.text.strip():
                # Extract tg:// or t.me proxy links
                matches = re.findall(r'(https://t\.me/proxy\?[^\s"\'<>]+|tg://proxy\?[^\s"\'<>]+)', res.text)
                for m in matches:
                    clean_link = m.strip().replace("tg://proxy", "https://t.me/proxy")
                    if clean_link not in found_links:
                        found_links.append(clean_link)
                    if len(found_links) >= 6:
                        break
        except Exception as e:
            print(f"Fetch log: {e}")
            
        if len(found_links) >= 6:
            break

    return found_links

def main():
    proxies = get_live_proxies()

    # Dynamic fallback rotation with high-speed working domain MTProtos
    if len(proxies) < 6:
        working_backup = [
            "https://t.me/proxy?server=zemestan.goooalir.co.uk&port=8443&secret=7gAAAAAAAAAAAAAAAAAAAAB3d3cuZ29vZ2xlLmNvbQ",
            "https://t.me/proxy?server=esteghlal.goooalir.co.uk&port=8443&secret=7gAAAAAAAAAAAAAAAAAAAAB3d3cuZ29vZ2xlLmNvbQ",
            "https://t.me/proxy?server=nigan.goooalir.co.uk&port=8443&secret=7gAAAAAAAAAAAAAAAAAAAAB3d3cuZ29vZ2xlLmNvbQ",
            "https://t.me/proxy?server=leomessi.goooalir.co.uk&port=8443&secret=7gAAAAAAAAAAAAAAAAAAAAB3d3cuZ29vZ2xlLmNvbQ",
            "https://t.me/proxy?server=perspolis.goooalir.co.uk&port=8443&secret=7gAAAAAAAAAAAAAAAAAAAAB3d3cuZ29vZ2xlLmNvbQ",
            "https://t.me/proxy?server=narooo.goooalir.co.uk&port=8443&secret=7gAAAAAAAAAAAAAAAAAAAAB3d3cuZ29vZ2xlLmNvbQ"
        ]
        for p in working_backup:
            if p not in proxies:
                proxies.append(p)

    p1, p2, p3, p4, p5, p6 = proxies[:6]

    text = (
        "⚡ <b>Fast MTProto Proxy</b> ⚡\n\n"
        f"<b><a href=\"{p1}\">پروکسی</a> | <a href=\"{p2}\">پروکسی</a> | <a href=\"{p3}\">پروکسی</a></b>\n"
        f"<b><a href=\"{p4}\">پروکسی</a> | <a href=\"{p5}\">پروکسی</a> | <a href=\"{p6}\">پروکسی</a></b>\n\n"
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
