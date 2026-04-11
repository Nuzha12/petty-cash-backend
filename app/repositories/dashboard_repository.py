from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.models.budget import Budget
from app.models.expense import Expense, ExpenseStatus
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
        (Expense.status == ExpenseStatus.approved) &
        (extract("month", Expense.expense_date) == month) &
        (extract("year", Expense.expense_date) == year)
    ).filter(
        Budget.company_id == company_id,
        Budget.month == month,
        Budget.year == year
    ).group_by(Category.name, Budget.amount).all()
    return results


def get_dashboard_data(db: Session, company_id: int, month: int, year: int):
    total_res = db.query(
        func.coalesce(func.sum(Expense.amount), 0)
    ).filter(
        Expense.company_id == company_id,
        Expense.status == ExpenseStatus.approved,
        extract("month", Expense.expense_date) == month,
        extract("year", Expense.expense_date) == year
    ).scalar()

    total = float(total_res) if total_res is not None else 0.0

    category_data = db.query(
        Category.name,
        func.coalesce(func.sum(Expense.amount), 0)
    ).join(
        Expense, Expense.category_id == Category.category_id
    ).filter(
        Expense.company_id == company_id,
        Expense.status == ExpenseStatus.approved,
        extract("month", Expense.expense_date) == month,
        extract("year", Expense.expense_date) == year
    ).group_by(Category.name).all()

    categories = []
    for c in category_data:
        val = float(c[1])
        if val > 0:
            categories.append({"name": str(c[0]), "value": val})

    top_category = max(categories, key=lambda x: x["value"])["name"] if categories else "-"

    budget_data = get_budget_vs_actual(db, company_id, month, year)
    budget_vs_actual = [
        {
            "category": b[0],
            "budget": float(b[1]),
            "spent": float(b[2]),
            "remaining": float(b[1] - b[2])
        } for b in budget_data
    ]

    recent_expenses = db.query(Expense, Category.name).join(
        Category, Expense.category_id == Category.category_id
    ).filter(Expense.company_id == company_id).order_by(Expense.created_at.desc()).limit(5).all()

    return {
        "total_expenses": total,
        "categories": categories,
        "top_category": top_category,
        "budget_vs_actual": budget_vs_actual,
        "recent_expenses": [
            {
                "amount": float(e[0].amount),
                "description": e[0].description or "",
                "date": str(e[0].expense_date),
                "category": e[1],
                "status": e[0].status.value if hasattr(e[0].status, 'value') else str(e[0].status)
            } for e in recent_expenses
        ]
    }