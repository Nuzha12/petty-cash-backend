import io
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse

from app.auth.dependencies import verify_token, TokenData
from app.database import get_db
from app.services import report_service

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/")
def get_unified_report(
        type: str = Query("monthly"),
        month: int = Query(None),
        year: int = Query(None),
        date: str = Query(None),
        db: Session = Depends(get_db),
        manager: TokenData = Depends(verify_token)
):
    now = datetime.now()
    r_month = month or now.month
    r_year = year or now.year
    return report_service.get_unified_report(db, manager, type, r_month, r_year, date)


@router.get("/monthly-summary")
def monthly_summary(month: int, year: int, db: Session = Depends(get_db), manager: TokenData = Depends(verify_token)):
    return report_service.get_monthly_summary(db, manager, month, year)


@router.get("/category")
def category_report(month: int, year: int, db: Session = Depends(get_db), manager: TokenData = Depends(verify_token)):
    return report_service.get_category_report(db, manager, month, year)


@router.get("/budget")
def budget_report(month: int, year: int, db: Session = Depends(get_db), manager: TokenData = Depends(verify_token)):
    return report_service.get_budget_report(db, manager, month, year)


@router.get("/daily")
def daily_report(month: int, year: int, db: Session = Depends(get_db), manager: TokenData = Depends(verify_token)):
    return report_service.get_daily_report(db, manager, month, year)


@router.get("/download")
def download_report(
        month: int,
        year: int,
        db: Session = Depends(get_db),
        manager: TokenData = Depends(verify_token)
):
    csv_data = report_service.generate_monthly_csv(
        db, manager.company_id, month, year
    )

    return StreamingResponse(
        io.StringIO(csv_data),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=report_{month}_{year}.csv",
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )