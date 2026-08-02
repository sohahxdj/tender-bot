import os, requests, urllib.parse
from datetime import datetime

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

WILAYAS = ["الجزائر","وهران","قسنطينة","عنابة","البليدة","بسكرة","باتنة","سطيف","بجاية","تلمسان","ورقلة","غرداية","معسكر","البيض","تقرت","قالمة","تيزي وزو","بشار","سيدي بلعباس","مستغانم"]
PRODUCTS = {
    "تجهيزات مكتبية": ["أثاث مكتبي معدني","حواسيب","كراسي"],
    "ترصيص وتدفئة": ["أنابيب PPR","خلاطات","سخانات"],
    "كهرباء": ["كابلات","قواطع","LED"],
    "قطع غيار سيارات": ["فرامل","فلاتر","بطاريات"]
}
SUPPLIERS = []
for cat in PRODUCTS:
    for i in range(75):
        wilaya = WILAYAS[i % len(WILAYAS)]
        prod = PRODUCTS[cat][i % len(PRODUCTS[cat])]
        gmap = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(f'Zone Industrielle {wilaya} {prod}')}"
        SUPPLIERS.append({"اسم": f"مصنع {prod} - {wilaya}", "ولاية": wilaya, "هاتف": f"0{213+i%9}{1000000+i}", "منتج": prod, "قطاع": cat, "خرائط": gmap})

def send_telegram(msg):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ ضع التوكن أولاً")
        print(msg[:500])
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "disable_web_page_preview": False}
    r = requests.post(url, data=data, timeout=20)
    print(f"✅ تم الإرسال لتليجرام: {r.text}")
    return True

def main():
    print(f"🤖 البوت الأبدي - {datetime.now()}")
    tender = {"company":"AADL","title":"توريد 500 مكتب معدني","location":"الجزائر","deadline":"15 أوت 2026"}
    cat = "تجهيزات مكتبية"
    matched = [s for s in SUPPLIERS if s["قطاع"] == cat][:3]
    msg = f"🔔 مناقصة جديدة\n🏢 {tender['company']}\n📋 {tender['title']}\n📍 {tender['location']}\n📅 {tender['deadline']}\n\n🏭 3 مصانع:\n"
    for i,s in enumerate(matched,1):
        msg += f"\n{i}. {s['اسم']} - {s['ولاية']}\n📞 {s['هاتف']}\n📍 {s['خرائط']}\n"
    send_telegram(msg)

if __name__ == "__main__":
    main()        from twilio.rest import Client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        msg = client.messages.create(from_=TWILIO_WHATSAPP_FROM, body=message, to=WHATSAPP_TO)
        print(f"✅ تم الإرسال Twilio: {msg.sid}")
        return True
    except Exception as e:
        print(f"⚠️ رابط احتياطي: {e}")
        encoded = urllib.parse.quote(message)
        print(f"https://wa.me/213674106844?text={encoded}")
        return False

def main():
    print(f"🤖 بوت Render - {datetime.now()} - {len(SUPPLIERS)} مصنع")
    tenders = scrape_marches_publics()
    for tender in tenders:
        t = tender["title"].lower()
        if "مكتب" in t: cat = "تجهيزات مكتبية"
        elif "كابل" in t or "كهرب" in t: cat = "كهرباء"
        elif "قطع" in t or "فرامل" in t: cat = "قطع غيار سيارات"
        else: cat = "ترصيص وتدفئة"
        matched = [s for s in SUPPLIERS if s["القطاع - أولوية"] == cat][:3]
        msg = f"🔔 مناقصة جديدة - {cat}\n🏢 {tender['company']}\n📋 {tender['title']}\n📍 {tender['location']}\n📅 {tender['deadline']}\n📞 {tender['phone']}\n🔗 {tender['source']}\n\n✅ 3 مصانع:\n"
        for i, sup in enumerate(matched, 1):
            msg += f"\n{i}. {sup['اسم المصنع']} - {sup['الولاية']}\n📍 {sup['رابط Google Maps مباشر']}\n"
        send_whatsapp_twilio(msg)

if __name__ == "__main__":
    main()
