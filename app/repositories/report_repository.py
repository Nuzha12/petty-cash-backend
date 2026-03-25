from sqlalchemy import func, extract
from sqlalchemy.orm import Session

from app.models import Expense, Budget
from app.models.category import Category
from app.models.expense import ExpenseStatus


def get_total_expenses(db: Session, company_id: int, month: int, year: int):
    return db.query(
        func.coalesce(func.sum(Expense.amount),0)
    ).filter(
        Expense.company_id == company_id,
        extract("month", Expense.expense_date) == month,
        extract("year", Expense.expense_date) == year,
        Expense.status == ExpenseStatus.approved
    ).scalar()

# category wise expenses
def get_category_expenses(db: Session, company_id: int, month: int, year: int):
    return db.query(
        Category.name,
        func.coalesce(func.sum(Expense.amount), 0).label("total")
    ).join(Expense, Expense.category_id == Category.category_id) \
        .filter(
        Expense.company_id == company_id,
        extract("month", Expense.expense_date) == month,
        extract("year", Expense.expense_date) == year,
        Expense.status == ExpenseStatus.approved
    ) \
        .group_by(Category.name) \
        .all()


def get_budget_vs_actual(db: Session, company_id: int, month: int, year: int):
    return db.query(
        Category.name,
        Budget.amount.label("budget"),
        func.coalesce(func.sum(Expense.amount), 0).label("spent")
    ).join(Category, Category.category_id == Budget.category_id)\
     .outerjoin(
        Expense,
        (Expense.category_id == Budget.category_id) &
        (Expense.company_id == company_id) &
        (extract("month", Expense.expense_date) == month) &
        (extract("year", Expense.expense_date) == year) &
        (Expense.status == ExpenseStatus.approved)
    )\
     .filter(
        Budget.company_id == company_id,
        Budget.month == month,
        Budget.year == year
    )\
     .group_by(Category.name, Budget.amount)\
     .all()


