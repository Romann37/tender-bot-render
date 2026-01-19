# TenderAnalyzerBot PRO

Telegram бот для поиска тендеров ЕИС с ИИ-анализом.

## Развертывание на Render

1. Fork/Clone репозиторий
2. render.com → New Web Service → Connect GitHub
3. Environment Variables: BOT_TOKEN, OPENROUTER_API_KEY
4. Build: `pip install -r requirements.txt`
5. Start: `gunicorn app:app`
