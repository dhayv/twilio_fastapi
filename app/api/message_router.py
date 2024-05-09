from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import MessageResponse
from database import get_db

router = APIRouter()


@router.post("/message/", response_model=MessageResponse)
def send_message(db: Session = Depends(get_db)):
    return {"message": "made"}


@router.get("/message/{message_id}", response_model=MessageResponse)
def retrieve_message(db: Session = Depends(get_db)):
    return {"message": "made"}
