from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Manager
from app.auth.jwt_handler import create_access_token
from app.core.security import verify_password


def login(db: Session, email: str, password: str):

    manager = db.query(Manager).filter(
        Manager.email == email
    ).first()

    if not manager:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(password, manager.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "manager_id": manager.manager_id
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }