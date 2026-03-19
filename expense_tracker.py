"""Expense Tracker CLI - Interactive command-line expense tracking."""

import json
from dataclasses import dataclass, asdict
from typing import Optional

DATA_FILE = "expenses.json"


@dataclass
class Expense:
    """Represents a single expense record."""
    amount: float
    category: str
    date: str
    note: str = ""


def load_expenses() -> list[dict]:
    """Load expenses from JSON file."""
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_expenses(expenses: list[dict]) -> None:
    """Save expenses to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def add_expense(expenses: list[dict]) -> list[dict]:
    """Prompt user for expense details and add to list."""
    # Amount with retry on invalid input
    while True:
        amount_str = input("Amount: ").strip()
        try:
            amount = float(amount_str)
            break
        except ValueError:
            print("Error: Please enter a valid number.")

    category = input("Category: ").strip()
    date = input("Date (YYYY-MM-DD): ").strip()
    note = input("Note (optional): ").strip()

    expense = Expense(amount=amount, category=category, date=date, note=note)
    expenses.append(asdict(expense))
    print("Expense added successfully!")
    return expenses


def list_expenses(expenses: list[dict]) -> None:
    """Print all expenses in table format."""
    if not expenses:
        print("No expenses recorded.")
        return

    print(f"\n{'#':<4} {'Amount':<10} {'Category':<15} {'Date':<12} {'Note'}")
    print("-" * 70)
    for i, exp in enumerate(expenses, 1):
        print(f"{i:<4} {exp['amount']:<10.2f} {exp['category']:<15} {exp['date']:<12} {exp['note']}")


def stats_by_category(expenses: list[dict]) -> None:
    """Print aggregated statistics by category."""
    if not expenses:
        print("No expenses recorded.")
        return

    totals: dict[str, float] = {}
    for exp in expenses:
        cat = exp["category"]
        totals[cat] = totals.get(cat, 0) + exp["amount"]

    print("\n=== Expenses by Category ===")
    for cat, total in sorted(totals.items()):
        print(f"  {cat}: ${total:.2f}")
    print(f"\nTotal: ${sum(totals.values()):.2f}")


def main() -> None:
    """Main CLI loop."""
    expenses = load_expenses()
    print("=== Expense Tracker ===")

    while True:
        print("\nMenu:")
        print("1: Add expense")
        print("2: List all expenses")
        print("3: Statistics by category")
        print("4: Exit and save")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            expenses = add_expense(expenses)
        elif choice == "2":
            list_expenses(expenses)
        elif choice == "3":
            stats_by_category(expenses)
        elif choice == "4":
            save_expenses(expenses)
            print(f"Expenses saved to {DATA_FILE}. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    main()
