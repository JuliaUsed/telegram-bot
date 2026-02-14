import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TOKEN = os.getenv("TELEGRAM_TOKEN")

# -------------------------
# БЛАГОДАРНОСТИ (без повторов)
# -------------------------

THANKS_ALL = [
"Спасибо, что не зассал и написал 🥇",
"Спасибо, что ты всегда говоришь «я рядом», когда это нужно.",
"Спасибо, что ты слышишь меня.",
"Спасибо, что покупаешь голубику и мою любимую водичку.",
"Спасибо за твой мозг и амбиции.",
"Спасибо, что показал мне другую жизнь.",
"Спасибо, что любишь меня. У тебя хороший вкус.",
"Спасибо, что кладёшь носки в корзину (на 70%).",
"Спасибо, что думаешь о будущем. Это секси.",
"Спасибо, что ты это ты. Я люблю тебя.",
"Спасибо, что остаёшься собой.",
"Спасибо за секс посреди ночи 😄",
"Спасибо, что забираешь меня и находишь время за кофе.",
"Спасибо, что почти выкинул ковёр.",
"Спасибо, что целуешь меня в татушки.",
"Спасибо за твою нежность."
]

thanks_bag = THANKS_ALL.copy()

def get_random_thanks():
    global thanks_bag
    if not thanks_bag:
        thanks_bag = THANKS_ALL.copy()
    phrase = random.choice(thanks_bag)
    thanks_bag.remove(phrase)
    return phrase

# -------------------------
# МОМЕНТЫ (вставишь file_id позже)
# -------------------------

LOVE_ALL = [
{
    "photo": "example_id_1",
    "text": "Наш первый вечер. Тогда я поняла, что всё будет по-настоящему."
},
{
    "photo": "example_id_2",
    "text": "Тот день, когда мы устали, но были счастливы."
},
]

love_bag = LOVE_ALL.copy()

def get_random_love():
    global love_bag
    if not love_bag:
        love_bag = LOVE_ALL.copy()
    moment = random.choice(love_bag)
    love_bag.remove(moment)
    return moment

# -------------------------
# МЕНЮ
# -------------------------

def main_menu():
    keyboard = [
        [InlineKeyboardButton("🙏 Сказать спасибо", callback_data="thanks")],
        [InlineKeyboardButton("❤️ Рандомный момент", callback_data="love")],
        [InlineKeyboardButton("📦 Архив", callback_data="archive")],
    ]
    return InlineKeyboardMarkup(keyboard)

def archive_menu():
    keyboard = [
        [InlineKeyboardButton("⚡️ Удариться током", callback_data="shock")],
        [InlineKeyboardButton("🎉 Поздравление", callback_data="congrat")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back")],
    ]
    return InlineKeyboardMarkup(keyboard)

# -------------------------
# ОБРАБОТЧИКИ
# -------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Выбирай 💌", reply_markup=main_menu())

async def thanks_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    phrase = get_random_thanks()
    await query.message.reply_text(phrase)
    await query.message.reply_text("👇", reply_markup=main_menu())

async def love_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    moment = get_random_love()
    await query.message.reply_photo(photo=moment["photo"], caption=moment["text"])
    await query.message.reply_text("👇", reply_markup=main_menu())

async def archive_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Архив старых функций:", reply_markup=archive_menu())

async def back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Выбирай 💌", reply_markup=main_menu())

# Старые функции

async def shock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "⚡️ Представь, как мы слегка пьяненькие в ресторане...\n\n"
        "🎵 O Children — Nick Cave"
    )

async def congrat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("номер знаешь 😉")

# -------------------------
# ВРЕМЕННО: ПОЛУЧЕНИЕ file_id
# -------------------------

async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    await update.message.reply_text(f"Вот твой file_id:\n{photo.file_id}")

# -------------------------
# MAIN
# -------------------------

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(thanks_handler, pattern="thanks"))
    app.add_handler(CallbackQueryHandler(love_handler, pattern="love"))
    app.add_handler(CallbackQueryHandler(archive_handler, pattern="archive"))
    app.add_handler(CallbackQueryHandler(back_handler, pattern="back"))
    app.add_handler(CallbackQueryHandler(shock, pattern="shock"))
    app.add_handler(CallbackQueryHandler(congrat, pattern="congrat"))

    app.add_handler(MessageHandler(filters.PHOTO, get_file_id))

    app.run_polling()

if __name__ == "__main__":
    main()
