import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel


from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")



client = OpenAI(api_key=api_key)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    logging.info("Database Created")


app = FastAPI()



class UserMessage(BaseModel):
    userid: int
    message: str


@app.get("/api")
def hello():
    return {"message": "Hello, World"}


@app.post("/usersearch",)
async def send_question(user_response: str):
    # generate ai repsponse
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a text message assistant, you are skilled in returning simple answers to a users query, all messages are done through text messages so be mindful of character limits",
            },
            {
                "role": "user",
                "content": {user_response},
            },
        ],
    )

    return completion.choices[0].message.content.strip()


@app.get("/airesponse",)
async def send_response(user_id: int,):
    pass
