import os

from dotenv import load_dotenv
from fastapi import APIRouter
from twilio.rest import Client

load_dotenv()

router = APIRouter


account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
twilio_number = os.environ.get("TWILIO_NUMBER")


client = Client(account_sid, auth_token)


message = client.messages.create(
    from_=twilio_number, body="Hello from Twilio", to="+18777804236"
)

print(message.sid)

# Print detailed output
print(f"Message SID: {message.sid}")
print(f"Message Status: {message.status}")
print(f"Sent from: {message.from_}")
print(f"Sent to: {message.to}")
print(f"Message Body: {message.body}")
