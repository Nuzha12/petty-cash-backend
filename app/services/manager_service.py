from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.manager import Manager
from app.repositories import manager_repository
from app.schemas.manager import ManagerCreate, ManagerUpdate


def create_manager(db: Session, manager: ManagerCreate):
    manager_data = manager.model_dump()

    manager_data["password"] = hash_password(manager_data["password"])

    return manager_repository.create_manager(db, manager_data)

def get_managers(db: Session, skip: int = 0, limit: int = 100):
    return manager_repository.get_managers(db, skip, limit)

def get_manager(db: Session, manager_id: int):
    manager = manager_repository.get_manager_by_id(db, manager_id)

    if not manager:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Manager not found")

    return manager

def update_manager_partial(db: Session, manager_id: int, manager: ManagerUpdate):
    db_manager = manager_repository.get_manager_by_id(db, manager_id)

    if not db_manager:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Manager not found")

    update_data = manager.model_dump(exclude_unset=True)


    # Hash password if updating
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])

    return manager_repository.update_manager(db, db_manager, update_data)


def update_manager_full(db: Session, manager_id: int, manager: ManagerCreate):
    db_manager = manager_repository.get_manager_by_id(db, manager_id)

    if not db_manager:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Manager not found")

    update_data = manager.model_dump()

    # Hash password
    if "password" in update_data and update_data["password"]:
        update_data["password"] = hash_password(update_data["password"])

    return manager_repository.update_manager(db, db_manager, update_data)


def delete_manager(db: Session, manager_id: int):
    manager = manager_repository.get_manager_by_id(db, manager_id)

    if not manager:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Manager not found")

    return manager_repository.delete_manager(db, manager)




