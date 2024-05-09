from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from model import User
from database import get_db
from schemas import UserCreate, UserResponse

router = APIRouter()


# Add a new sms user to db no need to check if your users already exist
@router.post("/users/", response_model=UserResponse)
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    user = User(phone_number=user.phone_number)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# Retrieve user info from db
@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    fetched_user = db.query(User).filter(User.id == user_id).first()
    return fetched_user
