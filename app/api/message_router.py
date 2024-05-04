from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

router = APIRouter()


@router.post("/message/")
def send_message(db: Session = Depends(get_db)):
    return {"message": "made"}


@router.get("/message/{message_id}")
def retrieve_message(db: Session = Depends(get_db)):
    return {"message": "made"}
