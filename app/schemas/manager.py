from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict, Field


class ManagerBase(BaseModel):
    company_id: int
    name: str
    email: EmailStr


class ManagerCreate(ManagerBase):
    password: str = Field(..., min_length=6)

class ManagerUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = Field(..., min_length=6)

class ManagerResponse(ManagerBase):
    manager_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

