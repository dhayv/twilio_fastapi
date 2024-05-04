import logging
from contextlib import asynccontextmanager

from data_base.dbcore import create_database
from fastapi import FastAPI
from model import Message, User
from router import message_router, user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    logging.info("Database Created")


app = FastAPI()


@app.get("api")
def hello():
    return {"message": "Hello, World"}


app.include_router(message_router.router)
app.include_router(user_router.router)
