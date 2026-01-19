from flask import Flask, request
import telebot
import os
from config import BOT_TOKEN
from database import db
import asyncio
import threading
from parser_rss import search_tenders_rss

app = Flask(__name__)
bot = telebot.TeleBot(BOT_TOKEN)


# Webhook endpoint для Render
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        return 'ok'


@app.route('/health')
def health():
    return {"status": "TenderAnalyzerBot PRO 24/7 OK"}


@app.route('/')
def home():
    return "TenderAnalyzerBot deployed on Render!"


# Здесь все обработчики бота (копия из bot_pro.py)
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import json
import time
from datetime import datetime, timedelta
from parser_rss import get_tender_details
from analyzer import analyze_tender

user_data = {}  # Временное хранилище


def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('🔍 Поиск', '⚙️ Настройки')
    markup.add('🔔 Автопоиск', '📊 Статус')
    markup.add('ℹ️ Помощь')
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name

    asyncio.create_task(db.create_user(user_id, username))

    bot.send_message(message.chat.id,
                     "👋 **TenderAnalyzerBot PRO** на Render!\n\n"
                     "🔥 Реальные тендеры ЕИС\n"
                     "🤖 ИИ-анализ + чек-листы\n"
                     "🔔 Автопоиск каждые 30 мин\n\n"
                     "⚙️ Настройте регион и автопоиск!",
                     reply_markup=main_menu(), parse_mode='Markdown')


@bot.message_handler(func=lambda m: m.text == '🔍 Поиск')
def search_prompt(message):
    bot.send_message(message.chat.id,
                     "🔎 Введите запрос:\n*отопительные системы, котельное*",
                     parse_mode='Markdown', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add('🔙 Меню'))
    bot.register_next_step_handler(message, process_search)


def process_search(message):
    user_id = message.from_user.id
    query = message.text.strip()

    # Регион из БД или Иваново
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    user = loop.run_until_complete(db.get_user(user_id)) or {}
    region = user.get('region', '37')

    bot.send_message(message.chat.id, f"⏳ **{region}**: *{query}*...", parse_mode='Markdown')

    tenders = search_tenders_rss(query, region=region, limit=5)

    for i, tender in enumerate(tenders, 1):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(f"📄 #{i}", callback_data=f"details_{tender['id']}"))
        bot.send_message(message.chat.id,
                         f"{i}. **{tender['title']}**\n💰 {tender['price']} | 📅 {tender['published']}\n🔗 [{tender['id']}]({tender['url']})",
                         reply_markup=keyboard, parse_mode='Markdown', disable_web_page_preview=True)


@bot.message_handler(func=lambda m: m.text == '⚙️ Настройки')
def settings_menu(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('🌍 Регион', '🔙 Меню')
    bot.send_message(message.chat.id, "⚙️ **Настройки**", reply_markup=markup, parse_mode='Markdown')


@bot.message_handler(func=lambda m: m.text == '🌍 Регион')
def region_menu(message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    regions = {'37': 'Иваново', '44': 'Кострома', '78': 'СПб', '77': 'Москва', '0': 'Все'}
    for region_id, name in regions.items():
        keyboard.add(InlineKeyboardButton(name, callback_data=f"set_region_{region_id}"))
    bot.send_message(message.chat.id, "🌍 Выберите регион:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('set_region_'))
def set_region(call):
    user_id = call.from_user.id
    region_id = call.data.split('_')[-1]
    region_names = {'37': 'Иваново', '44': 'Кострома', '78': 'СПб', '77': 'Москва', '0': 'Все'}
    region_name = region_names.get(region_id, 'Неизвестно')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(db.update_user(user_id, region=region_id, region_name=region_name))

    bot.edit_message_text(f"✅ **{region_name}** установлен!", call.message.chat.id, call.message.id,
                          parse_mode='Markdown')


@bot.message_handler(func=lambda m: m.text == '🔔 Автопоиск')
def toggle_auto(message):
    user_id = message.from_user.id
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    user = loop.run_until_complete(db.get_user(user_id)) or {}
    new_status = 1 - user.get('auto_search', 0)

    loop.run_until_complete(db.update_user(user_id, auto_search=new_status))
    status = "✅ ВКЛЮЧЕН" if new_status else "❌ ОТКЛЮЧЕН"

    bot.send_message(message.chat.id, f"🔔 Автопоиск **{status}**!", parse_mode='Markdown', reply_markup=main_menu())


@bot.message_handler(func=lambda m: m.text == '🔙 Меню')
def back_menu(message):
    bot.send_message(message.chat.id, "👋 Главное меню:", reply_markup=main_menu())


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8443))
    app.run(host='0.0.0.0', port=port)
