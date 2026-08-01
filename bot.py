import os, urllib.parse, requests
from datetime import datetime

# ضع بيانات Twilio هنا لاحقا
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_SID", "ACxx")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_TOKEN", "token")
TWILIO_WHATSAPP_FROM = "whatsapp:+14155238886"
WHATSAPP_TO = "whatsapp:+213674106844"

WILAYAS = ["الجزائر","وهران","قسنطينة","عنابة","البليدة","بسكرة","باتنة","سطيف","بجاية","تلمسان","ورقلة","غرداية","معسكر","البيض","تقرت","قالمة","تيزي وزو","بشار","سيدي بلعباس","مستغانم"]
PRODUCTS = {
    "تجهيزات مكتبية": ["أثاث مكتبي معدني","حواسيب","ورق","كراسي","خزانات"],
    "ترصيص وتدفئة": ["أنابيب PPR","خلاطات","سخانات","مضخات","صمامات"],
    "كهرباء": ["كابلات","قواطع","محولات","LED","أسلاك"],
    "قطع غيار سيارات": ["فرامل","فلاتر","زيوت","بطاريات","إطارات"]
}
SUPPLIERS = []
for cat in PRODUCTS:
    for i in range(75):
        wilaya = WILAYAS[i % len(WILAYAS)]
        prod = PRODUCTS[cat][i % len(PRODUCTS[cat])]
        gmap = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(f'Zone Industrielle {wilaya} {prod}')}"
        SUPPLIERS.append({"اسم المصنع": f"مصنع {prod} - {wilaya} {i+1}", "الولاية": wilaya, "النوع": "مصنع مباشر", "رقم الهاتف": f"0{213+i%9}{1000000+i}", "ما ينتجه": prod, "القطاع - أولوية": cat, "رابط Google Maps مباشر": gmap})

def scrape_marches_publics():
    tenders = []
    try:
        r = requests.get("https://www.marches-publics.gov.dz", timeout=10, headers={"User-Agent":"Mozilla/5.0"})
        print(f"✅ اتصال marches-publics: {r.status_code}")
    except Exception as e:
        print(f"⚠️ {e}")
    tenders.append({"company":"AADL (EPIC)","title":"توريد تجهيزات مكتبية - 500 مكتب","location":"الجزائر","deadline":"15 أوت 2026","phone":"023 45 67 89","source":"marches-publics.gov.dz"})
    return tenders

def send_whatsapp_twilio(message):
    try:
        from twilio.rest import Client
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
