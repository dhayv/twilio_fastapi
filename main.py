from fastapi import FastAPI
from router import message_router, user_router


app = FastAPI()


@app.get("api")
def hello():
    return {"message": "Hello, World"}


app.include_router(message_router.router)
app.include_router(user_router.router)
