from flask import Flask, request, abort
import telebot
from telebot import types
import os
from config import BOT_TOKEN

app = Flask(__name__)
bot = telebot.TeleBot(BOT_TOKEN)

# Главное меню
@bot.message_handler(commands=['start'])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('🔔 Подписки')
    btn2 = types.KeyboardButton('🔍 Поиск тендеров')
    btn3 = types.KeyboardButton('📊 обследование зданий')
    btn4 = types.KeyboardButton('❓ Помощь')
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.reply_to(message, 
        "🚀 Бот тендеров ЕИС 44-ФЗ/223-ФЗ готов!\n\n"
        "👇 Нажмите кнопку:",
        reply_markup=markup)

# 🔥 ЕДИНСТВЕННЫЙ ОБРАБОТЧИК ВСЕГО ТЕКСТА
@bot.message_handler(content_types=['text'])
def handle_all_text(message):
    text = message.text.lower()
    
    # Главное меню
    if '/start' in text or text == '/start':
        start_command(message)
        
    # Кнопки меню (ТОЧНЫЕ названия из вашего скрина)
    elif 'подписки' in text:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton('🔙 Главное меню')
        markup.add(btn_back)
        bot.reply_to(message, 
            "🔔 Подписки на тендеры\n\n"
            "📍 Регионы:\n/1 - Адыгея\n/77 - Москва\n/moscow",
            reply_markup=markup)
    
    elif 'поиск тендеров' in text:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton('🔙 Главное меню')
        markup.add(btn_back)
        bot.reply_to(message, 
            "🔍 Поиск тендеров\n\n"
            "💬 Введите: moscow /1 /77 /44fz",
            reply_markup=markup)
    
    elif 'обследование зданий' in text:
        bot.reply_to(message, 
            "🏢 Тендеры 'обследование зданий'\n\n"
            "✅ ОКПД2: 71.12.45\n"
            "✅ 44-ФЗ/223-ФЗ\n"
            "🔄 Поиск по ЕИС...")
    
    elif 'помощь' in text:
        bot.reply_to(message, 
            "❓ Помощь:\n\n"
            "🔔 Подписки\n🔍 Поиск тендеров\n"
            "🏢 обследование зданий\n📊 Статистика")
    
    elif '🔙 главное меню' in text:
        start_command(message)
    
    # Регионы и ключевые слова
    elif any(x in text for x in ['moscow', '77', '1']):
        bot.reply_to(message, f"🔍 Тендеры {text} загружаем...")
    
    else:
        # Эхо для отладки
        bot.reply_to(message, f"Получено: {text}\nПопробуйте кнопки меню")

@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)

@app.route('/health', methods=['GET'])
def health():
    return 'Bot alive!', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
