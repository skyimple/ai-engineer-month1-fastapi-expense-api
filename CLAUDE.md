# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A FastAPI-based expense tracking API with CLI utilities. Two versions exist:

- **Simple version:** `fastapi_expense_api/main.py` — single-file app with basic CRUD
- **Final version:** `month1-final-expense-api/` — modular app with routers, middleware, file upload, and weather integration

## Commands

**Run the simple API (from repo root):**
```bash
uvicorn fastapi_expense_api.main:app --reload
```

**Run the final API (from month1-final-expense-api/):**
```bash
cd month1-final-expense-api
uvicorn fastapi_expense_api.main:app --reload
```

**Run tests (from month1-final-expense-api/):**
```bash
cd month1-final-expense-api
pytest
```

**Run a single test:**
```bash
pytest tests/test_expenses.py::test_name
```

**Install dependencies:**
```bash
pip install -r requirements.txt          # root (simple version)
pip install -r month1-final-expense-api/requirements.txt  # final version
```

**CLI utilities (from repo root):**
```bash
python expense_tracker.py   # interactive expense tracker (JSON-based)
python weather_cli.py       # weather lookups via Open-Meteo API
```

## Architecture

### Final Version (month1-final-expense-api/)

The modular app splits concerns across files:

- `main.py` — App factory, middleware registration, router inclusion, startup DB init
- `database.py` — `get_db()` context manager + `init_db()` schema creation (SQLite)
- `models.py` — Pydantic v2 models with validation (`ExpenseCreate`, `ExpenseResponse`, `UploadResponse`, `WeatherResponse`)
- `middleware.py` — `ExceptionHandlerMiddleware` that catches all exceptions and returns JSON (maps `ValueError` → 400, defaults to 500)
- `routers/expenses.py` — CRUD at `/expenses`
- `routers/upload.py` — JSON file import at `/upload`
- `routers/weather.py` — Weather lookup at `/weather/{city}` via Open-Meteo geocoding + weather APIs

### Simple Version (root)

- `fastapi_expense_api/main.py` — All-in-one file with `get_db()`, `init_db()`, Pydantic models, and three endpoints

### API Endpoints (Final Version)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/expenses` | List all expenses |
| POST | `/expenses` | Create a new expense (returns 201) |
| DELETE | `/expenses/{expense_id}` | Delete an expense (404 if not found) |
| POST | `/upload` | Import expenses from JSON file |
| GET | `/weather/{city}` | Get weather for a city via Open-Meteo |

### Data Model

Expense: `id` (auto), `amount` (float, must be > 0), `category` (str, 1-50 chars), `date` (str), `note` (optional str, max 200 chars)

## Testing Notes

- Tests live in `month1-final-expense-api/tests/test_expenses.py` using `pytest` + `TestClient`
- An `autouse` fixture resets the database before each test
- Weather tests (`test_weather_endpoint`, `test_weather_endpoint_invalid_city`) make **real network calls** to Open-Meteo — they can be flaky offline
