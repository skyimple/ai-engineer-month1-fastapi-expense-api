# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A simple FastAPI-based expense tracking API. The entire web application lives in a single file.

## Commands

**Run the API:**
```bash
uvicorn fastapi_expense_api.main:app --reload
```

**Run tests:**
```bash
pytest
```

**Run a single test:**
```bash
pytest tests/test_file.py::test_name
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**CLI utilities:**
```bash
python expense_tracker.py
python weather_cli.py
```

## Architecture

- **FastAPI app:** `fastapi_expense_api/main.py` - Contains the FastAPI app, SQLite database logic, and all endpoints
- **CLI utilities:** `expense_tracker.py` (expense tracking), `weather_cli.py` (weather lookups)
- **Database:** SQLite (`expenses.db`) - auto-created on startup via `init_db()`
- **Connection management:** Uses a `get_db()` context manager for SQLite connections
- **Pydantic models:** `ExpenseCreate` (request schema) and `ExpenseResponse` (response schema)
- **Virtual environment:** `ai-engineer-month1/` (Windows pyvenv)

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/expenses` | List all expenses |
| POST | `/expenses` | Create a new expense |
| DELETE | `/expenses/{expense_id}` | Delete an expense by ID |

## Data Model

Expense fields: `id` (auto), `amount` (float), `category` (str), `date` (str), `note` (optional str)
