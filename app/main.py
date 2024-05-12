import logging
from contextlib import asynccontextmanager

from api import message_router, user_router
from database import create_database
from fastapi import FastAPI


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
