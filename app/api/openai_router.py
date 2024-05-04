import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()
# defaults to getting the key using
os.environ.get("OPENAI_API_KEY")
