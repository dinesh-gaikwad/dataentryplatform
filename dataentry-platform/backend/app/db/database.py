import sqlite3
from pathlib import Path

DB_FILE = Path("dataentry.db")

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn
