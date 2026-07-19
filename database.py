import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "notes.db"

class Database:
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

    def add_note(self, title: str, content: str, reminder_datetime: str = None, repeat_rule: str = None) -> int:
        now = datetime.now().isoformat(timespec="seconds")
        cursor = self.connection.execute(
            "INSERT INTO notes (title, content, created_at, updated_at, reminder_datetime, repeat_rule) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (title, content, now, now, reminder_datetime, repeat_rule)
        )
        self.connection.commit()
        return cursor.lastrowid

    def update_note(self, note_id: int, title: str, content: str,
                     reminder_datetime: str = None, repeat_rule: str = None):
        now = datetime.now().isoformat(timespec="seconds")
        self.connection.execute(
            "UPDATE notes SET title = ?, content = ?, updated_at = ?, "
            "reminder_datetime = ?, repeat_rule = ? WHERE id = ?",
            (title, content, now, reminder_datetime, repeat_rule, note_id)
        )
        self.connection.commit()

    def delete_note(self, note_id: int):
        self.connection.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        self.connection.commit()

    def get_due_reminders(self, now_iso: str):
        cursor = self.connection.execute(
            "SELECT id, title, content, reminder_datetime, repeat_rule FROM notes "
            "WHERE reminder_datetime IS NOT NULL AND reminder_datetime <= ?",
            (now_iso,)
        )
        return cursor.fetchall()

    def set_reminder(self, note_id: int, reminder_datetime: str, repeat_rule: str):
        self.connection.execute(
            "UPDATE notes SET reminder_datetime = ?, repeat_rule = ? WHERE id = ?",
            (reminder_datetime, repeat_rule, note_id)
        )
        self.connection.commit()

    def clear_reminder(self, note_id: int):
        self.connection.execute(
            "UPDATE notes SET reminder_datetime = NULL, repeat_rule = NULL WHERE id = ?",
            (note_id,)
        )
        self.connection.commit()

    def close(self):
        self.connection.close()
