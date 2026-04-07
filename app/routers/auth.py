from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import hash_password
from app.database import get_db
from app.models import Manager
from app.schemas.auth import ForgotPasswordRequest, ResetPasswordRequest
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    return auth_service.login(
        db,
        form_data.username,
        form_data.password
    )

@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):

    user = db.query(Manager).filter(Manager.email == request.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    return {"message": "User verified"}

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):

    if len(request.new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    user = db.query(Manager).filter(Manager.email == request.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = hash_password(request.new_password)
    db.commit()

    return {"message": "Password updated successfully"}