from sqlalchemy.orm import Session

from app.repositories import report_repository


def get_monthly_summary(db: Session, manager, month: int, year: int):
    total = report_repository.get_total_expenses(db, manager.company_id, month, year)

    return {"month": month, "year": year, "total_expenses": total}


def get_category_report(db: Session, manager, month: int, year: int):
    data = report_repository.get_category_expenses(db, manager.company_id, month, year)

    return [
            {"category": row[0], "total": row[1]}
            for row in data
        ]


def get_budget_report(db: Session, manager, month: int, year: int):
    data = report_repository.get_budget_vs_actual(db, manager.company_id, month, year)

    return [
        {
            "category": row[0],
            "budget": row[1],
            "spent": row[2],
            "remaining": row[1] - row[2]
        }
        for row in data
    ]