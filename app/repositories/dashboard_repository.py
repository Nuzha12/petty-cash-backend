from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.models.expense import Expense
from app.models.category import Category


def get_dashboard_data(db: Session, company_id: int, month: int, year: int):

    total = db.query(
        func.coalesce(func.sum(Expense.amount), 0)
    ).filter(
        Expense.company_id == company_id,
        extract("month", Expense.expense_date) == month,
        extract("year", Expense.expense_date) == year
    ).scalar()

    category_data = db.query(
        Category.name,
        func.coalesce(func.sum(Expense.amount), 0)
    ).join(
        Expense, Expense.category_id == Category.category_id
    ).filter(
        Expense.company_id == company_id,
        extract("month", Expense.expense_date) == month,
        extract("year", Expense.expense_date) == year
    ).group_by(Category.name).all()

    categories = [
        {"category": c[0], "total": float(c[1])}
        for c in category_data
    ]

    top_category = max(categories, key=lambda x: x["total"])["category"] if categories else None

    return {
        "total_expenses": float(total),
        "categories": categories,
        "top_category": top_category
    }