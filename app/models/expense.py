import enum
from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Numeric, Text, DateTime, Date, Enum
from sqlalchemy.orm import relationship

from app.database import Base

class ExpenseStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class Expense(Base):

    __tablename__ = "expenses"

    expense_id = Column(Integer, primary_key=True, index=True)

    company_id = Column(Integer, ForeignKey("companies.company_id"), nullable=False)

    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)

    manager_id = Column(Integer, ForeignKey("managers.manager_id"), nullable=False)

    amount = Column(Numeric(10, 2), nullable=False)

    description = Column(Text)

    expense_date = Column(Date, nullable= False)

    status = Column(
        Enum(ExpenseStatus),
        default=ExpenseStatus.pending,
        nullable=False
    )

    created_at = Column( DateTime, default=datetime.utcnow )

    company = relationship("Company")
    category = relationship("Category")
    manager = relationship("Manager")


