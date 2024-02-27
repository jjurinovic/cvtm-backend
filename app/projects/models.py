from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from ..database import Base
from datetime import datetime


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(type_=String, nullable=True)
    company_id = Column(Integer, ForeignKey(
        "companies.id"), nullable=True)
    users = relationship("User", back_populates="company")
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    estimated_date = Column(DateTime)
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime)
    updated_by = Column(Integer)
    password_changed = Column(Boolean)
    active = Column(Boolean, default=True)
