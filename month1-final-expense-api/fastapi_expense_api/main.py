"""FastAPI Expense API - Main application entry point."""

from fastapi import FastAPI
from fastapi_expense_api.database import init_db
from fastapi_expense_api.middleware import ExceptionHandlerMiddleware
from fastapi_expense_api.routers import expenses, upload, weather

# Create FastAPI application
app = FastAPI(
    title="Expense Tracker API",
    description="A comprehensive FastAPI expense tracking API with SQLite, file upload, and weather integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add global exception handler middleware
app.add_middleware(ExceptionHandlerMiddleware)

# Initialize database on startup
app.on_event("startup")(init_db)

# Include routers
app.include_router(expenses.router)
app.include_router(upload.router)
app.include_router(weather.router)
