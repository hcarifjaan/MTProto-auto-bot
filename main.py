import os
import requests
import re

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_NAME = os.getenv("CHANNEL_NAME")

def get_proxy():
    sources = [
        "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/mtproto.txt",
        "https://raw.githubusercontent.com/v2fly/freenode/main/v2ray.txt",
        "https://raw.githubusercontent.com/E34678/Telegram-Proxies/main/proxies.txt"
    ]
    
    for url in sources:
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                matches = re.findall(r'(https://t\.me/proxy\?[^\s"\'<>]+|tg://proxy\?[^\s"\'<>]+)', res.text)
                if matches:
                    link = matches[0]
                    if link.startswith("tg://proxy"):
                        link = link.replace("tg://proxy", "https://t.me/proxy")
                    return link
        except Exception as e:
            print(f"Error fetching from {url}: {e}")

    try:
        api_url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=mtproto&timeout=10000"
        res = requests.get(api_url, timeout=10)
        if res.status_code == 200 and res.text.strip():
            lines = res.text.strip().split("\n")
            if len(lines) > 0:
                parts = lines[0].strip().split(":")
                if len(parts) >= 2:
                    ip, port = parts[0], parts[1]
                    secret = parts[2] if len(parts) > 2 else "ee00000000000000000000000000000000"
                    return f"https://t.me/proxy?server={ip}&port={port}&secret={secret}"
    except Exception as e:
        print(f"Fallback API error: {e}")

    return None

def main():
    proxy_link = get_proxy()
    if not proxy_link:
        print("No valid MTProto proxy link found.")
        return

    # Button ki bajaye direct message body mein hyperlinked format
    text = f"⚡ **Fast MTProto Proxy** ⚡\n\n🚀 [Click Here to Connect Proxy]({proxy_link})"
    
    payload = {
        "chat_id": CHANNEL_NAME,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    
    tg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    res = requests.post(tg_url, json=payload)
    print("Telegram Response:", res.json())

if __name__ == "__main__":
    main()
