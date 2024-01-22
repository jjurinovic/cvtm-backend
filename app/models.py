from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time
from .database import Base
from sqlalchemy.orm import relationship


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
    name = Column(String)
    email = Column(String)
    password = Column(String)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    role = Column(Integer)
    address_id = Column(Integer, ForeignKey("addresses.id"))
    address = relationship("Address")


class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    vat = Column(String)
    address_id = Column(Integer, ForeignKey("addresses.id"))
    address = relationship("Address", backref="companies")


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
