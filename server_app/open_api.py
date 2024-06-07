import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


client = OpenAI(api_key=api_key)

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a text message assistant, you are skilled in returning simple answers to a users query, all messages are done through text messages so be mindful of character limits",
        },
        {
            "role": "user",
            "content": "whats is earth population",
        },
    ],
)


print(completion.choices[0].message.content)
