from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import MessageResponse, MessageCreate
from database import get_db
from model import Message

router = APIRouter()


@router.post("/messages/", response_model=MessageResponse)
def send_message(messages: MessageCreate, db: Session = Depends(get_db)):
    new_message = Message(
        message=messages.message,
        direction=messages.direction,
        user_id=messages.user_id)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message


@router.get("/message/{message_id}", response_model=MessageResponse)
def retrieve_message(message_id: int, db: Session = Depends(get_db)):
    statement = db.query(Message).filter(Message.id == message_id).first()
    if not statement:
        raise HTTPException(status_code=404, detail="Message not found")
    return statement
