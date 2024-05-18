import logging
from contextlib import asynccontextmanager

from server_app.database import create_database
from fastapi import FastAPI

from server_app import sms_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    logging.info("Database Created")


app = FastAPI()


@app.get("/api")
def hello():
    return {"message": "Hello, World"}


app.include_router(sms_router.router)
