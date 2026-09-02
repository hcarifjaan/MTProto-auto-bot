import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_NAME = os.getenv("CHANNEL_NAME")

# Live MTProto Proxy Source
PROXY_SOURCE_URL = "https://raw.githubusercontent.com/hookzof/socks5_list/master/tg/mtproto.json"

def get_proxies():
    try:
        response = requests.get(PROXY_SOURCE_URL, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching proxies: {e}")
    return []

def send_telegram_post(server, port, secret):
    proxy_link = f"https://t.me/proxy?server={server}&port={port}&secret={secret}"
    
    caption = (
        "⚡️ **Fast MTProto Proxy**\n\n"
        "🟢 **Status:** Active & Encrypted\n"
        "🛡 **Security:** High\n\n"
        "👇 Click below button to connect:"
    )
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_NAME,
        "text": caption,
        "parse_mode": "Markdown",
        "reply_markup": {
            "inline_keyboard": [[
                {"text": "🚀 Connect Proxy", "url": proxy_link}
            ]]
        }
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    proxies = get_proxies()
    if proxies:
        p = proxies[0]
        send_telegram_post(p['host'], p['port'], p['secret'])
        print("Proxy posted successfully!")
    else:
        print("No proxy found.")
