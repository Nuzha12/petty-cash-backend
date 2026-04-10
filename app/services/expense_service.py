from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from app.models.expense import Expense, ExpenseStatus
from app.repositories import expense_repository
from app.repositories.budget_repository import get_budget_by_category


def create_expense(db: Session, expense, manager):
    budget = get_budget_by_category(
        db,
        expense.category_id,
        manager.company_id,
        expense.expense_date.month,
        expense.expense_date.year
    )

    if not budget:
        raise HTTPException(status_code=400, detail="Please set a budget for this category first")

    current_spent = expense_repository.get_total_expenses_for_month(
        db,
        manager.company_id,
        expense.category_id,
        expense.expense_date.month,
        expense.expense_date.year
    )

    if (current_spent + expense.amount) > budget.amount:
        raise HTTPException(status_code=400, detail="Budget exceeded")

    db_expense = Expense(
        company_id=manager.company_id,
        category_id=expense.category_id,
        manager_id=manager.manager_id,
        amount=expense.amount,
        description=expense.description,
        expense_date=expense.expense_date,
        status=ExpenseStatus.pending
    )

    return expense_repository.create_expense(db, db_expense)


def get_expenses(db, manager):
    rows = expense_repository.get_expenses_by_company(db, manager.company_id)

    return [
        {
            "expense_id": r[0].expense_id,
            "amount": float(r[0].amount),
            "description": r[0].description or "",
            "category": r[1],
            "status": r[0].status.value
        }
        for r in rows
    ]


def get_expense(db: Session, expense_id: int, manager):
    expense = expense_repository.get_expense_by_id(db, expense_id, manager.company_id)
    if not expense:
        raise HTTPException(404, "Expense not found")
    return expense


def update_expense(db: Session, expense_id: int, data, manager):
    expense = expense_repository.get_expense_by_id(db, expense_id, manager.company_id)

    if not expense:
        raise HTTPException(404, "Expense not found")

    if expense.status != ExpenseStatus.pending:
        raise HTTPException(400, "Only pending expenses can be updated")

    update_data = data.model_dump(exclude_unset=True)
    return expense_repository.update_expense(db, expense, update_data)


def delete_expense(db: Session, expense_id: int, manager):
    expense = expense_repository.get_expense_by_id(db, expense_id, manager.company_id)

    if not expense:
        raise HTTPException(404, "Expense not found")

    if expense.status != ExpenseStatus.pending:
        raise HTTPException(400, "Cannot delete approved/rejected expense")

    return expense_repository.delete_expense(db, expense)


def approve_expense(db: Session, expense_id: int, manager):
    expense = expense_repository.get_expense_by_id(db, expense_id, manager.company_id)

    if not expense:
        raise HTTPException(404, "Expense not found")

    if expense.status != ExpenseStatus.pending:
        raise HTTPException(400, "Already processed")

    return expense_repository.update_expense_status(db, expense, ExpenseStatus.approved)


def reject_expense(db: Session, expense_id: int, manager):
    expense = expense_repository.get_expense_by_id(db, expense_id, manager.company_id)

    if not expense:
        raise HTTPException(404, "Expense not found")

    if expense.status != ExpenseStatus.pending:
        raise HTTPException(400, "Already processed")

    return expense_repository.update_expense_status(db, expense, ExpenseStatus.rejected)


def get_dashboard_summary(db: Session, manager):
    now = datetime.now()
    expenses = expense_repository.get_expenses_by_company(db, manager.company_id)

    total_approved = sum(float(e[0].amount) for e in expenses if e[0].status == ExpenseStatus.approved)
    total_pending = sum(float(e[0].amount) for e in expenses if e[0].status == ExpenseStatus.pending)

    recent = expenses[:5]

    return {
        "total_expense": total_approved + total_pending,
        "month": f"{now.month}/{now.year}",
        "recent_transactions": [
            {
                "amount": float(e[0].amount),
                "description": e[0].description,
                "category": e[1],
                "status": e[0].status.value
            }
            for e in recent
        ]
    }