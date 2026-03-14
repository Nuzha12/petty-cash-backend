from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    __table_args__ = (
        UniqueConstraint("company_id", "name", name="uq_company_category"),
    )


    category_id = Column(Integer, primary_key=True, index=True)

    company_id = Column(Integer, ForeignKey("companies.company_id"), nullable=False)

    name = Column(String(100), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    company = relationship("Company", backref="categories")