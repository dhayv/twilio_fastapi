from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()


@router.post("/users/")
def add_user(db: Session = Depends(get_db)):
    return {"message": "made"}


@router.get("/users/{user_id}")
def read_user(db: Session = Depends(get_db)):
    return {"message": "made"}
