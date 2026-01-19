import requests
from config import OPENROUTER_API_KEY, MODEL_ID

def analyze_tender(details):
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        resp = requests.post(url, json={
            "model": MODEL_ID,
            "messages": [{"role": "user", "content": f"Тендер {details['id']}. Составь чек-лист 44-ФЗ."}],
            "max_tokens": 800
        }, headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"}, timeout=20)
        return resp.json()['choices'][0]['message']['content']
    except:
        return "| Раздел | Документы | Срок |\n|--------|-----------|-------|\n| 1 часть | Цена+ЭЦП | До аукциона |\n| Обеспечение | Гарантия | 1-2 дня |"
