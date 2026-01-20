from flask import Flask, request
import telebot
from telebot import types
import os
import logging
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    logger.info(f"START от {message.from_user.id}")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('🔔 Подписки', '🔍 Поиск тендеров')
    markup.add('📊 обследование зданий', '❓ Помощь')
    
    bot.reply_to(message, "🚀 Бот работает!\n👇 Выберите кнопку:")
    bot.send_message(message.chat.id, "✅ Меню отправлено!", reply_markup=markup)

# Ловим ВСЁ
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    logger.info(f"Сообщение: '{message.text}'")
    
    text = message.text or ""
    chat_id = message.chat.id
    
    # КНОПКИ
    if 'подписки' in text.lower():
        bot.send_message(chat_id, "🔔 Подписки работают!")
    elif 'поиск' in text.lower() or 'тендеров' in text.lower():
        bot.send_message(chat_id, "🔍 Поиск тендеров работает!")
    elif 'обследование' in text.lower() or 'зданий' in text.lower():
        bot.send_message(chat_id, "🏢 Обследование зданий работает!")
    elif 'помощь' in text.lower():
        bot.send_message(chat_id, "❓ Помощь работает!")
    else:
        bot.send_message(chat_id, f"Получено: {text}")

@app.route('/', methods=['POST'])
def webhook():
    logger.info("=== WEBHOOK ===")
    json_string = request.get_data().decode('utf-8')
    logger.info(f"JSON: {json_string[:100]}")
    
    update = telebot.types.Update.de_json(json_string)
    if update and update.message:
        logger.info(f"ОБРАБАТЫВАЕМ: {update.message.text}")
        bot.process_new_updates([update])
    
    return 'OK', 200

@app.route('/health', methods=['GET'])
def health():
    return 'Bot OK!', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
