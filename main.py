import os
import requests
import re

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_NAME = os.getenv("CHANNEL_NAME")

def get_proxy():
    sources = [
        "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/mtproto",
        "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/sub_merge.txt"
    ]
    
    for url in sources:
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                # Direct tg:// or t.me proxy links search karne ke liye regex
                matches = re.findall(r'(https://t\.me/proxy\?[^\s"\'<>]+|tg://proxy\?[^\s"\'<>]+)', res.text)
                if matches:
                    return matches[0]
        except Exception as e:
            print(f"Error fetching from {url}: {e}")

    return None

def main():
    proxy_link = get_proxy()
    if not proxy_link:
        print("No valid MTProto proxy link found.")
        return

    text = "⚡ **Fast MTProto Proxy** ⚡\n\nClick below to connect:"
    payload = {
        "chat_id": CHANNEL_NAME,
        "text": text,
        "parse_mode": "Markdown",
        "reply_markup": {
            "inline_keyboard": [[
                {"text": "🚀 Connect Proxy", "url": proxy_link}
            ]]
        }
    }
    
    tg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    res = requests.post(tg_url, json=payload)
    print("Telegram Response:", res.json())

if __name__ == "__main__":
    main()
