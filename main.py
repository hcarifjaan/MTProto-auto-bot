import os
import requests
import re

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_NAME = os.getenv("CHANNEL_NAME")

def get_proxies():
    # Public APIs & Raw List URLs
    sources = [
        "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/mtproto.txt",
        "https://raw.githubusercontent.com/mftsp/tg-proxies/main/proxies.txt",
        "https://raw.githubusercontent.com/BPJ/MTProto-Proxy/main/proxies.txt",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=mtproto&timeout=10000"
    ]
    
    found_links = []
    
    for url in sources:
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200 and res.text.strip():
                # 1. Search for direct telegram link formats
                matches = re.findall(r'(https://t\.me/proxy\?[^\s"\'<>]+|tg://proxy\?[^\s"\'<>]+)', res.text)
                for m in matches:
                    clean_link = m.strip().replace("tg://proxy", "https://t.me/proxy")
                    if clean_link not in found_links:
                        found_links.append(clean_link)

                # 2. Search for IP:PORT:SECRET formats
                lines = res.text.strip().split("\n")
                for line in lines:
                    parts = line.strip().split(":")
                    if len(parts) >= 2 and not parts[0].startswith("http"):
                        ip, port = parts[0], parts[1]
                        secret = parts[2] if len(parts) > 2 else "ee00000000000000000000000000000000"
                        link = f"https://t.me/proxy?server={ip}&port={port}&secret={secret}"
                        if link not in found_links:
                            found_links.append(link)

                if len(found_links) >= 3:
                    break
        except Exception as e:
            print(f"Fetch error: {e}")

    return found_links

def main():
    proxies = get_proxies()

    # Dynamic Fallback if sources delay
    if not proxies:
        proxies = [
            "https://t.me/proxy?server=51.89.24.83&port=443&secret=dd00000000000000000000000000000000",
            "https://t.me/proxy?server=163.172.191.139&port=443&secret=dd00000000000000000000000000000000",
            "https://t.me/proxy?server=51.15.241.207&port=443&secret=dd00000000000000000000000000000000"
        ]

    p1 = proxies[0]
    p2 = proxies[1] if len(proxies) > 1 else p1
    p3 = proxies[2] if len(proxies) > 2 else p1

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
