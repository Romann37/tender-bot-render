import random
from datetime import datetime, timedelta
import requests
from config import REGIONS

def search_tenders_rss(query, region='37', limit=5):
    """Генератор реалистичных тендеров ЕИС"""
    region_name = REGIONS.get(region, 'Россия')
    
    tenders = []
    base_id = f"019{random.randint(220000, 229999)}"
    
    for i in range(limit):
        tender_id = f"{base_id}{random.randint(10000, 99999)}"
        price = random.randint(500000, 5000000)
        
        tenders.append({
            'id': tender_id,
            'title': f"{query.title()} {region_name} №{i+1}",
            'price': f"{price:,} ₽",
            'published': datetime.now().strftime("%d.%m.%Y %H:%M"),
            'url': f"https://zakupki.gov.ru/epz/order/{tender_id}/common-info.html",
            'region': region_name
        })
    return tenders

def get_tender_details(order_id):
    """Детали тендера"""
    return {
        'id': order_id,
        'platform': 'ЕИС 44-ФЗ',
        'deadline': (datetime.now() + timedelta(days=random.randint(5, 20))).strftime("%d.%m.%Y"),
        'security': f"{random.randint(1, 5)}% от НМЦК",
        'docs': [
            f"https://zakupki.gov.ru/epz/order/{order_id}/notification/downloadDocument.do",
            f"https://zakupki.gov.ru/epz/order/{order_id}/notification/downloadDocument.do?doc=tech",
            f"https://zakupki.gov.ru/epz/order/{order_id}/notification/downloadDocument.do?doc=contract"
        ]
    }
