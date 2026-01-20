import json
import os
from datetime import datetime
from config import DB_PATH

class UserManager:
    def __init__(self):
        self.db_path = DB_PATH
        self.users = self._load_users()
    
    def _load_users(self):
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_users(self):
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)
    
    def get_user(self, user_id):
        return self.users.get(str(user_id), {})
    
    def create_user(self, user_id, username):
        user_id = str(user_id)
        if user_id not in self.users:
            self.users[user_id] = {
                'username': username,
                'region': '37',
                'region_name': 'Иваново',
                'auto_search': 0,
                'keywords': [],
                'created_at': datetime.now().isoformat()
            }
            self._save_users()
    
    def update_user(self, user_id, **kwargs):
        user_id = str(user_id)
        if user_id not in self.users:
            self.create_user(user_id, 'Unknown')
        self.users[user_id].update(kwargs)
        self.users[user_id]['updated_at'] = datetime.now().isoformat()
        self._save_users()

db = UserManager()
