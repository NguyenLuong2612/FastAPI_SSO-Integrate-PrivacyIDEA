from fastapi import Depends, HTTPException
from sqlalchemy import DateTime, create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from fastapi import APIRouter
from logger_config import setup_logger

logger = setup_logger(__name__)

router = APIRouter()

DATABASE_URL = "mysql+pymysql://luongnv:123@10.128.0.19/mydb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Account(Base):
    __tablename__ = "account"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    create_at = Column(DateTime, default=datetime.utcnow)


class Person(Base):
    __tablename__ = "person"
    personid = Column(Integer, primary_key=True)
    email = Column(String)
    full_name = Column(String)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/user/")
def get_user(id: int, db: Session = Depends(get_db)):
    try:
        result = (
            db.query(Account.username, Person.email, Person.full_name)
            .join(Person, Account.id == Person.personid)
            .filter(Account.id == id)
            .first()
        )
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        logger.info(f"User {id} found")
        return {
            "id": id,
            "username": result.username,
            "email": result.email,
            "full_name": result.full_name,
        }
    except Exception as e:
        logger.error(f"Failed to get user: {id}")
        raise HTTPException(status_code=400, detail=str(e))

def add_user(username: str, data:Person, db: Session = Depends(get_db)):
    try:
        result = db.query(Account).filter(Account.username == username).first()
        if result:
            new_user = Person(personid=result.id,full_name=data.full_name,email=data.email)
            db.add(new_user)
            db.commit()
            logger.info(f"User {username} added successfully")
        else:
            logger.error(f"Error function >> [add_user]: User {username} not found")
            raise Exception("User not found")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to add user: {username}")
        raise Exception(str(e))
