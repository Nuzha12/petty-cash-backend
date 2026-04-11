from sqlalchemy.orm import Session
from app.repositories.dashboard_repository import get_dashboard_data

def get_dashboard(db: Session, manager, month: int, year: int):
    return get_dashboard_data(db, manager.company_id, month, year)