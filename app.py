from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio
import os
from config import BOT_TOKEN

app = Flask(__name__)
application = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Бот тендеров ЕИС 44-ФЗ/223-ФЗ готов!\n\n"
        "📋 Команды:\n"
        "/tenders - свежие тендеры\n"
        "/regions - выбор региона\n"
        "/help - справка"
    )

application.add_handler(CommandHandler("start", start))

@app.route('/', methods=['POST'])
def webhook():
    """Правильная webhook обработка для Render"""
    if not request.is_json:
        return 'OK', 200
    
    update = Update.de_json(request.get_json(), application.bot)
    if update:
        # Правильный способ: в event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(application.process_update(update))
        loop.close()
    
    return 'OK', 200

@app.route('/health', methods=['GET'])
def health():
    return 'Bot alive!', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
