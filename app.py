from flask import Flask, request
import logging
import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes  # ← ВСЁ ЗДЕСЬ!
from config import BOT_TOKEN

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаём Application
application = Application.builder().token(BOT_TOKEN).build()

# Handler функция
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Бот тендеров ЕИС 44-ФЗ/223-ФЗ готов!\n\n"
        "/tenders - свежие тендеры\n"
        "/regions - регионы\n"
        "/help - справка"
    )

# Регистрируем handler
application.add_handler(CommandHandler("start", start))

@app.route('/', methods=['POST'])
def webhook():
    try:
        json_data = request.get_json()
        logger.info(f"Webhook data: {json_data.get('message', {}).get('text', 'no text')}")
        
        if json_data:
            # Создаём и обрабатываем Update
            update = Update.de_json(json_data, application.bot)
            if update:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(application.process_update(update))
                loop.close()
        
        return 'OK', 200
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return 'OK', 200  # Всегда 200 для Telegram!

@app.route('/', methods=['GET'])
def index():
    return 'Bot webhook ready!'

@app.route('/health', methods=['GET'])
def health():
    return 'Bot alive!', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)

   
