
import os
import logging
from typing import Union
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, ExpiredSignatureError, JWTError

logger = logging.getLogger("auth")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

security = HTTPBearer(auto_error=False)


class TokenData:
    def __init__(self, manager_id: int, company_id: int):
        self.manager_id = manager_id
        self.company_id = company_id


def verify_token(
    credentials: Union[HTTPAuthorizationCredentials, str, None] = Depends(security)
):
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if isinstance(credentials, str):
        token = credentials
    else:
        token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        return TokenData(
            manager_id=payload.get("manager_id"),
            company_id=payload.get("company_id"),
        )

    except ExpiredSignatureError:
        logger.error("Token expired")
        raise HTTPException(status_code=401, detail="Token expired")

    except JWTError:
        logger.error("Invalid token")
        raise HTTPException(status_code=401, detail="Invalid token")
