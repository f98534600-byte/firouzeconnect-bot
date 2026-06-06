import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ==========================================
#   تنظیمات اصلی ربات - اینجا را ویرایش کن
# ==========================================

TOKEN = "توکن_ربات_خودت_را_اینجا_بگذار"   # توکن از BotFather
SUPPORT_ID = "@FirouzeConnect_support"       # آیدی پشتیبانی
CHANNEL_LINK = "https://t.me/FirouzeConnect" # لینک کانال رسمی
ADMIN_ID = 123456789  # آیدی عددی ادمین (برای دریافت درخواست‌ها)

# ==========================================
#   فایل تست رایگان
# ==========================================
# مسیر فایل تست رایگان روی سرور یا file_id تلگرام
FREE_TEST_FILE = "free_test.txt"  # نام فایل تست را اینجا بگذار

# ==========================================

bot = telebot.TeleBot(TOKEN)


# ─── منوی اصلی ───────────────────────────
def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📥 دریافت تست رایگان", callback_data="free_test"),
        InlineKeyboardButton("💎 دریافت اشتراک", callback_data="subscription"),
        InlineKeyboardButton("📲 دانلود برنامه‌ها", callback_data="download"),
        InlineKeyboardButton("💰 تعرفه‌ها", callback_data="prices"),
        InlineKeyboardButton("📚 آموزش اتصال", callback_data="tutorial"),
        InlineKeyboardButton("🎧 پشتیبانی", callback_data="support"),
    )
    markup.add(
        InlineKeyboardButton("📢 کانال رسمی", url=CHANNEL_LINK)
    )
    return markup


# ─── دکمه بازگشت به منو ──────────────────
def back_button():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 بازگشت به منو", callback_data="back_main"))
    return markup


# ─── منوی دانلود برنامه‌ها ───────────────
def download_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🤖 Android", callback_data="dl_android"),
        InlineKeyboardButton("🍎 iOS", callback_data="dl_ios"),
        InlineKeyboardButton("💻 Windows", callback_data="dl_windows"),
        InlineKeyboardButton("🏪 Google Play", callback_data="dl_googleplay"),
    )
    markup.add(InlineKeyboardButton("🔙 بازگشت به منو", callback_data="back_main"))
    return markup


# =========================================
#   هندلر /start
# =========================================
@bot.message_handler(commands=["start"])
def start(message):
    name = message.from_user.first_name or "کاربر"
    text = (
        f"👋 سلام {name} عزیز!\n\n"
        "به ربات رسمی *FirouzeConnect* خوش اومدی 🌐\n\n"
        "از منوی زیر گزینه موردنظرت رو انتخاب کن 👇"
    )
    bot.send_message(
        message.chat.id,
        text,
        parse_mode="Markdown",
        reply_markup=main_menu()
    )


# =========================================
#   هندلر دکمه‌های شیشه‌ای
# =========================================
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    msg_id = call.message.message_id

    bot.answer_callback_query(call.id)

    # ─── تست رایگان ─────────────────────
    if call.data == "free_test":
        text = (
            "📥 *تست رایگان VPN*\n\n"
            "فایل تست رایگان برای شما ارسال می‌شه.\n"
            "⏳ لطفاً چند لحظه صبر کنید..."
        )
        bot.edit_message_text(text, chat_id, msg_id,
                              parse_mode="Markdown", reply_markup=back_button())
        try:
            with open(FREE_TEST_FILE, "rb") as f:
                bot.send_document(chat_id, f, caption="✅ فایل تست رایگان شما")
        except Exception:
            bot.send_message(
                chat_id,
                "⚠️ در حال حاضر فایل تست موجود نیست.\n"
                f"لطفاً با پشتیبانی تماس بگیرید: {SUPPORT_ID}"
            )
        # اطلاع به ادمین
        try:
            user = call.from_user
            bot.send_message(
                ADMIN_ID,
                f"📥 درخواست تست رایگان\n"
                f"👤 نام: {user.first_name}\n"
                f"🆔 یوزرنیم: @{user.username}\n"
                f"🔢 آیدی: {user.id}"
            )
        except Exception:
            pass

    # ─── دریافت اشتراک ───────────────────
    elif call.data == "subscription":
        text = (
            "💎 *دریافت اشتراک*\n\n"
            "برای خرید اشتراک و دریافت کانفیگ اصلی،\n"
            "لطفاً با پشتیبانی ما در ارتباط باشید:\n\n"
            f"👤 {SUPPORT_ID}\n\n"
            "⚡️ پس از تأیید پرداخت، کانفیگ شما ارسال می‌شه."
        )
        bot.edit_message_text(text, chat_id, msg_id,
                              parse_mode="Markdown", reply_markup=back_button())

    # ─── دانلود برنامه‌ها ─────────────────
    elif call.data == "download":
        text = (
            "📲 *دانلود برنامه‌ها*\n\n"
            "سیستم‌عامل خود را انتخاب کنید:"
        )
        bot.edit_message_text(text, chat_id, msg_id,
                              parse_mode="Markdown", reply_markup=download_menu())

    elif call.data == "dl_android":
        text = (
            "🤖 *دانلود برای Android*\n\n"
            "برنامه پیشنهادی: V2rayNG\n"
            "🔗 لینک دانلود مستقیم:\n"
            "https://github.com/2dust/v2rayNG/releases\n\n"
            "📌 بعد از نصب، کانفیگ خود را وارد کنید."
        )
        bot.edit_message_text(text, chat_id, msg_id,
                              parse_mode="Markdown", reply_markup=back_button())

    elif call.data == "dl_ios":
        text = (
            "🍎 *دانلود برای iOS*\n\n"
            "برنامه پیشنهادی: Streisand\n"
            "🔗 App Store:\n"
            "https://apps.apple.com/app/streisand/id6450534064\n\n"
            "📌 بعد از نصب، کانفیگ خود را وارد کنید."
        )
        bot.edit_message_text(text, chat_id, msg_id,
                              parse_mode="Markdown", reply_markup=back_button())

    elif call.data == "dl_windows":
        text = (
            "💻 *دانلود برای Windows*\n\n"
            "برنامه پیشنهادی: v2rayN\n"
            "🔗 لینک دانلود:\n"
            "https://github.com/2dust/v2rayN/releases\n\n"
            "📌 بعد از نصب، کانفیگ خود را وارد کنید."
        )
        bot.edit_message_text(text, chat_id, msg_id,
                              parse_mode="Markdown", reply_markup=back_button())

    elif call.data == "dl_googleplay":
        text = (
            "🏪 *Google Play*\n\n"
            "برنامه V2rayNG در Google Play:\n"
            "🔗 https://play.google.com/store/apps/details?id=com.v2ray.ang\n\n"
            "📌 بعد از نصب، کانفیگ خود را وارد کنید."
        )
        bot.edit_message_text(text, chat_id, msg_id,
                              parse_mode="Markdown", reply_markup=back_button())

    # ─── تعرفه‌ها ─────────────────────────
    elif call.data == "prices":
        text = (
            "💰 *تعرفه‌های اشتراک FirouzeConnect*\n\n"
            "━━━━━━━━━━━━━━━━\n"
            "🔹 *پلن ۱ ماهه*\n"
            "   قیمت: [قیمت را اینجا وارد کن]\n\n"
            "🔹 *پلن ۳ ماهه*\n"
            "   قیمت: [قیمت را اینجا وارد کن]\n\n"
            "🔹 *پلن ۶ ماهه*\n"
            "   قیمت: [قیمت را اینجا وارد کن]\n\n"
            "🔹 *پلن ۱ ساله*\n"
            "   قیمت: [قیمت را اینجا وارد کن]\n"
            "━━━━━━━━━━━━━━━━\n"
            f"📩 برای خرید: {SUPPORT_ID}"
        )
        bot.edit_message_text(text, chat_id, msg_id,
                              parse_mode="Markdown", reply_markup=back_button())

    # ─── آموزش اتصال ─────────────────────
    elif call.data == "tutorial":
        text = (
            "📚 *آموزش اتصال VPN*\n\n"
            "━━━━━━━━━━━━━━━━\n"
            "🤖 *Android:*\n"
            "1. برنامه V2rayNG را نصب کنید\n"
            "2. روی + بزنید\n"
            "3. گزینه Import config from clipboard را انتخاب کنید\n"
            "4. کانفیگ خود را paste کنید\n"
            "5. دکمه اتصال را بزنید\n\n"
            "🍎 *iOS:*\n"
            "1. برنامه Streisand را نصب کنید\n"
            "2. لینک کانفیگ را باز کنید\n"
            "3. Add to Streisand را بزنید\n"
            "4. Connect را بزنید\n\n"
            "💻 *Windows:*\n"
            "1. برنامه v2rayN را نصب کنید\n"
            "2. از سرورها، Add Server را بزنید\n"
            "3. کانفیگ را paste کنید\n"
            "4. Set as active server را بزنید\n"
            "━━━━━━━━━━━━━━━━\n"
            f"❓ سوال دارید؟ {SUPPORT_ID}"
        )
        bot.edit_message_text(text, chat_id, msg_id,
                              parse_mode="Markdown", reply_markup=back_button())

    # ─── پشتیبانی ────────────────────────
    elif call.data == "support":
        text = (
            "🎧 *پشتیبانی FirouzeConnect*\n\n"
            "برای ارتباط با تیم پشتیبانی:\n\n"
            f"👤 {SUPPORT_ID}\n\n"
            "🕐 ساعات پاسخگویی:\n"
            "شنبه تا پنجشنبه | ۹ صبح تا ۱۱ شب\n\n"
            "⚡️ معمولاً در کمتر از ۱ ساعت پاسخ می‌دهیم."
        )
        bot.edit_message_text(text, chat_id, msg_id,
                              parse_mode="Markdown", reply_markup=back_button())

    # ─── بازگشت به منو ───────────────────
    elif call.data == "back_main":
        text = (
            "🏠 *منوی اصلی FirouzeConnect*\n\n"
            "یکی از گزینه‌ها رو انتخاب کن 👇"
        )
        bot.edit_message_text(text, chat_id, msg_id,
                              parse_mode="Markdown", reply_markup=main_menu())


# =========================================
#   اجرای ربات
# =========================================
print("✅ ربات FirouzeConnect در حال اجراست...")
bot.infinity_polling()
