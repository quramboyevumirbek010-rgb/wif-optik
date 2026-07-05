# 🤖 WiF Optik Telegram Bot — Qo'llanma

## Bot nimalar qiladi:
- ✅ Xizmatlarni ko'rsatadi
- ✅ Narxlarni ko'rsatadi
- ✅ Buyurtma qabul qiladi (ism, telefon, manzil, xizmat turi)
- ✅ Sizga (admin) buyurtma haqida xabar yuboradi
- ✅ 24/7 avtomatik ishlaydi
- ✅ Foydalanuvchi yozsa — avtomatik javob beradi va sizga bildirishnoma keladi

---

## 🔧 BOT YARATISH (1 marta qilasiz):

### 1-qadam: BotFather'da bot yaratish
1. Telegram'da @BotFather oching
2. `/newbot` yozing
3. Bot nomi: `WiF Optik Bot`
4. Username: `wif_optik_bot`
5. BotFather sizga TOKEN beradi — SAQLANG!

### 2-qadam: Admin Chat ID olish
1. Telegram'da @userinfobot oching
2. `/start` bosing
3. U sizga `Id:` raqamini ko'rsatadi — SAQLANG!
   (Masalan: 123456789)

---

## 🚀 BOTNI ISHGA TUSHIRISH (Render.com — BEPUL):

### 1-qadam: Render.com'ga ro'yxatdan o'ting
1. https://render.com ga boring
2. GitHub bilan ro'yxatdan o'ting

### 2-qadam: Yangi servis yarating
1. "New +" bosing → "Background Worker"
2. GitHub repo tanlang: `wif-optik`
3. Sozlamalar:
   - Name: `wif-optik-bot`
   - Root Directory: `bot`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`

### 3-qadam: Environment Variables (muhim!)
1. "Environment" bo'limida qo'shing:
   - `BOT_TOKEN` = BotFather'dan olgan tokeningiz
   - `ADMIN_CHAT_ID` = @userinfobot dan olgan ID raqamingiz

### 4-qadam: Deploy
1. "Create Background Worker" bosing
2. 1-2 daqiqa kutib — bot ishlaydi!

---

## 📱 BOT BUYRUQLARI:

| Buyruq | Nima qiladi |
|--------|-------------|
| /start | Bosh menyu |
| /xizmatlar | Xizmatlar ro'yxati |
| /narxlar | Narxlar |
| /buyurtma | Buyurtma berish |
| /aloqa | Bog'lanish ma'lumotlari |
| /yordam | Barcha buyruqlar |

---

## 🔄 BUYURTMA JARAYONI:

1. Mijoz /buyurtma bosadi
2. Bot ismini so'raydi
3. Bot telefon raqamini so'raydi
4. Bot manzilini so'raydi
5. Bot xizmat turini so'raydi (tugmalar bilan)
6. Buyurtma qabul qilindi — mijozga tasdiqlash keladi
7. **SIZGA** (admin) buyurtma haqida xabar keladi!
8. Siz mijozga qo'ng'iroq qilasiz

---

## ❓ MUAMMOLAR:

**Bot ishlamayapti:**
- Token to'g'riligini tekshiring
- Render.com'da "Logs" bo'limini ko'ring

**Buyurtma kelmayapti:**
- ADMIN_CHAT_ID to'g'riligini tekshiring (@userinfobot'dan)

**Bot sekin javob beryapti:**
- Bepul rejada shunday — 1-2 sekund normal

---

Muvaffaqiyat! 🚀
