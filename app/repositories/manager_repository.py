from sqlalchemy.orm import Session
from app.models.manager import Manager


def create_manager(db: Session, manager_data: dict):
    manager = Manager(**manager_data) #unpacking dic
    db.add(manager)
    db.commit()
    db.refresh(manager)

    return manager


def get_managers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Manager).offset(skip).limit(limit).all()

def get_manager_by_id(db: Session, manager_id: int):
    return db.query(Manager).filter(Manager.manager_id == manager_id).first()

def update_manager(db: Session, db_manager, update_data: dict):
    for key, value in update_data.items():
        setattr(db_manager, key, value)

    db.commit()
    db.refresh(db_manager)
    return db_manager


def delete_manager(db: Session, manager):
    db.delete(manager)
    db.commit()

    return manager


def get_manager_by_email(db: Session, email: str):
    return db.query(Manager).filter(Manager.email == email).first()