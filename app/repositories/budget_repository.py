from sqlalchemy.orm import Session
from app.models.budget import Budget
from app.models.category import Category
from app.schemas.budget import BudgetCreate

def create_budget(db: Session, budget: BudgetCreate, company_id: int):
    db_budget = Budget(
        company_id = company_id,
        category_id = budget.category_id,
        amount = budget.amount,
        month = budget.month,
        year = budget.year
    )
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

def get_budgets_by_company(db: Session, company_id: int):
    return db.query(Budget).filter(Budget.company_id == company_id).all()

def get_budget(db: Session, budget_id: int):
    return db.query(Budget).filter(Budget.budget_id == budget_id).first()

def get_budget_by_category(db, category_id, company_id, month, year):
    return db.query(Budget).filter(
        Budget.category_id == category_id,
        Budget.company_id == company_id,
        Budget.month == month,
        Budget.year == year
    ).first()

def delete_budget(db: Session, budget: Budget):
    db.delete(budget)
    db.commit()