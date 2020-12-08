from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    persons = relationship("Person", back_populates="owner")
    events = relationship("Event", back_populates="owner")

class Person(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True, index=True)
    relation = Column(String)
    gender = Column(String)
    interests = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="persons")
    events = relationship("Event", back_populates="person")
    

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    upcomming_date = Column(Date, index=True)
    repeat_every = Column(String)
    event_type = Column(String, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"))    
    owner_id = Column(Integer, ForeignKey("users.id"))

    person = relationship("Person", back_populates="events")
    owner = relationship("User", back_populates="events")    