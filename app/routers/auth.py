from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import LoginRequest, ForgotPasswordRequest, ResetPasswordRequest
from app.services.auth_service import login, forgot_password, reset_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login_user(data: LoginRequest, db: Session = Depends(get_db)):
    return login(db, data.email, data.password)


@router.post("/forgot-password")
def forgot(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    return forgot_password(db, data.email)


@router.post("/reset-password")
def reset(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    return reset_password(db, data.email, data.new_password)