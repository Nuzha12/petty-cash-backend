from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.dependencies import verify_token
from app.database import get_db
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from app.services import expense_service

router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.post("/")
def add_expense(expense: ExpenseCreate, db: Session = Depends(get_db), manager=Depends(verify_token)):
    return expense_service.create_expense(db, expense, manager)

@router.get("/")
def list_expenses(db: Session = Depends(get_db), manager=Depends(verify_token)):
    return expense_service.get_expenses(db, manager)

@router.patch("/{expense_id}")
def update_expense(expense_id: int, expense: ExpenseUpdate, db: Session = Depends(get_db), manager=Depends(verify_token)):
    return expense_service.update_expense(db, expense_id, expense, manager)

@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db), manager=Depends(verify_token)):
    expense_service.delete_expense(db, expense_id, manager)
    return {"message": "deleted"}

@router.patch("/{expense_id}/approve")
def approve(expense_id: int, db: Session = Depends(get_db), manager=Depends(verify_token)):
    return expense_service.approve_expense(db, expense_id, manager)

@router.patch("/{expense_id}/reject")
def reject(expense_id: int, db: Session = Depends(get_db), manager=Depends(verify_token)):
    return expense_service.reject_expense(db, expense_id, manager)