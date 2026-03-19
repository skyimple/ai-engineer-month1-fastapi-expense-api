"""FastAPI Expense API - Web API for expense tracking."""

import sqlite3
from contextlib import contextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Expense API", version="1.0.0")

DATABASE = "expenses.db"


@contextmanager
def get_db():
    """Context manager for database connections."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Initialize the database table."""
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                note TEXT
            )
            """
        )
        conn.commit()


class ExpenseCreate(BaseModel):
    """Schema for creating an expense."""
    amount: float
    category: str
    date: str
    note: Optional[str] = None


class ExpenseResponse(BaseModel):
    """Schema for expense response."""
    id: int
    amount: float
    category: str
    date: str
    note: Optional[str] = None


@app.on_event("startup")
def startup_event():
    """Initialize database on startup."""
    init_db()


@app.get("/expenses", response_model=list[ExpenseResponse])
def get_expenses():
    """Get all expenses."""
    with get_db() as conn:
        cursor = conn.execute("SELECT id, amount, category, date, note FROM expenses")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


@app.post("/expenses", response_model=ExpenseResponse, status_code=201)
def create_expense(expense: ExpenseCreate):
    """Create a new expense."""
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
            (expense.amount, expense.category, expense.date, expense.note),
        )
        conn.commit()
        expense_id = cursor.lastrowid

        cursor = conn.execute(
            "SELECT id, amount, category, date, note FROM expenses WHERE id = ?",
            (expense_id,),
        )
        row = cursor.fetchone()
        return dict(row)


@app.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int):
    """Delete an expense by ID."""
    with get_db() as conn:
        cursor = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Expense not found")

        return None