from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict

class BudgetBase(BaseModel):
    category_id: int
    amount: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=2024, le=2100)

class BudgetCreate(BudgetBase):
    pass

class BudgetResponse(BudgetBase):
    budget_id: int
    company_id: int
    category_name: str | None = None
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes = True)