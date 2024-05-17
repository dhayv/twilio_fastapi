import pytest
from unittest.mock import patch
from fastapi import status

@pytest.fixture
def twilio_signature():
    return "test_twilio_signature"

@pytest.fixture
def twilio_form_data():
    return {
        "From": "+123456789",
        "Body": "Hello"
    }

@pytest.mark.asyncio
@patch("app.routes.RequestValidator.validate", return_value=True)
@patch("app.routes.Client.messages.create")
async def test_receive_sms(mock_twilio_create, mock_twilio_validate, client, twilio_signature, twilio_form_data):
    response = await client.post(
        "/sms/receive",
        data=twilio_form_data,
        headers={"X-Twilio-Signature": twilio_signature}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "Thank you for using our service" in response.json()["message"]

@pytest.mark.asyncio
@patch("app.routes.openai.Completion.create")
@patch("app.routes.Client.messages.create")
async def test_send_response(mock_twilio_create, mock_openai_create, client, db_session):
    user = User(phone_number="+123456789")
    db_session.add(user)
    db_session.commit()

    message = Message(user_id=user.id, message="Hello", direction=MessageDirection.OUTGOING)
    db_session.add(message)
    db_session.commit()

    mock_openai_create.return_value = {
        "choices": [{"text": "This is a test response from OpenAI."}]
    }

    response = await client.post(f"/sms/send{user.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "This is a test response from OpenAI."
