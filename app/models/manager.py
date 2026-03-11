
from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class Manager(Base):
    __tablename__ = "managers"

    manager_id = Column(Integer, primary_key=True, index=True)

    company_id = Column(Integer,ForeignKey("companies.company_id"), nullable=False)

    name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True)
    password = Column(String(255), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()

    )

    company = relationship("Company", backref="managers")