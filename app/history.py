# app/history.py

import sqlite3
import os
from datetime import datetime


class HistoryStore:
    def __init__(self, db_path="data/app.db"):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.full_path = os.path.join(base_dir, db_path)

        self.conn = sqlite3.connect(self.full_path, check_same_thread=False)
        self._init_table()

    def _init_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT,
            decision TEXT,
            score INTEGER,
            timestamp TEXT
        )
        """)
        self.conn.commit()

    def log(self, job_id: str, decision: str, score: int):
        self.conn.execute(
            "INSERT INTO history (job_id, decision, score, timestamp) VALUES (?, ?, ?, ?)",
            (job_id, decision, score, datetime.utcnow().isoformat())
        )
        self.conn.commit()

    def fetch_all(self):
        return self.conn.execute(
            "SELECT job_id, decision, score, timestamp FROM history ORDER BY timestamp DESC"
        ).fetchall()
