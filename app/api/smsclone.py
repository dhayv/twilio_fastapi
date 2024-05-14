import os

from database import get_db
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status, Request
from model import Message, MessageDirection, User
from openai import OpenAI
from sqlalchemy.orm import Session
from twilio.rest import Client
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

import openai

load_dotenv()

router = APIRouter()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_NUMBER")
openai.api_key = os.getenv("OPENAI_API_KEY")

client = Client(account_sid, auth_token)

client = OpenAI()
# defaults to getting the key using


@router.post("sms/receive", response_model=MessagingResponse)
async def receive_sms(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    from_number = form_data.get('From', None)
    body = form_data.get('Body', None)

    if not all([from_number, body]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing Message Details")

    validator = RequestValidator(auth_token)
    if not validator.validate(
        str(request.url),
        form_data,
        request.headers.get("X-Twilio-Signature", "")
    ):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Twilio Signature")

    # Validate input parameters
    if not all(from_number.startswith("+")):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input parameters")

    if not all([account_sid, auth_token]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing API keys")

    # Check if user exists or create a new one
    user = db.query(User).filter(User.phone_number == from_number).first()
    if not user:
        user = User(phone_number=from_number)  # Assuming User has a phone_number field
        db.add(user)
        db.commit()
        db.refresh(user)

    # Log message via Twilio
    log_message = Message(
        user_id=user.id,
        message=body,
        direction=MessageDirection.INCOMING
    )

    db.add(log_message)
    db.commit()
    db.refresh(log_message)

    response = MessagingResponse()
    return response.message("Thank you for your message. We will get back to you shortly!")


@router.post("sms/send{user_id}", response_model=MessagingResponse)
async def send_response(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # pull latest user mesage from databse pass to ai
    user_message = db.query(Message).filter(
        Message.user_id == user_id,
        Message.direction == MessageDirection.OUTGOING,
        ).order_by(Message.id.desc()).first()

    # generate ai repsponse
    completion = openai.completions.create(
        model="text-davinci-003",
        prompt=user_message.message,
        max_tokens=150
    )

    ai_response = completion.choices[0].text.strip()

    # send response to user via Twilio
    try:

        sent_message = client.messages.create(
            body=ai_response,
            to=user.phone_number,
            from_=twilio_number,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # log message to database
    log_message = Message(
        body=ai_response,
        user_id=user.id,
        direction=MessageDirection.OUTGOING,
    )

    db.add(log_message)
    db.commit()
    db.refresh(log_message)

    return log_message
