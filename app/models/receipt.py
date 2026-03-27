from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

from app.database import Base


class Receipt(Base):
    __tablename__ = "receipts"

    receipt_id = Column(Integer, primary_key=True, index=True)
    expense_id = Column(Integer, ForeignKey("expenses.expense_id"), nullable=False)
    file_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)