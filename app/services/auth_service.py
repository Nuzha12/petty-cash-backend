from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.manager import Manager
from app.auth.jwt_handler import create_access_token
from app.core.security import verify_password, hash_password


def login(db: Session, email: str, password: str):
    manager = db.query(Manager).filter(
        Manager.email == email
    ).first()

    if not manager:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(password, manager.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "manager_id": manager.manager_id,
        "company_id": manager.company_id
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


def forgot_password(db: Session, email: str):
    user = db.query(Manager).filter(Manager.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    return {"message": "User verified"}


def reset_password(db: Session, email: str, new_password: str):
    if len(new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    user = db.query(Manager).filter(Manager.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = hash_password(new_password)
    db.commit()

    return {"message": "Password updated successfully"}