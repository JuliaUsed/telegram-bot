from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random
import os
import asyncio

# Get token from environment variables
TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TOKEN:
    raise ValueError("Please set the TELEGRAM_TOKEN secret in the Secrets tab")

# Данные
quotes = [
    "You are free. You can fly anywhere and be anything you want. Your limits are only in your mind. — Richard Bach, Jonathan Livingston Seagull",
    "The only true law is the one that leads to freedom. — Richard Bach, Jonathan Livingston Seagull",
    ...
]

# Функции для бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Я бот.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
