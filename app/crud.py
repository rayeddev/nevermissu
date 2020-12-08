from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_persons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Person).offset(skip).limit(limit).all()

def get_user_persons(db: Session, user_id:int, skip: int = 0, limit: int = 100):
    return db.query(models.Person).filter(models.Person.owner_id == user_id).offset(skip).limit(limit).all()    

def get_user_events(db: Session, user_id:int, skip: int = 0, limit: int = 100):
    return db.query(models.Event).filter(models.Event.owner_id == user_id).offset(skip).limit(limit).all()    


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()    


def create_user_person(db: Session, person: schemas.PersonCreate, user_id: int):
    db_person = models.Person(**person.dict(), owner_id=user_id)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person


def create_user_event(db: Session, event: schemas.EventCreate, user_id: int, person_id: int):
    db_event = models.Event(**event.dict(), owner_id=user_id,person_id=person_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event    