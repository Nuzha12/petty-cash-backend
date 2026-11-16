from sqlalchemy import func, extract
from sqlalchemy.orm import Session
from app.models import Expense, Budget
from app.models.category import Category
from app.models.expense import ExpenseStatus

def get_total_expenses(db: Session, company_id: int, month: int, year: int):
    return db.query(
        func.coalesce(func.sum(Expense.amount), 0)
    ).filter(
        Expense.company_id == company_id,
        extract("month", Expense.expense_date) == month,
        extract("year", Expense.expense_date) == year,
        Expense.status == ExpenseStatus.approved
    ).scalar()

def get_category_expenses(db: Session, company_id: int, month: int, year: int):
    return db.query(
        Category.name.label("category"),
        func.coalesce(func.sum(Expense.amount), 0).label("total")
    ).join(Expense, Expense.category_id == Category.category_id) \
    .filter(
        Expense.company_id == company_id,
        extract("month", Expense.expense_date) == month,
        extract("year", Expense.expense_date) == year,
        Expense.status == ExpenseStatus.approved
    ).group_by(Category.name).all()

def get_budget_vs_actual(db: Session, company_id: int, month: int, year: int):
    return db.query(
        Category.name.label("category"),
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
    ).filter(
        Budget.company_id == company_id,
        Budget.month == month,
        Budget.year == year
    ).group_by(Category.name, Budget.amount).all()

def get_annual_expenses(db: Session, company_id: int, year: int):
    return db.query(
        func.coalesce(func.sum(Expense.amount), 0)
    ).filter(
        Expense.company_id == company_id,
        extract("year", Expense.expense_date) == year,
        Expense.status == ExpenseStatus.approved
    ).scalar() # Changed to match get_total_expenses style

def get_annual_category_expenses(db: Session, company_id: int, year: int):
    return db.query(
        Category.name.label("category"),
        func.coalesce(func.sum(Expense.amount), 0).label("total")
    ).join(Expense, Expense.category_id == Category.category_id) \
    .filter(
        Expense.company_id == company_id,
        extract("year", Expense.expense_date) == year,
        Expense.status == ExpenseStatus.approved
    ).group_by(Category.name).all()

def get_daily_expenses(db: Session, company_id: int, month: int, year: int):
    return db.query(
        func.date(Expense.expense_date).label("date"),
        func.coalesce(func.sum(Expense.amount), 0).label("total")
    ).filter(
        Expense.company_id == company_id,
        extract("month", Expense.expense_date) == month,
        extract("year", Expense.expense_date) == year,
        Expense.status == ExpenseStatus.approved
    ).group_by(func.date(Expense.expense_date)).all()

def get_specific_date_expenses(db: Session, company_id: int, target_date: str):
    return db.query(
        Category.name.label("category"),
        func.coalesce(func.sum(Expense.amount), 0).label("total")
    ).join(Expense, Expense.category_id == Category.category_id) \
    .filter(
        Expense.company_id == company_id,
        func.date(Expense.expense_date) == target_date,
        Expense.status == ExpenseStatus.approved
    ).group_by(Category.name).all()


def get_detailed_report_data(db: Session, company_id: int, type: str, month: int, year: int, date_str: str = None):
    query = db.query(
        Expense.expense_date,
        Category.name.label("category_name"),
        Expense.amount,
        Expense.description,
        Expense.status
    ).join(Category, Expense.category_id == Category.category_id).filter(
        Expense.company_id == company_id,
        Expense.status == ExpenseStatus.approved
    )

    if type == "daily" and date_str:
        query = query.filter(Expense.expense_date == date_str)
    elif type == "monthly":
        query = query.filter(extract("month", Expense.expense_date) == month,
                             extract("year", Expense.expense_date) == year)
    elif type == "annual":
        query = query.filter(extract("year", Expense.expense_date) == year)

    results = query.order_by(Expense.expense_date.desc()).all()

    total = sum(r[2] for r in results)

    transactions = [
        {
            "date": str(r[0]),
            "category": r[1],
            "amount": float(r[2]),
            "description": r[3] or "No description",
            "status": r[4].value if hasattr(r[4], 'value') else str(r[4])
        } for r in results
    ]

    return {"total_expenses": float(total), "transactions": transactions}