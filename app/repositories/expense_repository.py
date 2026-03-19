from sqlalchemy import func, extract
from sqlalchemy.orm import Session

from app.models.expense import Expense, ExpenseStatus


def create_expense(db: Session, expense: Expense):
    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense


def get_expenses_by_company(db: Session, company_id: int):
    return db.query(Expense).filter(
        Expense.company_id == company_id
    ).order_by(Expense.created_at.desc()).all()

def get_expense_by_id(db: Session, expense_id: int, company_id: int):
    return db.query(Expense).filter(
        Expense.expense_id == expense_id,
        Expense.company_id == company_id
    ).first()

def delete_expense(db: Session, expense: Expense):
    db.delete(expense)
    db.commit()
    return expense


def get_total_expenses_for_month(db: Session, company_id: int, category_id: int, month: int, year: int):
    return  db.query(
        func.coalesce(func.sum(Expense.amount), 0)
    ).filter(
        Expense.company_id == company_id,
        Expense.category_id == category_id,
        extract("month", Expense.expense_date) == month,
        extract("year", Expense.expense_date) == year,
        Expense.status == ExpenseStatus.approved
    ).scalar()

def update_expense(db: Session, expense: Expense, update_date: dict):
    for key, value in update_date.items():
        setattr(expense, key, value)

    db.commit()
    db.refresh(expense)
    return expense

def update_expense_status(db: Session, expense: Expense, status: ExpenseStatus):
    expense.status = status
    db.commit()
    db.refresh(expense)
    return expense


