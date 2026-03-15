from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    return auth_service.login(
        db,
        form_data.username,
        form_data.password
    )