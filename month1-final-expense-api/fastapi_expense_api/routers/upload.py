"""File upload endpoint for batch importing expenses."""

import json
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi_expense_api.database import get_db
from fastapi_expense_api.models import ExpenseCreate, UploadResponse

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("", response_model=UploadResponse)
async def upload_expenses(file: UploadFile = File(...)):
    """Upload a JSON file to import expenses in batch.

    Args:
        file: JSON file containing an array of expense objects

    Returns:
        UploadResponse with count of imported expenses and any errors
    """
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="File must be a JSON file")

    try:
        contents = await file.read()
        data = json.loads(contents.decode("utf-8"))
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {str(e)}")

    if not isinstance(data, list):
        raise HTTPException(status_code=400, detail="JSON must contain an array of expenses")

    imported = 0
    errors = []

    with get_db() as conn:
        cursor = conn.cursor()
        for idx, item in enumerate(data):
            try:
                expense = ExpenseCreate(**item)
                cursor.execute(
                    "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
                    (expense.amount, expense.category, expense.date, expense.note),
                )
                imported += 1
            except Exception as e:
                errors.append(f"Row {idx + 1}: {str(e)}")

        conn.commit()

    return UploadResponse(imported=imported, errors=errors)
