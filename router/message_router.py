from data_base.dbcore import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from model import Message

router = APIRouter


@router.post("/message/", response_model=Message)
def send_message(db: Session = Depends(get_db)):
    pass


@router.get("/message/{message_id}", response_model=Message)
def retrieve_message(db: Session = Depends(get_db)):
    pass
