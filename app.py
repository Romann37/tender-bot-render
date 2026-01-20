from flask import Flask, request, abort
import telebot
from config import BOT_TOKEN
import os

app = Flask(__name__)
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, 
        "🚀 Бот тендеров ЕИС 44-ФЗ/223-ФЗ готов!\n\n"
        "📋 Команды:\n"
        "/tenders - свежие тендеры\n"
        "/regions - регионы\n"
        "/help - справка"
    )

@bot.message_handler(commands=['tenders'])
def tenders_command(message):
    bot.reply_to(message, "🔄 Поиск свежих тендеров...")

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
