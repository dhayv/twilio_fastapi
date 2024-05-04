from data_base.dbcore import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from model import User

router = APIRouter


@router.post("/users/", response_model=User)
def add_user(db: Session = Depends(get_db)):
    pass


@router.get("/users/{user_id}", response_model=User)
def read_user(db: Session = Depends(get_db)):
    pass
