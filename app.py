from flask import Flask, request, abort
import telebot
from telebot import types
import os
import logging
from config import BOT_TOKEN

# ВАЖНО: Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    logger.info(f"START команда от {message.from_user.id}")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('🔔 Подписки')
    btn2 = types.KeyboardButton('🔍 Поиск тендеров')
    btn3 = types.KeyboardButton('📊 обследование зданий')
    btn4 = types.KeyboardButton('❓ Помощь')
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.reply_to(message, 
        "🚀 Бот тендеров ЕИС готов!\n\n"
        "👇 Нажмите кнопку:",
        reply_markup=markup)

# 🔥 ЛОВИМ ВСЁ!
@bot.message_handler(func=lambda message: True)
def catch_all(message):
    logger.info(f"Получено сообщение: '{message.text}' от {message.from_user.id}")
    
    text = message.text.lower() if message.text else ""
    
    if 'подписки' in text:
        bot.reply_to(message, "🔔 Подписки работают!")
    elif 'поиск' in text or 'тендеров' in text:
        bot.reply_to(message, "🔍 Поиск работает!")
    elif 'обследование' in text or 'зданий' in text:
        bot.reply_to(message, "🏢 Обследование работает!")
    elif 'помощь' in text:
        bot.reply_to(message, "❓ Помощь работает!")
    else:
        bot.reply_to(message, f"Получил: {message.text}")

@app.route('/', methods=['POST'])
def webhook():
    try:
        logger.info("Webhook POST получен")
        
        if request.headers.get('content-type') == 'application/json':
            json_string = request.get_data().decode('utf-8')
            logger.info(f"JSON: {json_string[:200]}...")
            
            update = telebot.types.Update.de_json(json_string)
            if update:
                logger.info(f"Update: message={update.message.text if update.message else 'None'}")
                bot.process_new_updates([update])
            return '', 200
        else:
            logger.warning(f"Неправильный content-type: {request.headers.get('content-type')}")
            abort(403)
            
    except Exception as e:
        logger.error(f"Webhook ERROR: {e}")
        return 'ERROR', 500

@app.route('/health', methods=['GET'])
def health():
    return 'Bot alive!', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
