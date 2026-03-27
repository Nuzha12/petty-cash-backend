from sqlalchemy.orm import Session
from app.repositories import report_repository


def get_dashboard(db: Session, manager, month: int, year: int):
    total = report_repository.get_total_expenses(
        db, manager.company_id, month, year
    )

    categories = report_repository.get_category_expenses(
        db, manager.company_id, month, year
    )

    category_list = [
        {
            "category": c.category if c.category else "Uncategorized",
            "total": float(c.total or 0.0)
        }
        for c in categories
    ]

    top_category = None
    if category_list:
        top_category = max(category_list, key=lambda x: x["total"])["category"]

    return {
        "total_expenses": float(total or 0.0),
        "categories": category_list,
        "top_category": top_category
    }