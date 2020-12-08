from datetime import datetime
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import date


from ..database import Base
from ..main import app, get_db
from ..models import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

test_active_user: int = None
test_active_person: int = None


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()



app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hi there,signup start adding your loved ones !!"}


def test_create_user():
    global test_active_user
    response = client.post("/users",
    json={
        "email":"missu1@gmail.com",
        "password":"123456",
    })
    
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "missu1@gmail.com"
    assert "id" in data
    user_id = data["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "missu1@gmail.com"
    assert data["id"] == user_id
    test_active_user =  user_id



def test_create_user_person():
    global test_active_person
    owner_id :int = test_active_user
    response = client.post(f"/users/{owner_id}/persons",
    json={
        "relation":"brother",
        "gender":"male",
        "interests": "electronics, perfumes",
        "owner_id": owner_id
    })
    
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["relation"] == "brother"
    assert data["gender"] == "male"
    assert data["interests"] == "electronics, perfumes"
    assert data["owner_id"] == owner_id
    assert "id" in data
    test_active_person = data["id"]

    response = client.get(f"/users/{owner_id}/persons")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) > 0
    

def test_create_user_event():
    owner_id :int = test_active_user
    person_id :int = test_active_person
    response = client.post(f"/users/{owner_id}/presons/{person_id}/events",
    json={
        "upcomming_date": str(date.today()),
        "repeat_every":"year",
        "event_type": "birthdate"
    })
    
    
    assert response.status_code == 200, response.text
    data = response.json()    
    assert data["upcomming_date"] == str(date.today())
    assert data["repeat_every"] == "year"
    assert data["event_type"] == "birthdate"
    assert data["owner_id"] == owner_id
    assert data["person_id"] == person_id
    assert "id" in data

    response = client.get(f"/users/{owner_id}/events")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) > 0
        
    
    
    