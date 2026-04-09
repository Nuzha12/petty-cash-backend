from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import verify_token, TokenData
from app.database import get_db
from app.schemas.manager import ManagerResponse, ManagerCreate, ManagerUpdate
from app.services import manager_service

router = APIRouter(prefix="/managers", tags=["managers"])


@router.post("/", response_model=ManagerResponse)
def create_manager(
    manager: ManagerCreate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(verify_token)
):
    return manager_service.create_manager(db, manager, current_user.company_id)


@router.get("/", response_model=list[ManagerResponse])
def get_managers(
    skip: int = 0,
    limit: int = Query(default=100, le=100),
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(verify_token)
):
    return manager_service.get_managers(db, current_user.company_id, skip, limit)


@router.get("/{manager_id}", response_model=ManagerResponse)
def get_manager(
    manager_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(verify_token)
):
    return manager_service.get_manager(db, manager_id, current_user.company_id)


@router.patch("/{manager_id}", response_model=ManagerResponse)
def update_manager_partial(
    manager_id: int,
    manager: ManagerUpdate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(verify_token)
):
    return manager_service.update_manager_partial(
        db,
        manager_id,
        manager,
        current_user.company_id
    )


@router.put("/{manager_id}", response_model=ManagerResponse)
def update_manager_full(
    manager_id: int,
    manager: ManagerCreate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(verify_token)
):
    return manager_service.update_manager_full(
        db,
        manager_id,
        manager,
        current_user.company_id
    )


@router.delete("/{manager_id}")
def delete_manager(
    manager_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(verify_token)
):
    manager_service.delete_manager(db, manager_id, current_user.company_id)

    return {"message": "Manager deleted successfully"}