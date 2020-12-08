from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.get("/")
async def root():
    return {"message": "Hi there,signup start adding your loved ones !!"}


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/persons", response_model=schemas.Person)
def create_user_person(
    user_id: int, person: schemas.PersonCreate, db: Session = Depends(get_db)
):
    return crud.create_user_person(db=db, person=person, user_id=user_id)

@app.get("/users/{user_id}/persons", response_model=List[schemas.Person])
def read_user_persons(user_id: int, db: Session = Depends(get_db)):
    db_user_persons = crud.get_user_persons(db, user_id=user_id)
    if db_user_persons is None:
        raise HTTPException(status_code=404, detail="no Persons found for user")
    return db_user_persons


@app.post("/users/{user_id}/presons/{person_id}/events", response_model=schemas.Event)
def create_user_event(
    user_id: int, person_id: int, event: schemas.EventCreate, db: Session = Depends(get_db)
):
    return crud.create_user_event(db=db, event=event, user_id=user_id,person_id=person_id)



@app.get("/users/{user_id}/events", response_model=List[schemas.Event])
def read_user_events(user_id: int, db: Session = Depends(get_db)):
    db_user_events = crud.get_user_events(db, user_id=user_id)
    if db_user_events is None:
        raise HTTPException(status_code=404, detail="no events found for user")
    return db_user_events


@app.get("/persons", response_model=List[schemas.Person])
def read_persons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    persons = crud.get_persons(db, skip=skip, limit=limit)
    return persons


@app.get("/events", response_model=List[schemas.Event])
def read_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = crud.get_events(db, skip=skip, limit=limit)
    return events