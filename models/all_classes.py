from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id :
    phone_number :

class Message(Base):
    __tablename__ = "message"
    id :
    message :
    direction :
    user_id :
