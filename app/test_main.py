import os
from unittest.mock import MagicMock, patch

import pytest
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import sms_router
from database import get_db
from model import Base, Message, MessageDirection, User

# Ensure necessary packages are imported
import openai

load_dotenv()

twilio_number = os.getenv("TWILIO_NUMBER")

# Setup the database and app
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(sms_router.router)

# Dependency override
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def test_app():
    return app

@pytest.fixture(scope="module")
async def async_client(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        yield ac

# Mock OpenAI and Twilio
mock_openai_response = MagicMock()
mock_openai_response.choices = [MagicMock()]
mock_openai_response.choices[0].text = "Mock AI response"

mock_twilio_response = MagicMock()
mock_twilio_response.sid = "mock_sid"

@pytest.mark.asyncio
async def test_receive_sms(async_client):
    form_data = {
        "From": "+1234567890",
        "Body": "Test message",
        "To": twilio_number,
    }

    with patch("twilio.rest.Client.messages.create", return_value=mock_twilio_response):
        with patch(
            "twilio.request_validator.RequestValidator.validate", return_value=True
        ):
            response = await async_client.post("/sms/receive", data=form_data)
            assert response.status_code == 200
            assert response.json()["message"] == "Thank you for using our service"

@pytest.mark.asyncio
async def test_send_response(async_client):
    # Create a user and a message
    db = TestingSessionLocal()
    user = User(phone_number="+1234567890")
    db.add(user)
    db.commit()
    db.refresh(user)

    message = Message(
        user_id=user.id,
        message="Test message",
        direction=MessageDirection.INCOMING,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    db.close()

    with patch("twilio.rest.Client.messages.create", return_value=mock_twilio_response):
        with patch("openai.Completion.create", return_value=mock_openai_response):
            response = await async_client.post(f"/sms/send/{user.id}")
            assert response.status_code == 200
            assert response.json()["message"] == "Mock AI response"

@pytest.mark.asyncio
async def test_invalid_twilio_signature(async_client):
    form_data = {
        "From": "+1234567890",
        "Body": "Test message",
    }

    with patch(
        "twilio.request_validator.RequestValidator.validate", return_value=False
    ):
        response = await async_client.post("/sms/receive", data=form_data)
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid Twilio Signature"}

@pytest.mark.asyncio
async def test_missing_message_details(async_client):
    form_data = {
        "From": "",
        "Body": "",
    }

    response = await async_client.post("/sms/receive", data=form_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing Message Details"}

@pytest.mark.asyncio
async def test_user_not_found(async_client):
    response = await async_client.post("/sms/send/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

@pytest.mark.asyncio
async def test_user_message_not_found(async_client):
    # Create a user without messages
    db = TestingSessionLocal()
    user = User(phone_number="+1234567890")
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    response = await async_client.post(f"/sms/send/{user.id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "User message not found"}
