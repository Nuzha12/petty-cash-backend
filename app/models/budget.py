from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Numeric, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship

from app.database import Base


class Budget(Base):
    __tablename__ = "budgets"

    budget_id = Column(Integer, primary_key= True, index=True)

    company_id = Column(Integer, ForeignKey("companies.company_id"), nullable= False)

    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)

    amount = Column(Numeric(10, 2), nullable=False)

    month = Column(Integer, nullable=False)

    year = Column(Integer, nullable=False)

    created_at = Column(DateTime, default= datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow,  onupdate=datetime.utcnow)


    __table_args__ = (UniqueConstraint("company_id", "category_id", "month", "year", name="unique_budget_per_month"),)

    company = relationship("Company")

    category = relationship("Category")

