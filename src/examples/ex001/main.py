import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from rich import print

load_dotenv()

model = os.getenv("MODEL", "Not working. Read the `.env-example`.")

llm = init_chat_model(model)

response = llm.invoke("hi, how are you?")
print(response)
