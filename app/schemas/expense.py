from datetime import date, datetime
from decimal import Decimal

from pydantic import Field, ConfigDict, BaseModel

from app.models.expense import ExpenseStatus


class ExpenseBase(BaseModel):
    category_id: int
    amount: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    description: str | None = None
    expense_date: date

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(BaseModel):
    amount: Decimal | None = None
    description: str | None = None
    expense_date: date | None = None

class ExpenseResponse(ExpenseBase):
    expense_id: int
    company_id: int
    manager_id: int
    status: ExpenseStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

