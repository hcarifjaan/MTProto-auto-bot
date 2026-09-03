import os
import requests
import re

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_NAME = os.getenv("CHANNEL_NAME")

def verify_and_get_proxies():
    # Fresh dynamic sources for MTProto
    sources = [
        "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/mtproto",
        "https://raw.githubusercontent.com/mftsp/tg-proxies/main/proxies.txt",
        "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/mtproto.txt",
        "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt"
    ]
    
    found_links = []
    
    for url in sources:
        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200 and res.text.strip():
                # Extract links with valid servers and secrets
                matches = re.findall(r'(https://t\.me/proxy\?[^\s"\'<>]+|tg://proxy\?[^\s"\'<>]+)', res.text)
                for m in matches:
                    clean_link = m.strip().replace("tg://proxy", "https://t.me/proxy")
                    
                    # Ensure secret and server are present
                    if "server=" in clean_link and "secret=" in clean_link:
                        if clean_link not in found_links:
                            found_links.append(clean_link)
                            
                    if len(found_links) >= 6:
                        break
        except Exception as e:
            print(f"Skipping unresponsive source: {e}")
            
        if len(found_links) >= 6:
            break

    return found_links

def main():
    proxies = verify_and_get_proxies()

    # Agar online fresh proxies nahi milti toh job skip kar do (dead proxy post nahi hogi)
    if len(proxies) < 3:
        print("No active/fresh proxies available right now. Skipping execution to avoid unavailable links.")
        return

    p1 = proxies[0]
    p2 = proxies[1] if len(proxies) > 1 else p1
    p3 = proxies[2] if len(proxies) > 2 else p1
    p4 = proxies[3] if len(proxies) > 3 else p1
    p5 = proxies[4] if len(proxies) > 4 else p2
    p6 = proxies[5] if len(proxies) > 5 else p3

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
