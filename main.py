import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_NAME = os.getenv("CHANNEL_NAME")

def get_proxy():
    url = "https://raw.githubusercontent.com/mftsp/tg-proxies/main/proxies.json"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            p = data[0]
            server = p.get('host') or p.get('server')
            port = p.get('port')
            secret = p.get('secret')
            if server and port and secret:
                return f"https://t.me/proxy?server={server}&port={port}&secret={secret}"
    except Exception as e:
        print(f"Primary source error: {e}")

    try:
        fallback_url = "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/mtproto"
        res = requests.get(fallback_url, timeout=10)
        if res.status_code == 200:
            lines = res.text.strip().split("\n")
            for line in lines:
                if line.startswith("tg://proxy") or line.startswith("https://t.me/proxy"):
                    return line.strip()
    except Exception as e:
        print(f"Fallback source error: {e}")

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
