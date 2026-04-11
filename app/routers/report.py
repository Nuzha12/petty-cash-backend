from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.auth.dependencies import verify_token
from app.database import get_db
from app.services import report_service

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/")
def get_unified_report(
    type: str = Query("monthly"),
    month: int = Query(1, ge=1, le=12),
    year: int = Query(2026),
    date: str = Query(None),
    db: Session = Depends(get_db),
    manager = Depends(verify_token)
):
    return report_service.get_unified_report(db, manager, type, month, year, date)

@router.get("/monthly-summary")
def monthly_summary(month: int, year: int, db: Session = Depends(get_db), manager=Depends(verify_token)):
    return report_service.get_monthly_summary(db, manager, month, year)

@router.get("/category")
def category_report(month: int, year: int, db: Session= Depends(get_db), manager= Depends(verify_token)):
    return report_service.get_category_report(db, manager, month, year)

@router.get("/budget")
def budget_report(month: int, year: int, db: Session= Depends(get_db), manager= Depends(verify_token)):
    return report_service.get_budget_report(db, manager, month, year)

@router.get("/daily")
def daily_report(month: int, year: int, db: Session = Depends(get_db), manager = Depends(verify_token)):
    return report_service.get_daily_report(db, manager, month, year)