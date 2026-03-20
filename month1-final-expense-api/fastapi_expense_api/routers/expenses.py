"""Expense CRUD endpoints."""

from fastapi import APIRouter, HTTPException
from fastapi_expense_api.database import get_db
from fastapi_expense_api.models import ExpenseCreate, ExpenseResponse

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("", response_model=list[ExpenseResponse])
def list_expenses():
    """List all expenses.

    Returns:
        List of all expenses in the database
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, amount, category, date, note FROM expenses ORDER BY id DESC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


@router.post("", response_model=ExpenseResponse, status_code=201)
def create_expense(expense: ExpenseCreate):
    """Create a new expense.

    Args:
        expense: The expense data to create

    Returns:
        The created expense with assigned ID
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
            (expense.amount, expense.category, expense.date, expense.note),
        )
        conn.commit()
        expense_id = cursor.lastrowid

        cursor.execute(
            "SELECT id, amount, category, date, note FROM expenses WHERE id = ?",
            (expense_id,),
        )
        return dict(cursor.fetchone())


@router.delete("/{expense_id}", status_code=204)
def delete_expense(expense_id: int):
    """Delete an expense by ID.

    Args:
        expense_id: The ID of the expense to delete

    Raises:
        HTTPException: 404 if expense not found
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM expenses WHERE id = ?", (expense_id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Expense not found")

        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
