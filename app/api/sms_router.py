import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from twilio.rest import Client

from database import get_db
from model import Message, User

load_dotenv()

router = APIRouter()


account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_NUMBER")


client = Client(account_sid, auth_token)


@router.post("/sms/")
def send_sms(
    user_data: User,
    msg_info: Message,
    db: Session = Depends(get_db)):
    message = client.messages.create(
        from_=twilio_number,
        body=msg_info.message,
        to=user_data.phone_number,
    )

    print(message.sid)
