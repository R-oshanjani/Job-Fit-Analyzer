# app/memory.py

import sqlite3
import os
import hashlib
import pickle


class EmbeddingMemory:
    def __init__(self, db_path="data/app.db"):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.full_path = os.path.join(base_dir, db_path)

        os.makedirs(os.path.dirname(self.full_path), exist_ok=True)

        self.conn = sqlite3.connect(self.full_path, check_same_thread=False)
        self._init_tables()

    def _init_tables(self):
        # Embedding cache table
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            text_hash TEXT PRIMARY KEY,
            embedding BLOB
        )
        """)

        # Decision memory table
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS decisions (
            job_id TEXT PRIMARY KEY,
            decision TEXT
        )
        """)

        self.conn.commit()

    # ---------- Embedding cache ----------
    def _hash(self, text: str):
        return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()

    def get_embedding(self, text: str):
        h = self._hash(text)
        row = self.conn.execute(
            "SELECT embedding FROM embeddings WHERE text_hash = ?",
            (h,)
        ).fetchone()
        return pickle.loads(row[0]) if row else None

    def store_embedding(self, text: str, embedding):
        h = self._hash(text)
        self.conn.execute(
            "INSERT OR REPLACE INTO embeddings (text_hash, embedding) VALUES (?, ?)",
            (h, pickle.dumps(embedding))
        )
        self.conn.commit()

    # ---------- Decision memory ----------
    def already_processed(self, job_id: str) -> bool:
        row = self.conn.execute(
            "SELECT 1 FROM decisions WHERE job_id = ?",
            (job_id,)
        ).fetchone()
        return row is not None

    def store_decision(self, job_id: str, decision: str):
        self.conn.execute(
            "INSERT OR REPLACE INTO decisions VALUES (?, ?)",
            (job_id, decision)
        )
        self.conn.commit()


# Singleton instance
memory = EmbeddingMemory()

# Export helpers
already_processed = memory.already_processed
store_decision = memory.store_decision
