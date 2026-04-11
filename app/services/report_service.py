from sqlalchemy.orm import Session
from app.repositories import report_repository
from app.schemas.report_schema import MonthlySummary, CategoryReport, BudgetReport, DailyReport


def get_unified_report(db: Session, manager, type: str, month: int, year: int, target_date: str = None):
    company_id = manager.company_id

    if target_date:
        cat_data = report_repository.get_specific_date_expenses(db, company_id, target_date)
        total = sum(row.total for row in cat_data)
        categories = [
            {"category": row.category, "total": float(row.total)}
            for row in cat_data
        ]

    elif type == "daily":
        data = report_repository.get_daily_expenses(db, company_id, month, year)
        total = sum(row.total for row in data)
        categories = [{"category": str(row.date), "total": float(row.total)} for row in data]

    elif type == "annual":
        total = report_repository.get_annual_expenses(db, company_id, year)
        cat_data = report_repository.get_annual_category_expenses(db, company_id, year)
        categories = [{"category": row.category, "total": float(row.total)} for row in cat_data]

    else:
        total = report_repository.get_total_expenses(db, company_id, month, year)
        cat_data = report_repository.get_category_expenses(db, company_id, month, year)
        categories = [{"category": row.category, "total": float(row.total)} for row in cat_data]

    return {
        "total_expenses": float(total or 0),
        "categories": categories
    }

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