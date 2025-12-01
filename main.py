import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import asyncio

# Токен из переменных окружения
TOKEN = os.environ.get("TELEGRAM_TOKEN")

SERVERS = [
    {"id": 0, "name": "🇷🇺 Москва", "url": "https://liverussia.online/app/join/0"},
    {"id": 1, "name": "🇷🇺 Севастополь", "url": "https://liverussia.online/app/join/1"},
    {"id": 2, "name": "🇬🇧 Continental", "url": "https://liverussia.online/app/join/2"},
    {"id": 3, "name": "🇬🇧 Babylon", "url": "https://liverussia.online/app/join/3"}
]

async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("🇷🇺 Москва", callback_data='0')],
        [InlineKeyboardButton("🇷🇺 Севастополь", callback_data='1')],
        [InlineKeyboardButton("🇬🇧 Continental", callback_data='2')],
        [InlineKeyboardButton("🇬🇧 Babylon", callback_data='3')],
        [InlineKeyboardButton("📋 Инструкция", callback_data='help')]
    ]
    
    await update.message.reply_text(
        "🚀 Выберите сервер:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'help':
        await query.edit_message_text(
            "📋 Как использовать:\n\n"
            "1. Выберите сервер\n"
            "2. Нажмите на ссылку\n"
            "3. В браузере: 'Открыть в приложении'\n\n"
            "⚠ Игра должна быть установлена!"
        )
        return
    
    server_id = int(query.data)
    server = SERVERS[server_id]
    
    keyboard = [[InlineKeyboardButton("🚀 Перейти", url=server['url'])]]
    
    await query.edit_message_text(
        f"{server['name']}\nСсылка: {server['url']}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("✅ Бот запущен!")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
