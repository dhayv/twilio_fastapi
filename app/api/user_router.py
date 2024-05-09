from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from model import User
from database import get_db

router = APIRouter()


# Add a new sms user to db no need to check if your users already exist
@router.post("/users/", response_model=)
def add_user(phone_num: str, db: Session = Depends(get_db)):
    user = User(phone_number=phone_num)
    db.add(user)
    db.commit()
    db.refresh(user)
    return  {"id": user.id, "phone_number": user.phone_number}

# Retrieve user info from db 
@router.get("/users/{phone_number}", response_model=)
def read_user(phone_num, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone_number == phone_num).first()
    return user