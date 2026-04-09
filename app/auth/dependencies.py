import os

from fastapi import Request, HTTPException
from jose import jwt

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


class TokenData:
    def __init__(self, manager_id: int, company_id: int):
        self.manager_id = manager_id
        self.company_id = company_id


def verify_token(request: Request):

    auth_header = request.headers.get("Authorization")

    print("HEADER RECEIVED:", auth_header)

    if not auth_header:
        raise HTTPException(status_code=401, detail="Token missing")

    token = auth_header.replace("Bearer ", "").strip()

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    return TokenData(
        manager_id=payload.get("manager_id"),
        company_id=payload.get("company_id"),
    )