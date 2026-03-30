from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import verify_token
from app.services.dashboard_service import get_dashboard

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("")
def dashboard(
    month: int,
    year: int,
    db: Session = Depends(get_db),
    manager = Depends(verify_token)
):
    return get_dashboard(db, manager, month, year)