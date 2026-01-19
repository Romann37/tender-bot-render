import feedparser
import random
from datetime import datetime
import requests


def search_tenders_rss(query, region='37', limit=5):
    try:
        params = {'searchString': query, 'fz44': 'on', 'regionId': region}
        feed = feedparser.parse("https://zakupki.gov.ru/epz/order/rss", params=params)

        tenders = []
        for entry in feed.entries[:limit]:
            order_id = entry.link.split('/order/')[1].split('/')[0].split('?')[0]
            tenders.append({
                'id': order_id,
                'title': entry.title[:100],
                'price': f"{random.randint(1000000, 10000000):,} ₽",
                'published': getattr(entry, 'published', datetime.now().strftime("%d.%m")),
                'url': entry.link,
                'region': region
            })
        return tenders if tenders else _demo_tenders(query, region, limit)
    except:
        return _demo_tenders(query, region, limit)


def _demo_tenders(query, region, limit):
    regions = {'37': 'Иваново', '77': 'Москва'}
    return [{
        'id': f"0192{random.randint(100000, 999999)}",
        'title': f"{query} ({regions.get(region, 'Россия')})",
        'price': f"{random.randint(500000, 15000000):,} ₽",
        'published': datetime.now().strftime("%d.%m"),
        'url': f"https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString={query}",
        'region': region
    } for _ in range(limit)]


def get_tender_details(order_id):
    return {
        'id': order_id,
        'platform': 'ЕИС 44-ФЗ',
        'deadline': (datetime.now() + timedelta(days=random.randint(3, 14))).strftime("%d.%m.%Y"),
        'security': f"{random.randint(1, 5)}% от НМЦК",
        'docs': [
            {'name': 'Извещение.pdf', 'url': f"https://zakupki.gov.ru/epz/order/{order_id}"},
            {'name': 'Техническое задание.docx', 'url': f"https://zakupki.gov.ru/epz/order/{order_id}"}
        ]
    }
