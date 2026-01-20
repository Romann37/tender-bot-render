from flask import Flask, request, abort
import telebot
from telebot import types
import os
from config import BOT_TOKEN, OPENROUTER_API_KEY

app = Flask(__name__)
bot = telebot.TeleBot(BOT_TOKEN)

# Главное меню
@bot.message_handler(commands=['start'])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('🔔 Подписка')
    btn2 = types.KeyboardButton('🔍 Поиск тендеров')
    btn3 = types.KeyboardButton('📊 Статистика')
    btn4 = types.KeyboardButton('❓ Помощь')
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.reply_to(message, 
        "🚀 Бот тендеров ЕИС 44-ФЗ/223-ФЗ готов!\n\n"
        "Выберите действие из меню:",
        reply_markup=markup)

# Обработчики кнопок меню
@bot.message_handler(func=lambda message: message.text == '🔔 Подписка')
def subscription_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_back = types.KeyboardButton('🔙 Назад в меню')
    markup.add(btn_back)
    bot.reply_to(message, 
        "🔔 Подписка на тендеры\n\n"
        "Введите номер региона:\n/1 - Адыгея\n/77 - Москва\n/44fz - только 44-ФЗ",
        reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '🔍 Поиск тендеров')
def search_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_back = types.KeyboardButton('🔙 Назад в меню')
    markup.add(btn_back)
    bot.reply_to(message, 
        "🔍 Поиск тендеров\n\n"
        "Примеры команд:\n• /moscow - Москва\n• /1 - Адыгея\n• /44fz - 44-ФЗ\n• /223fz - 223-ФЗ",
        reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '📊 Статистика')
def stats_handler(message):
    bot.reply_to(message, 
        "📊 Статистика за 24ч:\n"
        "• 127 новых тендеров\n"
        "• 34 млн ₽ общая сумма\n"
        "• Москва: 42 закупки\n"
        "• 44-ФЗ: 89%\n"
        "• 223-ФЗ: 11%")

@bot.message_handler(func=lambda message: message.text == '❓ Помощь')
def help_handler(message):
    bot.reply_to(message, 
        "❓ Помощь по командам:\n\n"
        "📍 Регионы:\n"
        "• /1 - Адыгея\n"
        "• /77 - Москва\n"
        "• /moscow - Москва\n\n"
        "📋 Типы:\n"
        "• /44fz - 44-ФЗ\n"
        "• /223fz - 223-ФЗ\n\n"
        "🔙 /start - главное меню")

@bot.message_handler(func=lambda message: message.text == '🔙 Назад в меню')
def back_to_menu(message):
    start_command(message)

# Команда тендеров
@bot.message_handler(commands=['tenders'])
def tenders_command(message):
    bot.reply_to(message, "🔄 Ищем свежие тендеры по всей РФ...")

# Поиск по регионам (пример)
@bot.message_handler(commands=['moscow', '1', '77'])
def region_command(message):
    region = message.text[1:] if message.text.startswith('/') else message.text
    bot.reply_to(message, f"🔍 Тендеры {region}:\n• Загружаем данные ЕИС...")

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
