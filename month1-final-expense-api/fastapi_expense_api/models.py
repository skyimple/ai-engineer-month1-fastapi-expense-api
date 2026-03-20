"""Pydantic models for request/response validation."""

from typing import Optional, List
from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    """Schema for creating a new expense."""

    amount: float = Field(..., gt=0, description="Expense amount (must be positive)")
    category: str = Field(..., min_length=1, max_length=50, description="Expense category")
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    note: Optional[str] = Field(None, max_length=200, description="Optional note")


class ExpenseResponse(BaseModel):
    """Schema for expense response."""

    id: int
    amount: float
    category: str
    date: str
    note: Optional[str]

    class Config:
        from_attributes = True


class UploadResponse(BaseModel):
    """Schema for file upload response."""

    imported: int = Field(..., description="Number of expenses successfully imported")
    errors: List[str] = Field(default_factory=list, description="List of errors encountered")


class WeatherResponse(BaseModel):
    """Schema for weather API response."""

    city: str = Field(..., description="City name")
    temperature: float = Field(..., description="Current temperature in Celsius")
    weather_code: int = Field(..., description="Open-Meteo weather code")
    description: str = Field(..., description="Human-readable weather description")
