from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random
import os
import asyncio

TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("Please set the TELEGRAM_TOKEN secret in the Variables/Secrets tab")

quotes = [
    "You are free. You can fly anywhere and be anything you want. Your limits are only in your mind. — Richard Bach, Jonathan Livingston Seagull",
    "The only true law is the one that leads to freedom. — Richard Bach, Jonathan Livingston Seagull",
    "The gull that sees farther flies higher. — Richard Bach, Jonathan Livingston Seagull",
    "Your only obligation in life is to be true to yourself. — Richard Bach, Jonathan Livingston Seagull",
    "Perfection knows no limits. Once you reach one height, you see new, even higher ones. — Richard Bach, Jonathan Livingston Seagull",
    "Freedom is the ability to make a choice without looking back at fear or doubt. — Richard Bach, Jonathan Livingston Seagull",
    "The path to truth always goes through doubts. — Richard Bach, Jonathan Livingston Seagull",
    "Every seagull knows deep down that it was born to fly. — Richard Bach, Jonathan Livingston Seagull",
]

memes = [
    "https://i.postimg.cc/GhBMrcBs/IMG-3098.jpg",
    "https://i.postimg.cc/BvJc8svp/IMG-3096.jpg",
    "https://i.postimg.cc/23pnCNJ4/IMG-3095.jpg",
    "https://i.postimg.cc/wBWfg3kL/IMG-3080.jpg",
    "https://i.postimg.cc/FRLj8KC9/IMG-3078.jpg",
    "https://i.postimg.cc/Mpp1x533/IMG-3077.jpg",
]

beach_coordinates = [
    "-8.705139, 115.172136 📍",
    "-8.725354, 115.164565 📍",
    "-8.808482, 115.146652 📍",
    "-8.829246, 115.087490 📍",
    "-8.671686, 115.128072 📍",
]

def menu_markup() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🎉 Посмотреть поздравление", callback_data="congratulation")],
        [InlineKeyboardButton("😋😋😋 meme", callback_data="meme")],
        [InlineKeyboardButton("🎥 гадаем на книжках", callback_data="wisdom")],
        [InlineKeyboardButton("🎁 Ваш подарок", callback_data="gift")],
        [InlineKeyboardButton("⚡️ Удариться током", callback_data="shock")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def show_menu_message(chat_message) -> None:
    await chat_message.reply_text("Выбери действие:", reply_markup=menu_markup())

async def show_menu_from_query(query) -> None:
    await query.message.reply_text("Выбери действие:", reply_markup=menu_markup())

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await show_menu_message(update.message)

async def congratulation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("номер знаешь")
    await show_menu_from_query(query)

async def meme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    meme_url = random.choice(memes)
    await query.message.reply_photo(photo=meme_url)
    await show_menu_from_query(query)

async def wisdom(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    quote = random.choice(quotes)
    await query.edit_message_text(f"это все будто о тебе:\n\n“{quote}”")
    await show_menu_from_query(query)

async def gift(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("я", callback_data="smile_response")],
        [InlineKeyboardButton("а сама то))))", callback_data="smile_response")],
    ]
    await query.edit_message_text(
        "А кто это тут у нас улыбается?))))",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def smile_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton("выбирай, где получить)))", callback_data="beach_coordinates")]]
    await query.edit_message_text(
        "выбирай, где получить)))",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def beach_coordinates_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Секундочку, выбираю лучшие пляжи...")

    for coord in beach_coordinates:
        await asyncio.sleep(0.7)
        await query.message.reply_text(coord)

    await show_menu_from_query(query)

async def shock(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    message_text = (
        "⚡️ Представь, как мы слегка пьяненькие в ресторане, спустя много тостов, поздравлений и шуток, "
        "встаем танцевать, услышав знакомый мотив, я смотрю тебе в глаза и поздравляю с твоим днем, только на другом языке, а не пайтоне))\n\n"
        "🎵 Слушай трек здесь: https://music.yandex.ru/album/4334256/track/463836?utm_medium=copy_link"
    )
    await query.edit_message_text(message_text)
    await show_menu_from_query(query)

def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(congratulation, pattern="^congratulation$"))
    app.add_handler(CallbackQueryHandler(meme, pattern="^meme$"))
    app.add_handler(CallbackQueryHandler(wisdom, pattern="^wisdom$"))
    app.add_handler(CallbackQueryHandler(gift, pattern="^gift$"))
    app.add_handler(CallbackQueryHandler(smile_response, pattern="^smile_response$"))
    app.add_handler(CallbackQueryHandler(beach_coordinates_handler, pattern="^beach_coordinates$"))
    app.add_handler(CallbackQueryHandler(shock, pattern="^shock$"))

    app.run_polling()

if __name__ == "__main__":
    main()
