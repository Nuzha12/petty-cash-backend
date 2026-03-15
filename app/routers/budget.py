from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import verify_token
from app.database import get_db
from app.schemas.budget import BudgetResponse, BudgetCreate
from app.services import budget_service

router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.post("/", response_model=BudgetResponse)
def create_budget(budget: BudgetCreate, db: Session = Depends(get_db), manager= Depends(verify_token)):
    return budget_service.create_budget(db, budget, manager)


@router.get("/", response_model=list[BudgetResponse])
def get_budgets(db: Session = Depends(get_db), manager = Depends(verify_token)):
    return budget_service.get_budgets(db, manager)


@router.delete("/{budget_id}")
def delete_budget(budget_id: int, db: Session = Depends(get_db), manager=Depends(verify_token)):
    budget_service.delete_budget(db, budget_id, manager)

    return {"message": "Budget deleted successfully"}