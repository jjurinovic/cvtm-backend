from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean, Table
from sqlalchemy.orm import relationship

from ..database import Base
from datetime import datetime

project_users = Table('project_users', Base.metadata,
                      Column('project_id', ForeignKey(
                          'projects.id'), primary_key=True),
                      Column('user_id', ForeignKey(
                          'users.id'), primary_key=True)
                      )


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(type_=String, nullable=True)
    company_id = Column(Integer, ForeignKey(
        "companies.id"), nullable=True)
    users = relationship("User", secondary="project_users",
                         back_populates="projects")
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    estimated_date = Column(DateTime)
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime)
    updated_by = Column(Integer)
    password_changed = Column(Boolean)
    active = Column(Boolean, default=True)
