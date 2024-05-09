import enum

from pydantic import BaseModel


class UserBase(BaseModel):
    phone_number: str
    """Base model for user data.
    Includes the user's phone number."""


class UserCreate(UserBase):
    """Schema for creating a new user.
    Inherits the phone number from UserBase."""


class UserResponse(UserBase):
    id: int
    """Response schema for user data.
    Includes the user's database ID and phone number."""

    class Config:
        orm_mode = True
        """Configures the schema to treat dictionaries as ORM models
        facilitating compatibility with SQLAlchemy."""


class MessageDirection(str, enum.Enum):
    INCOMING = "incoming"
    OUTGOING = "outgoing"


class MessageBase(BaseModel):
    message: str
    direction: MessageDirection
    """Defines the direction of the message
    either incoming to the system or outgoing from the system."""


class MessageCreate(MessageBase):
    """Schema for creating a new message.
    Inherits all fields from MessageBase without modification."""


class MessageResponse(MessageBase):
    id: int
    user_id: int
    """Response schema for message data.
    Includes database ID and associated user ID."""

    class Config:
        orm_mode = True
        """Enables ORM mode for compatibility with SQLAlchemy models."""
