import aiosqlite
import json
from datetime import datetime
from config import DB_PATH


class UserManager:
    def __init__(self):
        self.db_path = DB_PATH

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    region TEXT DEFAULT '37',
                    region_name TEXT DEFAULT 'Иваново',
                    keywords TEXT DEFAULT '[]',
                    auto_search INTEGER DEFAULT 0,
                    notify_new INTEGER DEFAULT 1,
                    min_price INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            await db.commit()

    async def get_user(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return dict(zip([desc[0] for desc in cursor.description], row))
        return None

    async def create_user(self, user_id, username):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)
            ''', (user_id, username))
            await db.commit()

    async def update_user(self, user_id, **kwargs):
        fields = ', '.join([f"{k}=?" for k in kwargs.keys()])
        values = list(kwargs.values()) + [user_id]
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f'UPDATE users SET {fields}, updated_at=CURRENT_TIMESTAMP WHERE user_id=?', values)
            await db.commit()


db = UserManager()
