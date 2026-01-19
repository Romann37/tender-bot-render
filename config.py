import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
MODEL_ID = os.getenv('MODEL_ID', 'anthropic/claude-3.5-sonnet')
DB_PATH = "tender_bot.db"
