"""SQLite database connection management."""

import sqlite3
from contextlib import contextmanager

DATABASE_PATH = "expenses.db"


@contextmanager
def get_db():
    """Context manager for SQLite database connections.

    Yields:
        sqlite3.Connection: Database connection

    Ensures connection is properly closed after use.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Initialize the database schema.

    Creates the expenses table if it doesn't exist.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                note TEXT
            )
        """)
        conn.commit()
