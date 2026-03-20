"""Unit tests for expense endpoints."""

import pytest
from fastapi.testclient import TestClient
from fastapi_expense_api.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Reset database before each test."""
    from fastapi_expense_api.database import get_db, init_db

    init_db()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses")
        conn.commit()


def test_list_expenses_empty():
    """Test listing expenses when database is empty."""
    response = client.get("/expenses")
    assert response.status_code == 200
    assert response.json() == []


def test_create_expense():
    """Test creating a new expense."""
    expense_data = {
        "amount": 25.50,
        "category": "food",
        "date": "2026-03-20",
        "note": "Lunch at restaurant",
    }
    response = client.post("/expenses", json=expense_data)
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 25.50
    assert data["category"] == "food"
    assert data["date"] == "2026-03-20"
    assert data["note"] == "Lunch at restaurant"
    assert "id" in data


def test_create_expense_invalid_amount():
    """Test creating expense with invalid (negative) amount."""
    expense_data = {
        "amount": -10.0,
        "category": "food",
        "date": "2026-03-20",
    }
    response = client.post("/expenses", json=expense_data)
    assert response.status_code == 422  # Validation error


def test_list_expenses_after_creation():
    """Test listing expenses after creating one."""
    expense_data = {
        "amount": 50.00,
        "category": "transport",
        "date": "2026-03-19",
    }
    client.post("/expenses", json=expense_data)

    response = client.get("/expenses")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["amount"] == 50.00


def test_delete_expense():
    """Test deleting an expense."""
    expense_data = {
        "amount": 30.00,
        "category": "entertainment",
        "date": "2026-03-18",
    }
    create_response = client.post("/expenses", json=expense_data)
    expense_id = create_response.json()["id"]

    delete_response = client.delete(f"/expenses/{expense_id}")
    assert delete_response.status_code == 204

    # Verify deletion
    list_response = client.get("/expenses")
    assert list_response.json() == []


def test_delete_expense_not_found():
    """Test deleting a non-existent expense."""
    response = client.delete("/expenses/99999")
    assert response.status_code == 404


def test_weather_endpoint():
    """Test weather endpoint with valid city."""
    response = client.get("/weather/Beijing")
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Beijing"
    assert "temperature" in data
    assert "weather_code" in data
    assert "description" in data


def test_weather_endpoint_invalid_city():
    """Test weather endpoint with invalid city."""
    response = client.get("/weather/InvalidCityNameXYZ123")
    assert response.status_code == 404


def test_global_exception_handler():
    """Test that non-existent endpoints return JSON error, not HTML."""
    response = client.get("/nonexistent-endpoint")
    # Should return JSON error, not HTML
    assert response.status_code == 404
    assert response.headers["content-type"].startswith("application/json")
