# portus_storage_module/storage_lite.py

import sqlite3
import uuid
from pathlib import Path

_DB_PATH: Path

_initialized = False

def set_db_path(path: Path):
    global _DB_PATH
    _DB_PATH = path

def _init_db():
    global _initialized
    if _initialized:
        return
    _initialized = True
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(_DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
      id TEXT PRIMARY KEY,
      title TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      last_access DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS turns (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      conversation_id TEXT,
      role TEXT,
      content TEXT,
      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY(conversation_id) REFERENCES conversations(id)
    )
    """)
    conn.commit()
    conn.close()

def init_conversation(first_message: str) -> str:
    _init_db()
    conv_id = str(uuid.uuid4())
    title = first_message.strip().replace("\n", " ")[:50]
    #print(f"[StorageLite] Creating conversation ID: {conv_id}, title: {title}")
    conn = sqlite3.connect(_DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO conversations(id, title) VALUES (?, ?)",
        (conv_id, title)
    )
    conn.commit()
    conn.close()
    return conv_id

def save_turn(conversation_id: str, role: str, content: str):
    if conversation_id is None:
        return
    _init_db()
    #print(f"[StorageLite] Saving turn → conv_id={conversation_id}, role={role}, content={content}")
    conn = sqlite3.connect(_DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO turns(conversation_id, role, content) VALUES (?, ?, ?)",
        (conversation_id, role, content)
    )
    cur.execute(
        "UPDATE conversations SET last_access = CURRENT_TIMESTAMP WHERE id = ?",
        (conversation_id,)
    )
    conn.commit()
    conn.close()

def list_conversations(limit: int = 10):
    _init_db()
    conn = sqlite3.connect(_DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, title, last_access FROM conversations ORDER BY last_access DESC LIMIT ?",
        (limit,)
    )
    rows = cur.fetchall()
    conn.close()
    return [
        {"id": r[0], "title": r[1], "last_access": r[2]}
        for r in rows
    ]

def load_conversation(conversation_id: str):
    _init_db()
    conn = sqlite3.connect(_DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT role, content, timestamp FROM turns WHERE conversation_id = ? ORDER BY id",
        (conversation_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return [
        {"role": r[0], "content": r[1], "timestamp": r[2]}
        for r in rows
    ]

def delete_conversation(conversation_id: str):
    _init_db()
    conn = sqlite3.connect(_DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM turns WHERE conversation_id = ?", (conversation_id,))
    cur.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
    conn.commit()
    conn.close()
    print(f"[StorageLite] Deleted conversation {conversation_id}")