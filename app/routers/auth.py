from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.jwt_handler import create_access_token
from app.database import get_db
from app.models.manager import Manager
from app.schemas.auth import LoginRequest, ForgotPasswordRequest, ResetPasswordRequest
from app.auth.password import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    manager = db.query(Manager).filter(Manager.email == data.email).first()

    if not manager:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(data.password, manager.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "manager_id": manager.manager_id,
        "company_id": manager.company_id
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


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