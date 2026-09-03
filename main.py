import os
import requests
import re
import base64

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_NAME = os.getenv("CHANNEL_NAME")

def get_proxies():
    sources = [
        "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/mtproto",
        "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/sub_merge.txt",
        "https://raw.githubusercontent.com/mftsp/tg-proxies/main/proxies.json"
    ]
    
    found_links = []
    
    for url in sources:
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                text = res.text
                
                # Base64 string decoding handling
                try:
                    decoded = base64.b64decode(text).decode('utf-8', errors='ignore')
                    text += "\n" + decoded
                except Exception:
                    pass

                # Extract tg:// or t.me proxy links
                matches = re.findall(r'(https://t\.me/proxy\?[^\s"\'<>]+|tg://proxy\?[^\s"\'<>]+)', text)
                for m in matches:
                    clean_link = m.strip().replace("tg://proxy", "https://t.me/proxy")
                    if clean_link not in found_links:
                        found_links.append(clean_link)
                    if len(found_links) >= 3:
                        break
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            
        if len(found_links) >= 3:
            break

    return found_links

def main():
    proxies = get_proxies()

    if not proxies:
        print("No valid proxies fetched. Skipping post.")
        return

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
