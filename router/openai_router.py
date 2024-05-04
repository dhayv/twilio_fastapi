from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()

client = OpenAI()
# defaults to getting the key using
os.environ.get("OPENAI_API_KEY")
