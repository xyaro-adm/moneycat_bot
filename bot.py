import os
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
from image_generator import generate_image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
ADMIN_IDS = list(map(int, os.environ["ADMIN_IDS"].split(",")))
WEBHOOK_URL = os.environ["WEBHOOK_URL"]

user_sessions = {}

RATE_LABELS = [
    "RUB/CNY Нал",
    "RUB/CNY Карта",
    "USDT/CNY",
    "RUB/USDT",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    await update.message.reply_text("Привет! Отправь /rates чтобы начать ввод курсов.")

async def rates_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    user_id = update.effective_user.id
    user_sessions[user_id] = []
    await update.message.reply_text(
        f"Введи курс *{RATE_LABELS[0]}*:",
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        return

    if user_id not in user_sessions:
        await update.message.reply_text("Начни с команды /rates")
        return

    text = update.message.text.strip()

    try:
        float(text.replace(",", "."))
    except ValueError:
        await update.message.reply_text("Введи число, например: 11.6")
        return

    session = user_sessions[user_id]
    session.append(text.replace(",", "."))

    if len(session) < 4:
        next_label = RATE_LABELS[len(session)]
        await update.message.reply_text(
            f"Введи курс *{next_label}*:",
            parse_mode="Markdown"
        )
    else:
        rates = session[:]
        today = datetime.now()
        months = ["Янв","Фев","Мар","Апр","Май","Июн",
                  "Июл","Авг","Сен","Окт","Ноя","Дек"]
        date_str = f"{today.day:02d} {months[today.month - 1]}"

        await update.message.reply_text("⏳ Генерирую картинку...")

        try:
            img_bytes = generate_image(rates, date_str)
        except Exception as e:
            logger.error(f"Image generation error: {e}")
            await update.message.reply_text(f"Ошибка генерации: {e}")
            del user_sessions[user_id]
            return

        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "📢 Опубликовать в канал",
                callback_data=f"publish|{'|'.join(rates)}|{date_str}"
            )
        ]])

        await update.message.reply_photo(
            photo=img_bytes,
            caption="Проверь курсы и опубликуй в канал 👆",
            reply_markup=keyboard
        )
        del user_sessions[user_id]

async def publish_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id not in ADMIN_IDS:
        return

    data = query.data.split("|")
    rates = data[1:5]
    date_str = data[5]

    try:
        img_bytes = generate_image(rates, date_str)
    except Exception as e:
        await query.edit_message_caption(f"Ошибка: {e}")
        return

    channel_keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("Начать обмен", url="https://t.me/moneycat_exchange")
    ]])
    await context.bot.send_photo(chat_id=CHANNEL_ID, photo=img_bytes, reply_markup=channel_keyboard)
    await query.edit_message_caption("✅ Опубликовано в канал!")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rates", rates_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(publish_callback, pattern="^publish"))

    port = int(os.environ.get("PORT", 8080))

    # PTB 21.x — run_webhook синхронный, не awaitable
    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        webhook_url=f"{WEBHOOK_URL}/webhook",
        url_path="/webhook",
    )

if __name__ == "__main__":
    main()
