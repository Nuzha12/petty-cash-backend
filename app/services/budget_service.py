from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import budget_repository
from app.schemas.budget import BudgetCreate


def create_budget(db: Session, budget: BudgetCreate, manager):
    return budget_repository.create_budget(db, budget, manager.company_id)


def get_budgets(db: Session, manager):
    return budget_repository.get_budgets_by_company(db, manager.company_id)


def delete_budget(db: Session, budget_id: int, manager):
    budget = budget_repository.get_budget(db, budget_id)

    if not budget:
        raise HTTPException(status_code=404, detail= "Budget not found")

    if budget.company_id != manager.company_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    budget_repository.delete_budget(db, budget)
