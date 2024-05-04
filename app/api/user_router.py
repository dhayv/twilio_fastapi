from data_base.dbcore import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/users/")
def add_user(db: Session = Depends(get_db)):
    return {"message": "made"}


@router.get("/users/{user_id}")
def read_user(db: Session = Depends(get_db)):
    return {"message": "made"}
