import os
import logging
import threading
import time
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot Token - BotFather'dan olinadi
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Admin chat ID - buyurtmalar shu yerga keladi
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "YOUR_ADMIN_CHAT_ID")

# Web server - Render uchun (port ochiq bo'lishi kerak)
PORT = int(os.environ.get("PORT", 10000))
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://wif-optik.onrender.com")

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"WiF Optik Bot is running!")
    def log_message(self, format, *args):
        pass

def run_web_server():
    server = HTTPServer(('0.0.0.0', PORT), HealthHandler)
    server.serve_forever()

def keep_alive():
    """Har 10 daqiqada o'ziga ping yuboradi — bot uxlamasligi uchun"""
    while True:
        time.sleep(600)  # 10 daqiqa
        try:
            urllib.request.urlopen(RENDER_URL)
            logger.info("Keep-alive ping yuborildi")
        except Exception as e:
            logger.error(f"Keep-alive xato: {e}")


# Conversation states
ORDER_NAME, ORDER_PHONE, ORDER_ADDRESS, ORDER_SERVICE = range(4)

# ==================== XABARLAR ====================

WELCOME_MESSAGE = """
🌐 *WiF Optik — GPON Internet Xizmati*

Assalomu alaykum! 👋
Xorazm va Urganch bo'ylab tez va sifatli internet xizmati.

Quyidagi tugmalardan birini tanlang:
"""

SERVICES_MESSAGE = """
🛠 *Bizning Xizmatlar:*

📡 *GPON Internet o'rnatish*
└ Tezkor optik internet ulanish

📶 *WiFi Router o'rnatish*
└ Sozlash va konfiguratsiya

🔧 *Internet tuzatish*
└ Muammolarni diagnostika va hal qilish

🏠 *Uy/Ofis tarmoq o'rnatish*
└ To'liq tarmoq infratuzilmasi

🔄 *Router almashtirish*
└ Eski routerni yangisiga almashtirish

📞 Buyurtma berish uchun — /buyurtma yozing
"""

PRICES_MESSAGE = """
💰 *Narxlar:*

📡 GPON ulanish (yangi) — *Kelishiladi*
├ Kabel + O'rnatish
└ Tezlik: 100+ Mbps

📶 WiFi router o'rnatish — *Kelishiladi*
├ Sozlash bilan
└ Kafolat bilan

🔧 Internet tuzatish — *Kelishiladi*
├ Diagnostika
└ Tuzatish

🔌 Kabel tortish (qo'shimcha) — *Kelishiladi*
└ 1 metr uchun

━━━━━━━━━━━━━━━━━
📞 *Aniq narx uchun buyurtma bering!*
Biz sizga 5 daqiqada javob beramiz.

/buyurtma — Buyurtma berish
"""

ABOUT_MESSAGE = """
ℹ️ *Biz haqimizda:*

📡 *WiF Optik* — Xorazm viloyatida GPON internet o'rnatish va WiFi xizmatlari.

✅ *Nega bizni tanlashadi:*

⚡ Tez xizmat — 1 soat ichida kelamiz
💯 Sifatli ishlov
🛡 Kafolat beramiz
💰 Arzon narxlar
🕐 24/7 qo'llab-quvvatlash
📍 Butun Xorazm viloyati

━━━━━━━━━━━━━━━━━
📍 *Hudud:* Xorazm / Urganch
🕐 *Ish vaqti:* Dush-Shan 08:00-20:00
🚨 *Shoshilinch:* 24/7
"""

CONTACT_MESSAGE = """
📞 *Bog'lanish:*

📷 Instagram: @wif_optik
🌐 Sayt: quramboyevumirbek010-rgb.github.io/wif-optik

📍 Xorazm / Urganch

━━━━━━━━━━━━━━━━━
💬 Shu yerda yozing — tez javob beramiz!
Yoki /buyurtma bosing — biz sizga qo'ng'iroq qilamiz.
"""

ORDER_SUCCESS_MESSAGE = """
✅ *Buyurtmangiz qabul qilindi!*

👤 Ism: {name}
📞 Telefon: {phone}
📍 Manzil: {address}
🛠 Xizmat: {service}

━━━━━━━━━━━━━━━━━
⏰ Biz sizga *5 daqiqa* ichida qo'ng'iroq qilamiz!
Rahmat! 🙏
"""

# ==================== HANDLERS ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start buyrug'i"""
    keyboard = [
        [InlineKeyboardButton("🛠 Xizmatlar", callback_data="services"),
         InlineKeyboardButton("💰 Narxlar", callback_data="prices")],
        [InlineKeyboardButton("📞 Buyurtma berish", callback_data="order"),
         InlineKeyboardButton("ℹ️ Biz haqimizda", callback_data="about")],
        [InlineKeyboardButton("📱 Bog'lanish", callback_data="contact")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(
            WELCOME_MESSAGE,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    elif update.callback_query:
        await update.callback_query.message.edit_text(
            WELCOME_MESSAGE,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tugmalar handleri"""
    query = update.callback_query
    await query.answer()
    
    back_button = [[InlineKeyboardButton("⬅️ Orqaga", callback_data="back")]]
    back_markup = InlineKeyboardMarkup(back_button)
    
    if query.data == "services":
        await query.message.edit_text(
            SERVICES_MESSAGE,
            parse_mode='Markdown',
            reply_markup=back_markup
        )
    elif query.data == "prices":
        await query.message.edit_text(
            PRICES_MESSAGE,
            parse_mode='Markdown',
            reply_markup=back_markup
        )
    elif query.data == "about":
        await query.message.edit_text(
            ABOUT_MESSAGE,
            parse_mode='Markdown',
            reply_markup=back_markup
        )
    elif query.data == "contact":
        await query.message.edit_text(
            CONTACT_MESSAGE,
            parse_mode='Markdown',
            reply_markup=back_markup
        )
    elif query.data == "order":
        await query.message.edit_text(
            "📝 *Buyurtma berish*\n\nIsmingizni yozing:",
            parse_mode='Markdown'
        )
        return ORDER_NAME
    elif query.data == "back":
        await start(update, context)


# ==================== BUYURTMA CONVERSATION ====================

async def order_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Buyurtma boshlash"""
    await update.message.reply_text(
        "📝 *Buyurtma berish*\n\n👤 Ismingizni yozing:",
        parse_mode='Markdown'
    )
    return ORDER_NAME


async def order_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ism olish"""
    context.user_data['name'] = update.message.text
    await update.message.reply_text(
        "📞 Telefon raqamingizni yozing:\n\n_Masalan: +998 90 123 45 67_",
        parse_mode='Markdown'
    )
    return ORDER_PHONE


async def order_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Telefon olish"""
    context.user_data['phone'] = update.message.text
    await update.message.reply_text(
        "📍 Manzilingizni yozing:\n\n_Masalan: Urganch, Al-Xorazmiy ko'chasi, 15-uy_",
        parse_mode='Markdown'
    )
    return ORDER_ADDRESS


async def order_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manzil olish"""
    context.user_data['address'] = update.message.text
    
    keyboard = [
        [InlineKeyboardButton("📡 GPON internet o'rnatish", callback_data="s_gpon")],
        [InlineKeyboardButton("📶 WiFi router o'rnatish", callback_data="s_wifi")],
        [InlineKeyboardButton("🔧 Internet tuzatish", callback_data="s_repair")],
        [InlineKeyboardButton("🏠 Uy/Ofis tarmoq o'rnatish", callback_data="s_network")],
        [InlineKeyboardButton("🔄 Router almashtirish", callback_data="s_replace")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🛠 Qaysi xizmat kerak? Tanlang:",
        reply_markup=reply_markup
    )
    return ORDER_SERVICE


async def order_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xizmat tanlash va buyurtmani yakunlash"""
    query = update.callback_query
    await query.answer()
    
    services = {
        "s_gpon": "📡 GPON internet o'rnatish",
        "s_wifi": "📶 WiFi router o'rnatish",
        "s_repair": "🔧 Internet tuzatish",
        "s_network": "🏠 Uy/Ofis tarmoq o'rnatish",
        "s_replace": "🔄 Router almashtirish"
    }
    
    service = services.get(query.data, "Noma'lum")
    context.user_data['service'] = service
    
    # Foydalanuvchiga tasdiqlash
    success_msg = ORDER_SUCCESS_MESSAGE.format(
        name=context.user_data['name'],
        phone=context.user_data['phone'],
        address=context.user_data['address'],
        service=service
    )
    
    await query.message.edit_text(success_msg, parse_mode='Markdown')
    
    # Adminga xabar yuborish
    admin_msg = f"""
🆕 *YANGI BUYURTMA!*

👤 Ism: {context.user_data['name']}
📞 Telefon: {context.user_data['phone']}
📍 Manzil: {context.user_data['address']}
🛠 Xizmat: {service}

👆 Tez qo'ng'iroq qiling!
"""
    
    try:
        if ADMIN_CHAT_ID and ADMIN_CHAT_ID != "YOUR_ADMIN_CHAT_ID":
            await context.bot.send_message(
                chat_id=int(ADMIN_CHAT_ID),
                text=admin_msg,
                parse_mode='Markdown'
            )
    except Exception as e:
        logger.error(f"Admin ga xabar yuborishda xato: {e}")
    
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Buyurtmani bekor qilish"""
    await update.message.reply_text(
        "❌ Buyurtma bekor qilindi.\n\n/start — Bosh menyu",
        parse_mode='Markdown'
    )
    return ConversationHandler.END


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yordam"""
    help_text = """
🤖 *Bot buyruqlari:*

/start — Bosh menyu
/xizmatlar — Xizmatlar ro'yxati
/narxlar — Narxlar
/buyurtma — Buyurtma berish
/aloqa — Bog'lanish
/yordam — Yordam

━━━━━━━━━━━━━━━━━
💬 Yoki shunchaki yozing — biz javob beramiz!
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def services_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xizmatlar"""
    await update.message.reply_text(SERVICES_MESSAGE, parse_mode='Markdown')


async def prices_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Narxlar"""
    await update.message.reply_text(PRICES_MESSAGE, parse_mode='Markdown')


async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Aloqa"""
    await update.message.reply_text(CONTACT_MESSAGE, parse_mode='Markdown')


async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Noma'lum xabarlar"""
    auto_reply = """
👋 Rahmat yozganingiz uchun!

Men avtomatik bot. Quyidagilardan birini tanlang:

/start — Bosh menyu
/buyurtma — Buyurtma berish
/narxlar — Narxlarni ko'rish

Yoki tez orada operator javob beradi! ⏰
"""
    await update.message.reply_text(auto_reply)
    
    # Adminga bildirishnoma
    try:
        if ADMIN_CHAT_ID and ADMIN_CHAT_ID != "YOUR_ADMIN_CHAT_ID":
            notification = f"💬 Yangi xabar!\n\n👤 {update.message.from_user.first_name}: {update.message.text}"
            await context.bot.send_message(
                chat_id=int(ADMIN_CHAT_ID),
                text=notification
            )
    except Exception as e:
        logger.error(f"Notification error: {e}")


# ==================== MAIN ====================

def main():
    """Botni ishga tushirish"""
    # Web server ishga tushirish (Render uchun)
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    logger.info(f"Web server {PORT} portda ishga tushdi")
    
    # Keep-alive — bot uxlamasligi uchun
    alive_thread = threading.Thread(target=keep_alive, daemon=True)
    alive_thread.start()
    logger.info("Keep-alive ishga tushdi — bot 24/7 ishlaydi")
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Buyurtma conversation handler
    order_conv = ConversationHandler(
        entry_points=[
            CommandHandler("buyurtma", order_start),
            CallbackQueryHandler(order_service, pattern="^s_")
        ],
        states={
            ORDER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_name)],
            ORDER_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_phone)],
            ORDER_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_address)],
            ORDER_SERVICE: [CallbackQueryHandler(order_service, pattern="^s_")]
        },
        fallbacks=[CommandHandler("cancel", cancel), CommandHandler("start", start)]
    )
    
    # Handlers
    app.add_handler(order_conv)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("yordam", help_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("xizmatlar", services_command))
    app.add_handler(CommandHandler("narxlar", prices_command))
    app.add_handler(CommandHandler("aloqa", contact_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_message))
    
    # Bot ishga tushadi
    logger.info("Bot ishga tushdi! ✅")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
