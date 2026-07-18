import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "notes.db"

class Database:
    """Обёртка над SQLite для хранения заметок."""
    def __init__(self, db_path: Path = DB_PATH):
        self.connection = sqlite3.connect(db_path)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self._create_tables()

    def _create_tables(self):
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                reminder_datetime TEXT,
                repeat_rule TEXT
            )
        """)
        self.connection.commit()

    def get_all_notes(self):
        cursor = self.connection.execute(
            "SELECT id, title, content, created_at, updated_at, reminder_datetime, repeat_rule "
            "FROM notes ORDER BY updated_at DESC"
        )
        return cursor.fetchall()

    def get_note(self, note_id: int):
        cursor = self.connection.execute(
            "SELECT id, title, content, created_at, updated_at, reminder_datetime, repeat_rule "
            "FROM notes WHERE id = ?",
            (note_id,)
        )
        return cursor.fetchone()

    def add_note(self, title: str, content: str) -> int:
        now = datetime.now().isoformat(timespec="seconds")
        cursor = self.connection.execute(
            "INSERT INTO notes (title, content, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (title, content, now, now)
        )
        self.connection.commit()
        return cursor.lastrowid

    def update_note(self, note_id: int, title: str, content: str):
        now = datetime.now().isoformat(timespec="seconds")
        self.connection.execute(
            "UPDATE notes SET title = ?, content = ?, updated_at = ? WHERE id = ?",
            (title, content, now, note_id)
        )
        self.connection.commit()

    def delete_note(self, note_id: int):
        self.connection.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        self.connection.commit()

    def close(self):
        self.connection.close()