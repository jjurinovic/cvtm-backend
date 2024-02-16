from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, DateTime, Boolean
from .database import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True, index=True)
    address1 = Column(String)
    address2 = Column(String, nullable=True)
    city = Column(String)
    county = Column(String, nullable=True)
    postcode = Column(String)
    country = Column(String)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    company_id = Column(Integer, ForeignKey(
        "companies.id", ondelete="CASCADE"), nullable=True)
    company = relationship("Company", back_populates="users")
    role = Column(Integer)
    address_id = Column(Integer, ForeignKey("addresses.id"))
    address = relationship("Address", cascade="all, delete")
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime)
    password_changed = Column(Boolean)
    deleted = Column(Boolean, default=False)
    inactive = Column(Boolean, default=False)
    updated_by = Column(Integer)


class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    vat = Column(String)
    address_id = Column(Integer, ForeignKey("addresses.id"))
    address = relationship("Address", cascade="all,delete")
    inactive = Column(Boolean, default=False)
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime)
    updated_by = Column(Integer)
    users = relationship("User", cascade="all,delete",
                         back_populates="company")


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
    title = Column(String)
    date = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
