from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt

from app.database import get_db
from app.models.manager import Manager
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def verify_token(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        manager_id: int = payload.get("manager_id")

        if manager_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    manager = db.query(Manager).filter(
        Manager.manager_id == manager_id
    ).first()

    if manager is None:
        raise HTTPException(status_code=401, detail="Manager not found")

    return manager