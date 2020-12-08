from typing import List, Optional

from pydantic import BaseModel
from datetime import date


class EventBase(BaseModel):
    upcomming_date: date
    repeat_every: str
    event_type: str

class EventCreate(EventBase):
    pass 

class Event(EventBase):
    id: int
    person_id: int
    owner_id: int

    class Config:
        orm_mode = True



class PersonBase(BaseModel):
    relation: str
    gender: str
    interests: str


class PersonCreate(PersonBase):
    pass


class Person(PersonBase):
    id: int
    owner_id: int
    events: List[Event]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    persons: List[Person] = []
    events: List[Event] = []

    class Config:
        orm_mode = True