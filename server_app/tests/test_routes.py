import os
from unittest.mock import MagicMock, patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from twilio.rest import Client

from server_app.database import Base, get_db
from server_app.main import app

# Set up test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def mock_env():
    os.environ["TWILIO_ACCOUNT_SID"] = "test_sid"
    os.environ["TWILIO_AUTH_TOKEN"] = "test_token"
    os.environ["TWILIO_NUMBER"] = "+123456789"
    os.environ["OPENAI_API_KEY"] = "test_openai_key"


@pytest.fixture(scope="session")
def db_engine():
    try:
        Base.metadata.create_all(bind=engine)
        yield engine
    finally:
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="module")
def client(db_session):
    def _get_db_override():
        yield db_session

    app.dependency_overrides[get_db] = _get_db_override
    with TestClient(app) as c:
        yield c


@pytest.fixture
def twilio_signature():
    return {"X-Twilio-Signature": ""}


@pytest.fixture
def twilio_form_data():
    return {"From": "+18553456789", "Body": "Hello"}


@pytest.mark.asyncio
@patch("twilio.rest.Client")
@patch("twilio.request_validator.RequestValidator")
async def test_receive_sms(
    mock_validator, mock_client, client, twilio_signature, twilio_form_data
):
    mock_validator.return_value.validate.return_value = True
    mock_client.return_value.messages.create.return_value = MagicMock(sid="12345")

    response = client.post(
        "/sms/receive",
        data=twilio_form_data,
        headers=twilio_signature,
    )
    assert response.status_code == status.HTTP_200_OK
    assert "Thank you for using our service" in response.text

    print(response.content)  # This will show the error message returned by the server


"""@pytest.mark.asyncio
@patch("server_app.sms_router.openai.Completion.create")
@patch("server_app.sms_router.client.messages.create")
async def test_send_response(
    mock_twilio_create, mock_openai_create, client, db_session
):
    user = User(phone_number="+123456789")
    db_session.add(user)
    db_session.commit()

    message = Message(
        user_id=user.id, message="Hello", direction=MessageDirection.OUTGOING
    )
    db_session.add(message)
    db_session.commit()

    mock_openai_create.return_value = {
        "choices": [{"text": "This is a test response from OpenAI."}]
    }

    response = await client.post(f"/sms/send/{user.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "This is a test response from OpenAI." """
