import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api import sms_router
from database import create_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    logging.info("Database Created")


app = FastAPI()


@app.get("/api")
def hello():
    return {"message": "Hello, World"}


app.include_router(sms_router.router)
