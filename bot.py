from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import random
import asyncio

# Получение токена из переменной окружения
TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TOKEN:
    raise ValueError("Please set the TELEGRAM_TOKEN secret in the Secrets tab")

# Данные для работы бота
quotes = [
    "You are free. You can fly anywhere and be anything you want. Your limits are only in your mind. — Richard Bach",
    "The only true law is the one that leads to freedom. — Richard Bach",
    "The gull that sees farther flies higher. — Richard Bach",
    "Your only obligation in life is to be true to yourself. — Richard Bach",
    "Perfection knows no limits. — Richard Bach",
    "Freedom is the ability to make a choice without looking back at fear or doubt. — Richard Bach",
    "The path to truth always goes through doubts. — Richard Bach",
    "Every seagull knows deep down that it was born to fly. — Richard Bach"
]

memes = [
    "https://i.postimg.cc/GhBMrcBs/IMG-3098.jpg",
    "https://i.postimg.cc/BvJc8svp/IMG-3096.jpg",
    "https://i.postimg.cc/23pnCNJ4/IMG-3095.jpg",
    "https://i.postimg.cc/wBWfg3kL/IMG-3080.jpg",
    "https://i.postimg.cc/FRLj8KC9/IMG-3078.jpg",
    "https://i.postimg.cc/Mpp1x533/IMG-3077.jpg"
]

beach_coordinates = [
    "-8.705139, 115.172136 📍",
    "-8.725354, 115.164565 📍",
    "-8.808482, 115.146652 📍",
    "-8.829246, 115.087490 📍",
    "-8.671686, 115.128072 📍"
]

# Функция для отображения главного меню
async def return_to_menu(update: Update) -> None:
    keyboard = [
        [InlineKeyboardButton("🎉 Посмотреть поздравление", callback_data="congratulation")],
        [InlineKeyboardButton("😋 Мем", callback_data="meme")],
        [InlineKeyboardButton("🎥 Гадаем на книжках", callback_data="wisdom")],
        [InlineKeyboardButton("🎁 Ваш подарок", callback_data="gift")],
        [InlineKeyboardButton("⚡️ Удариться током", callback_data="shock")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:  # Для команды /start
        await update.message.reply_text("Выбери действие:", reply_markup=reply_markup)
    elif update.callback_query:  # Для возврата в меню
        await update.callback_query.message.reply_text("Выбери действие:", reply_markup=reply_markup)

# Функция для отображения поздравления
async def congratulation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Номер знаешь 😉")

# Функция для отображения мемов
async def meme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    meme_url = random.choice(memes)
    await query.edit_message_text(text=f"Вот мем для тебя: [Посмотреть мем]({meme_url})", parse_mode="Markdown")

# Функция для отображения мудрых цитат
async def wisdom(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    quote = random.choice(quotes)
    await query.edit_message_text(text=f"Это для тебя:\n\n\"{quote}\"")

# Функция для отображения подарка
async def gift(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("я", callback_data="smile_response")],
        [InlineKeyboardButton("а сама то))", callback_data="smile_response")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="А кто это тут у нас улыбается?))", reply_markup=reply_markup)

# Ответ на улыбку
async def smile_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Выбирай, где получить))", callback_data="beach_coordinates")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Выбирай, где получить))", reply_markup=reply_markup)

# Отображение координат
async def beach_coordinates_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Секундочку, выбираю лучшие пляжи...")
    for coord in beach_coordinates:
        await asyncio.sleep(1)  # Задержка между сообщениями
        await query.message.reply_text(coord)

# Функция для "удариться током"
async def shock(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    message_text = (
        "⚡️ Представь, как мы слегка пьяненькие в ресторане, спустя много тостов, поздравлений и шуток, "
        "встаем танцевать, услышав знакомый мотив. Я смотрю тебе в глаза и поздравляю с твоим днем, только на другом языке, а не пайтоне))\n\n"
        "🎵 Слушай трек здесь: [O Children - Nick Cave & The Bad Seeds](https://music.yandex.ru/album/4334256/track/463836?utm_medium=copy_link)"
    )
    await query.edit_message_text(text=message_text, parse_mode="Markdown")

# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await return_to_menu(update)

# Главная функция запуска
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(congratulation, pattern="congratulation"))
    app.add_handler(CallbackQueryHandler(meme, pattern="meme"))
    app.add_handler(CallbackQueryHandler(wisdom, pattern="wisdom"))
    app.add_handler(CallbackQueryHandler(gift, pattern="gift"))
    app.add_handler(CallbackQueryHandler(smile_response, pattern="smile_response"))
    app.add_handler(CallbackQueryHandler(beach_coordinates_handler, pattern="beach_coordinates"))
    app.add_handler(CallbackQueryHandler(shock, pattern="shock"))

    app.run_polling()

if __name__ == "__main__":
    main()
