import sqlite3
from typing import Optional

class SqliteRepository:
    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    email TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL
                )
            """)

    def save(self, data: dict) -> None:
        with sqlite3.connect(self.db_path) as conn:
            try:
                conn.execute(
                    "INSERT INTO users (email, name, age) VALUES (?, ?, ?)",
                    (data['email'], data['name'], data['age'])
                )
            except sqlite3.IntegrityError:
                raise ValueError("duplicate email")

    def find_by_email(self, email: str) -> Optional[dict]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, email, age FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            if row:
                return {"name": row[0], "email": row[1], "age": row[2]}
            return None