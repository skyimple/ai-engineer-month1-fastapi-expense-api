# FastAPI Expense API

A comprehensive FastAPI-based expense tracking REST API with SQLite persistence, file upload support, and weather integration.

## Features

- **Expense CRUD Operations** - Create, read, delete expenses stored in SQLite
- **File Upload** - Import expenses from JSON files (batch processing)
- **Weather Integration** - Fetch current weather data for any city via Open-Meteo API
- **Global Exception Handling** - Graceful error responses for all endpoints
- **Auto-generated Documentation** - Interactive API docs via Swagger UI

## Project Structure

```
month1-final-expense-api/
├── fastapi_expense_api/
│   ├── __init__.py           # Package initialization
│   ├── main.py               # FastAPI app entry point
│   ├── models.py             # Pydantic schemas
│   ├── database.py           # SQLite connection management
│   ├── middleware.py         # Global exception handler
│   └── routers/
│       ├── __init__.py
│       ├── expenses.py       # /expenses endpoints
│       ├── upload.py         # /upload endpoint
│       └── weather.py        # /weather endpoint
├── tests/
│   ├── __init__.py
│   └── test_expenses.py      # Unit tests
├── requirements.txt
└── README.md
```

## Installation

```bash
# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the API

```bash
uvicorn fastapi_expense_api.main:app --reload
```

The API will be available at `http://localhost:8000`

- **Swagger Documentation**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/expenses` | List all expenses |
| POST | `/expenses` | Create a new expense |
| DELETE | `/expenses/{expense_id}` | Delete an expense by ID |
| POST | `/upload` | Upload JSON file to import expenses |
| GET | `/weather/{city}` | Get current weather for a city |

### Expense Data Model

```json
{
  "id": 1,
  "amount": 25.50,
  "category": "food",
  "date": "2026-03-20",
  "note": "Lunch at restaurant"
}
```

### Weather Response

```json
{
  "city": "Beijing",
  "temperature": 18.5,
  "weather_code": 3,
  "description": "Partly cloudy"
}
```

### Upload Format (JSON)

```json
[
  {
    "amount": 25.50,
    "category": "food",
    "date": "2026-03-20",
    "note": "Lunch at restaurant"
  },
  {
    "amount": 150.00,
    "category": "transport",
    "date": "2026-03-19",
    "note": "Taxi to airport"
  }
]
```

## Running Tests

```bash
pytest
```

## Key Learnings

### FastAPI Dependency Injection & Routers
FastAPI's router system allows modular code organization. Each router handles a group of related endpoints, and routers are mounted onto the main application using `app.include_router()` with optional prefixes.

### Context Managers for Database Connections
SQLite connections are managed via a `get_db()` context manager that ensures connections are properly closed after use, even if an exception occurs:

```python
@contextmanager
def get_db():
    conn = sqlite3.connect("expenses.db")
    try:
        yield conn
    finally:
        conn.close()
```

### Pydantic for Data Validation
Pydantic models provide automatic request validation, serialization, and OpenAPI schema generation. `BaseModel` subclasses define the structure, and FastAPI handles the rest.

### File Upload Handling
FastAPI handles multipart form data via `UploadFile` from `python-multipart`. Files are read asynchronously or synchronously depending on needs.

### External API Integration
The `requests` library simplifies calling external REST APIs. For Open-Meteo:
1. Geocoding: Convert city name to coordinates
2. Weather: Fetch current weather using coordinates

### Global Exception Middleware
A custom middleware class catches unhandled exceptions and returns structured JSON error responses instead of default HTML error pages.

### SQLite as Embedded Database
SQLite requires no separate server process, making it ideal for local development and simple production deployments with low concurrency needs.
