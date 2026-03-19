from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException


from app.models.expense import Expense, ExpenseStatus
from app.models.budget import Budget
from app.repositories import expense_repository
from app.schemas.expense import ExpenseCreate, ExpenseUpdate


def create_expense(db: Session, expense: ExpenseCreate, manager):

    company_id = manager.company_id

    budget = db.query(Budget).filter(
        Budget.company_id == company_id,
        Budget.category_id == expense.category_id,
        Budget.month == expense.expense_date.month,
        Budget.year == expense.expense_date.year
    ).first()

    if not budget:
        raise HTTPException(status_code=400, detail="No budget set for this category/month")

    total_expenses = expense_repository.get_total_expenses_for_month(
        db,
        company_id,
        expense.category_id,
        expense.expense_date.month,
        expense.expense_date.year)

    if expense.amount > (budget.amount - total_expenses):
        raise HTTPException(status_code=400, detail="Budget exceeded")

    new_expense = Expense(
        company_id= company_id,
        manager_id= manager.manager_id,
        category_id= expense.category_id,
        amount= expense.amount,
        description= expense.description,
        expense_date= expense.expense_date
    )

    return expense_repository.create_expense(db, new_expense)


def get_expenses(db: Session, manager):
    return expense_repository.get_expenses_by_company(db, manager.company_id)


def get_expense(db: Session, expense_id: int, manager):
    expense = expense_repository.get_expense_by_id(
        db,
        expense_id,
        manager.company_id
    )

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    return expense


def update_expense(db: Session, expense_id: int, data: ExpenseUpdate, manager):
    expense = expense_repository.get_expense_by_id(db, expense_id, manager.company_id)

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    if expense.status!= ExpenseStatus.pending:
        raise HTTPException(status_code=400, detail="Only pending expenses can be updated")

    update_data = data.model_dump(exclude_unset=True)

    return expense_repository.update_expense(db, expense, update_data)



def delete_expense(db: Session, expense_id: int, manager):
    expense = expense_repository.get_expense_by_id(
        db,
        expense_id,
        manager.company_id
    )


    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    if expense.status != ExpenseStatus.pending:
        raise HTTPException(status_code=400, detail="Cannot delete approved and rejected expense")

    return expense_repository.delete_expense(db, expense)


def approve_expense(db: Session, expense_id: int, manager):
    expense = expense_repository.get_expense_by_id(db, expense_id, manager.company_id)

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    if expense.status != ExpenseStatus.pending:
        raise HTTPException(status_code=400, detail="Already processed")

    return expense_repository.update_expense_status(db, expense, ExpenseStatus.approved)


def reject_expense(db: Session, expense_id: int, manager):

    expense = expense_repository.get_expense_by_id(db, expense_id, manager.company_id)

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    if expense.status != ExpenseStatus.pending:
        raise HTTPException(status_code=400, detail="Already processed")

    return expense_repository.update_expense_status(db, expense, ExpenseStatus.rejected)
