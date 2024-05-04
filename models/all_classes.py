from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, relationship, DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    phone_number: Mapped[str] = mapped_column(unique=True)

    addresses: Mapped["Message"] = relationship(back_populates="user")


class Message(Base):
    __tablename__ = "message"
    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str]
    direction: Mapped[Enum]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    addresses: Mapped["User"] = relationship(back_populates="message")
