import os, requests, urllib.parse
from datetime import datetime
TOKEN = os.getenv("TELEGRAM_TOKEN", "")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=20)
        print(f"TELEGRAM_OK {r.text[:200]}")
    except Exception as e:
        print(f"TELEGRAM_FAIL {e}")
        print(msg[:1000])

msg = f"🔔 مناقصة {datetime.now().strftime('%H:%M')} - AADL\n📍 الجزائر\n🏭 مصنع أثاث - https://www.google.com/maps/search/?api=1&query={urllib.parse.quote('Zone Industrielle Alger')}"
print("BOT_NEW_VERSION_TELEGRAM")
send(msg)
