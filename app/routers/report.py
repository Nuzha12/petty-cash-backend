from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import verify_token
from app.database import get_db
from app.services import report_service

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/summary")
def get_summary(month: int, year: int, db: Session= Depends(get_db), manager=Depends(verify_token)):
    return report_service.get_monthly_summary(db, manager, month, year)

@router.get("/category")
def get_category_report(month: int, year: int, db: Session= Depends(get_db), manager= Depends(verify_token)):
    return report_service.get_category_report(db, manager, month, year)

@router.get("/budget")
def get_budget_report(month: int, year: int, db: Session= Depends(get_db), manager= Depends(verify_token)):
    return report_service.get_budget_report(db, manager, month, year)