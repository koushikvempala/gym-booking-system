import sqlite3
import os

# Path to the database file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "gym_system.db")

def get_connection():
    """Returns a new SQLite connection with row_factory for dict-like access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def execute_query(query, params=(), fetchone=False, fetchall=False, commit=False):
    """
    General-purpose query executor.
    - fetchone: returns one row as dict
    - fetchall: returns list of dicts
    - commit: for INSERT/UPDATE/DELETE
    Returns lastrowid if commit=True, else fetched data.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        if commit:
            conn.commit()
            return cursor.lastrowid
        if fetchone:
            row = cursor.fetchone()
            return dict(row) if row else None
        if fetchall:
            rows = cursor.fetchall()
            return [dict(r) for r in rows]
        return None
    except sqlite3.Error as e:
        print(f"[DB ERROR] {e}")
        return None
    finally:
        conn.close()
