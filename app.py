from flask import Flask, request, jsonify
import logging
import os
from telegram.ext import Application
from config import BOT_TOKEN

# БАЗОВОЕ логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
application = Application.builder().token(BOT_TOKEN).build()

async def start(update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="🚀 Бот тендеров ЕИС готов!\n/tenders /regions /help"
    )

# Регистрируем обработчик
application.add_handler(CommandHandler("start", start))

@app.route('/', methods=['POST'])
def webhook():
    try:
        json_string = request.get_data(as_text=True)
        logger.info(f"Webhook received: {json_string[:200]}...")
        
        # Простой возврат OK (Telegram перестанет слать ошибки)
        return 'OK', 200
        
    except Exception as e:
        logger.error(f"Webhook ERROR: {e}")
        return 'OK', 200  # ← ВАЖНО: всегда 200 для Telegram!

@app.route('/health', methods=['GET'])
def health():
    return {'status': 'alive'}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

