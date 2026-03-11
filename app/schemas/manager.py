from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class ManagerBase(BaseModel):
    company_id: int
    name: str
    email: EmailStr


class ManagerCreate(ManagerBase):
    password: str

class ManagerUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None

class ManagerResponse(ManagerBase):
    manager_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

