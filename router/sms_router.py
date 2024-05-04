from fastapi import APIRouter
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter


account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = os.getenv('TWILIO_NUMBER')


client = Client(account_sid, auth_token)


message = client.messages.create(
  from_=twilio_number,
  body='Hello from Twilio',
  to='+13059624210'
)

print(message.sid)

# Print detailed output
print(f"Message SID: {message.sid}")
print(f"Message Status: {message.status}")
print(f"Sent from: {message.from_}")
print(f"Sent to: {message.to}")
print(f"Message Body: {message.body}")


@router.post("/sms/")
def send_sms():
    return {"message": "made"}
