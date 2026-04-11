
from pydantic import BaseModel


class MonthlySummary(BaseModel):
    month: int
    year: int
    total_expenses: float

class CategoryReport(BaseModel):
    category: str
    total: float

class BudgetReport(BaseModel):
    category: str
    budget: float
    spent: float
    remaining: float

class DailyReport(BaseModel):
    date: str
    total: float
