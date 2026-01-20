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
        "👇 Нажмите кнопку для действия:",
        reply_markup=markup)

# 🔥 ОБРАБОТЧИКИ ТОЧНО ПО ВАШИМ КНОПКАМ:
@bot.message_handler(func=lambda m: 'Подписки' in m.text)
def subscription_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_back = types.KeyboardButton('🔙 Главное меню')
    markup.add(btn_back)
    bot.reply_to(message, 
        "🔔 Подписки на тендеры\n\n"
        "📍 Выберите регион:\n"
        "• /1 — Адыгея\n"
        "• /77 — Москва\n"
        "• /moscow — Москва\n"
        "• /spb — СПб",
        reply_markup=markup)

@bot.message_handler(func=lambda m: 'Поиск тендеров' in m.text)
def search_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_back = types.KeyboardButton('🔙 Главное меню')
    markup.add(btn_back)
    bot.reply_to(message, 
        "🔍 Поиск тендеров\n\n"
        "💬 Введите:\n"
        "• moscow — Москва\n"
        "• 77 — Москва\n"
        "• 44fz — только 44-ФЗ\n"
        "• здание — обследование зданий",
        reply_markup=markup)

@bot.message_handler(func=lambda m: 'обследование зданий' in m.text)
def buildings_handler(message):
    bot.reply_to(message, 
        "🏢 Тендеры 'обследование зданий'\n\n"
        "🔄 Ищем по ЕИС 44-ФЗ/223-ФЗ...\n"
        "• ОКПД2: 71.12.45\n"
        "• Ключевые слова: обследование, здание\n\n"
        "⏳ Результаты через 10 сек...")

@bot.message_handler(func=lambda m: 'Помощь' in m.text)
def help_handler(message):
    bot.reply_to(message, 
        "❓ Помощь:\n\n"
        "🔔 Подписки — уведомления 24/7\n"
        "🔍 Поиск — найти тендеры\n"
        "🏢 обследование зданий — спец. поиск\n"
        "📊 Статистика — цифры по РФ\n\n"
        "💬 Примеры: /moscow /1 /44fz")

@bot.message_handler(func=lambda m: '🔙 Главное меню' in m.text)
def back_menu(message):
    start_command(message)

# Дополнительные команды
@bot.message_handler(commands=['moscow', '1', '77'])
def region_command(message):
    region = message.text[1:]
    bot.reply_to(message, f"🔍 Тендеры {region} загружаем...")

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
