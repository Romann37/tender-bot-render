from flask import Flask, request, jsonify
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import BOT_TOKEN

# Логирование для отладки
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    try:
        # Проверяем JSON
        if not request.is_json:
            return 'OK', 200
        
        json_data = request.get_json()
        logger.info(f"Received update: {json_data}")
        
        # Создаем Update объект
        update = Update.de_json(json_data, application.bot)
        if update and update.to_dict():
            # Запускаем обработку в новом event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(application.process_update(update))
            loop.close()
        
        return 'OK', 200
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return 'ERROR', 500

@app.route('/health', methods=['GET'])
def health():
    return 'Bot alive!', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
   
