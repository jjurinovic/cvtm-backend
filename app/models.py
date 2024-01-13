from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time
from .database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    company_id = Column(Integer, ForeignKey("companies.id"))
    role = Column(String)


class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    vat = Column(String)


class Day(Base):
    __tablename__ = 'days'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    company_id = Column(Integer, ForeignKey("companies.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    entries = relationship("TimeEntry", backref="days")


class TimeEntry(Base):
    __tablename__ = 'time_entries'
    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(Time)
    end_time = Column(Time)
    day_id = Column(Integer, ForeignKey("days.id"))
    pause = Column(Integer)
    notes = Column(String)
