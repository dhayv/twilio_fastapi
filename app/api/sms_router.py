import os

from database import get_db
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from model import Message, MessageDirection, User
from schemas import MessageCreate
from sqlalchemy.orm import Session
from twilio.rest import Client

load_dotenv()

router = APIRouter()


account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_NUMBER")


client = Client(account_sid, auth_token)


# User_id to identify the user to send sms
# User_id to to also log the messsage and the direction
@router.post("/sms/send/")
def send_sms(user_id: int, message_data: MessageCreate, db: Session = Depends(get_db)):

    try:
        sent_message = client.messages.create(
            from_=twilio_number,
            body=message_data.data,
            to=user.phone_number,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    log_message = Message(
        message=message_data.message,
        direction=MessageDirection.OUTGOING,
        user_id=user_id,
    )

    db.add(log_message)
    db.commit()
    db.refresh(log_message)

    return {"status": "Message sent", "sid": sent_message.sid}


@router.get("/sms/receive/{user_id}")
def fetch_sms(user_data: User, msg_info: Message, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    message = client.messages.create(
        from_=twilio_number,
        body=msg_info.message,
        to=user_data.phone_number,
    )

    print(message.sid)
