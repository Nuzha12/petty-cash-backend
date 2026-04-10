from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.models.budget import Budget
from app.models.expense import Expense
from app.models.category import Category


def get_budget_vs_actual(db: Session, company_id: int, month: int, year: int):
    results = db.query(
        Category.name,
        Budget.amount,
        func.coalesce(func.sum(Expense.amount), 0)
    ).join(
        Category, Category.category_id == Budget.category_id
    ).outerjoin(
        Expense,
        (Expense.category_id == Budget.category_id) &
        (Expense.company_id == company_id) &
        (extract("month", Expense.expense_date) == month) &
        (extract("year", Expense.expense_date) == year)
    ).filter(
        Budget.company_id == company_id,
        Budget.month == month,
        Budget.year == year
    ).group_by(
        Category.name,
        Budget.amount
    ).all()

    return results


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

    top_category = max(categories, key=lambda x: x["total"])["category"] if categories else "-"


    budget_data = get_budget_vs_actual(db, company_id, month, year)

    budget_vs_actual = [
        {
            "category": b[0],
            "budget": float(b[1]),
            "spent": float(b[2]),
            "remaining": float(b[1] - b[2])
        }
        for b in budget_data
    ]

    recent_expenses = db.query(
        Expense,
        Category.name
    ).join(
        Category, Expense.category_id == Category.category_id
    ).filter(
        Expense.company_id == company_id
    ).order_by(
        Expense.created_at.desc()
    ).limit(5).all()

    recent_data = [
        {
            "amount": float(e[0].amount),
            "description": e[0].description,
            "date": str(e[0].expense_date),
            "category": e[1]
        }
        for e in recent_expenses
    ]

    return {
        "total_expenses": float(total),
        "categories": categories,
        "top_category": top_category,
        "budget_vs_actual": budget_vs_actual,
        "recent_expenses": recent_data
    }
