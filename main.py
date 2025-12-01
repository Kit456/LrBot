import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import asyncio

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен из переменных окружения Railway
TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Проверка токена
if not TOKEN:
    logger.error("❌ Токен не найден! Проверьте переменную TELEGRAM_TOKEN в Railway")
    exit(1)

logger.info(f"✅ Токен получен, начинаю: {TOKEN[:10]}...")

# Серверы
SERVERS = [
    {"id": 0, "name": "🇷🇺 Москва", "lang": "Русский", "url": "https://liverussia.online/app/join/0"},
    {"id": 1, "name": "🇷🇺 Севастополь", "lang": "Русский", "url": "https://liverussia.online/app/join/1"},
    {"id": 2, "name": "🇬🇧 Continental", "lang": "Английский", "url": "https://liverussia.online/app/join/2"},
    {"id": 3, "name": "🇬🇧 Babylon", "lang": "Английский", "url": "https://liverussia.online/app/join/3"}
]

# Команда /start
async def start(update: Update, context):
    """Главное меню"""
    keyboard = [
        [InlineKeyboardButton("🇷🇺 Русские серверы", callback_data='ru')],
        [InlineKeyboardButton("🇬🇧 Английские серверы", callback_data='en')],
        [InlineKeyboardButton("📋 Инструкция", callback_data='help')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🚀 *Быстрый вход в Liverussia*\n\nВыберите опцию:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# Обработка кнопок
async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'ru':
        keyboard = [
            [InlineKeyboardButton("🇷🇺 Москва (ID: 0)", callback_data='server_0')],
            [InlineKeyboardButton("🇷🇺 Севастополь (ID: 1)", callback_data='server_1')],
            [InlineKeyboardButton("🔙 Назад", callback_data='back')]
        ]
        await query.edit_message_text(
            "🇷🇺 *Русские серверы:*\nВыберите сервер:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    elif query.data == 'en':
        keyboard = [
            [InlineKeyboardButton("🇬🇧 Continental (ID: 2)", callback_data='server_2')],
            [InlineKeyboardButton("🇬🇧 Babylon (ID: 3)", callback_data='server_3')],
            [InlineKeyboardButton("🔙 Назад", callback_data='back')]
        ]
        await query.edit_message_text(
            "🇬🇧 *Английские серверы:*\nВыберите сервер:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    elif query.data.startswith('server_'):
        server_id = int(query.data.split('_')[1])
        server = SERVERS[server_id]
        
        keyboard = [
            [InlineKeyboardButton("🚀 Перейти на сервер", url=server['url'])],
            [InlineKeyboardButton("🔙 Назад", callback_data='ru' if server_id < 2 else 'en')]
        ]
        
        await query.edit_message_text(
            f"*{server['name']}*\n\n"
            f"• ID: `{server['id']}`\n"
            f"• Язык: {server['lang']}\n\n"
            f"Нажмите кнопку ниже:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    elif query.data == 'help':
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='back')]]
        await query.edit_message_text(
            "📋 *Инструкция:*\n\n"
            "1. Выберите сервер\n"
            "2. Нажмите 'Перейти на сервер'\n"
            "3. В браузере: 'Открыть в приложении'\n"
            "4. Игра запустится автоматически\n\n"
            "⚠ *Игра должна быть установлена!*",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    elif query.data == 'back':
        keyboard = [
            [InlineKeyboardButton("🇷🇺 Русские серверы", callback_data='ru')],
            [InlineKeyboardButton("🇬🇧 Английские серверы", callback_data='en')],
            [InlineKeyboardButton("📋 Инструкция", callback_data='help')]
        ]
        await query.edit_message_text(
            "🚀 *Главное меню*\n\nВыберите опцию:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

# Главная функция
async def main():
    """Запуск бота"""
    logger.info("🔄 Создаю приложение...")
    
    try:
        application = Application.builder().token(TOKEN).build()
        
        # Обработчики
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button_handler))
        
        logger.info("✅ Бот запускается...")
        await application.run_polling()
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        raise

# Запуск
if __name__ == "__main__":
    asyncio.run(main())
