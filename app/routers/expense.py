from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import verify_token
from app.database import get_db
from app.schemas.expense import ExpenseResponse, ExpenseCreate, ExpenseUpdate
from app.services import expense_service

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("", response_model=ExpenseResponse)
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    manager=Depends(verify_token)
):
    return expense_service.create_expense(db, expense, manager)


@router.get("", response_model=list[ExpenseResponse])
def list_expenses(
    db: Session = Depends(get_db),
    manager=Depends(verify_token)
):
    return expense_service.get_expenses(db, manager)


@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db),
    manager=Depends(verify_token)
):
    return expense_service.get_dashboard_summary(db, manager)


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    manager=Depends(verify_token)
):
    return expense_service.get_expense(db, expense_id, manager)


@router.patch("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    db: Session = Depends(get_db),
    manager=Depends(verify_token)
):
    return expense_service.update_expense(db, expense_id, expense, manager)


@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    manager=Depends(verify_token)
):
    expense_service.delete_expense(db, expense_id, manager)
    return {"message": "Expense deleted"}


@router.patch("/{expense_id}/approve", response_model=ExpenseResponse)
def approve_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    manager=Depends(verify_token)
):
    return expense_service.approve_expense(db, expense_id, manager)


@router.patch("/{expense_id}/reject", response_model=ExpenseResponse)
def reject_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    manager=Depends(verify_token)
):
    return expense_service.reject_expense(db, expense_id, manager)