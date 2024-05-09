import enum
from typing import List

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import (
    Mapped, declarative_base, mapped_column, relationship)

Base = declarative_base()


# SqlAlchemy Model
class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    phone_number: Mapped[str] = mapped_column(unique=True)
    messages: Mapped[List["Message"]] = relationship(back_populates="user")


# SqlAlchemy Enum Model
class MessageDirection(enum.Enum):
    INCOMING = "incoming"
    OUTGOING = "outgoing"


# SqlAlchemy Model
class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column()
    direction: Mapped[MessageDirection] = mapped_column(Enum(MessageDirection))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="messages")
