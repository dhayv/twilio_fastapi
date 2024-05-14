import os

from database import get_db
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status, Request
from model import Message, MessageDirection, User
from openai import OpenAI
from schemas import MessageCreate, UserCreate
from sqlalchemy.orm import Session
from twilio.rest import Client
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

from openai import OpenAI
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


@router.post("sms/receive")
async def receive_sms(
    request: Request,
    to_number: str,
    from_number: str,
    message: str,
    body: str,
    db: Session = Depends(get_db)):

    message_sid = request.values.get('MessageSid', None)
    from_number = request.values.get('From', None)
    body = request.values.get('Body', None)

    if not all([message_sid, from_number, body]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing Message Details")

    validator = RequestValidator(os.environ["TWILIO_AUTH_TOKEN"])
    if not validator.validate(
        str(request.url),
        request.headers.get("X-Twilio-Signature", "")
    ):
        raise HTTPException(status_code=400, detail="Error in Twilio Signature")

    # Validate input parameters
    if not all(to_number.startswith("+") and from_number.startswith("+")):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input parameters")

    # Retrieve environment variables
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    openai_api_key = os.getenv("OPENAI_API_KEY")


    if not all([account_sid, auth_token, openai_api_key]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing API keys")

    # Initialize Twilio and OpenAI clients
    Client(account_sid, auth_token)
    openai.api_key = openai_api_key

    user = db.query(User).filter(User.phone_number == from_number).first()
    if not user:
        user = User(phone_number=from_number)  # Assuming User has a phone_number field
        db.add(user)
        db.commit()

    # Log message via Twilio
    log_message = Message(
        user_id=user.id,
        message=body,
        direction=MessageDirection.INCOMING
    )

    db.add(log_message)
    db.commit()

    return {
        "to_number": to_number,
        "from_number": from_number,
        "original_message": message,
        "response_message": response_message,
        "message_body": sent_message.body,
    }


@router.post("sms/send{user_id}")
async def send_response(user_id: int, user_message: str, response_message: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    twilio_number = os.getenv("TWILIO_NUMBER")


    client = Client(account_sid,auth_token)

    # pull user mesage from databse pass to ai
    db.query(Message).filter(Message.message == user_message).first()

    # generate ai repsponse
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        gpt_messages=[
            {
                "role": "system",
                "content": """You are a poetic assistant,
                    skilled in explaining complex
                    programming concepts with creative flair.""",
            },
            {
                "role": "user",
                "content": f"{user_message}",
            },
        ],
    )

    ai_response = completion.choices[0].message
    # send response to user
    message = client.messages.create(
        body= ai_response,
        to=user.phone_number,
        from_=twilio_number,
    )
    # log message to database
    message = client.messages.create(
        body= response_message,
        to=user.phone_number,
        from_=twilio_number,
    )
