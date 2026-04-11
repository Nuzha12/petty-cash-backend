from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.auth.dependencies import verify_token
from app.database import get_db
from app.services.dashboard_service import get_dashboard

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/")
def dashboard(
    db: Session = Depends(get_db),
    manager=Depends(verify_token),
    month: int | None = None,
    year: int | None = None
):
    now = datetime.now()
    if month is None:
        month = now.month
    if year is None:
        year = now.year

    return get_dashboard(db, manager, month, year)