import feedparser
import time
import threading
import requests
from flask import Flask
import os

# === Load from environment ===
BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

BINANCE_RSS = 'https://www.binance.com/en/support/announcement/rss'

KEYWORDS = [
    'will list', 'perpetual', 'futures', 'spot listing', 'launch', 'usdt-m'
]

seen_titles = set()
app = Flask(__name__)


def send_telegram_alert(text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': text}
    requests.post(url, data=data)


def check_binance():
    while True:
        feed = feedparser.parse(BINANCE_RSS)
        for entry in feed.entries:
            title = entry.title.lower()
            if title not in seen_titles and any(k in title for k in KEYWORDS):
                seen_titles.add(title)
                print(f"[NEW] {entry.title}")
                send_telegram_alert(
                    f"🚨 Binance Alert:\n{entry.title}\n{entry.link}")
        time.sleep(60)  # check every 60 seconds


@app.route('/')
def home():
    return "✅ Binance Alert Bot is running!"


# === Start thread and Flask server ===
if __name__ == '__main__':
    threading.Thread(target=check_binance).start()
    app.run(host='0.0.0.0', port=8080)
