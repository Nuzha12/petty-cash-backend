import csv
import io

from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.repositories import report_repository
from app.models.expense import Expense, ExpenseStatus
from app.models.category import Category
from app.schemas.report_schema import MonthlySummary, CategoryReport, BudgetReport, DailyReport


def get_unified_report(db: Session, manager, report_type: str, month: int, year: int, date_str: str = None):
    query = db.query(
        Expense.expense_date,
        Category.name.label("category_name"),
        Expense.amount,
        Expense.description,
        Expense.status
    ).join(Category, Expense.category_id == Category.category_id).filter(
        Expense.company_id == manager.company_id,
        Expense.status == ExpenseStatus.approved
    )

    if report_type == "daily" and date_str:
        query = query.filter(func.date(Expense.expense_date) == date_str)
    elif report_type == "monthly":
        query = query.filter(extract("month", Expense.expense_date) == month,
                             extract("year", Expense.expense_date) == year)
    elif report_type == "annual":
        query = query.filter(extract("year", Expense.expense_date) == year)

    results = query.order_by(Expense.expense_date.desc()).all()

    transactions = [
        {
            "date": str(r[0]),
            "category": r[1],
            "amount": float(r[2]),
            "description": r[3] or "No description",
            "status": r[4].value if hasattr(r[4], 'value') else str(r[4])
        } for r in results
    ]

    return {
        "total_expenses": float(sum(r[2] for r in results)),
        "transactions": transactions
    }


def generate_monthly_csv(db: Session, company_id: int, month: int, year: int):
    data = db.query(Expense.expense_date, Category.name, Expense.amount, Expense.description) \
        .join(Category).filter(Expense.company_id == company_id,
                               extract("month", Expense.expense_date) == month,
                               extract("year", Expense.expense_date) == year).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Category", "Amount", "Description"])
    for r in data:
        writer.writerow(r)
    return output.getvalue()
def get_monthly_summary(db: Session, manager, month: int, year: int):
    total = report_repository.get_total_expenses(db, manager.company_id, month, year)
    return MonthlySummary(month=month, year=year, total_expenses=float(total or 0))

def get_category_report(db: Session, manager, month: int, year: int):
    data = report_repository.get_category_expenses(db, manager.company_id, month, year)
    return [CategoryReport(category=row.category, total=float(row.total)) for row in data]

def get_budget_report(db: Session, manager, month: int, year: int):
    data = report_repository.get_budget_vs_actual(db, manager.company_id, month, year)
    return [
        BudgetReport(
            category=row.category,
            budget=float(row.budget),
            spent=float(row.spent),
            remaining=float(row.budget - row.spent)
        ) for row in data
    ]

def get_daily_report(db: Session, manager, month: int, year: int):
    data = report_repository.get_daily_expenses(db, manager.company_id, month, year)
    return [DailyReport(date=str(row.date), total=float(row.total)) for row in data]