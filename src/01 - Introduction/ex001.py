"""Langchain

For step by step applications or well defined tasks, the langchain model is better
for its simplicity.

As the name implies, it consists in a chain of steps where the return of a step
becomes the input of the next.

Prompt -> LLM -> Solution -> END
"""

import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from rich import print

load_dotenv()

model = os.getenv("MODEL", "Not working. Read the `.env-example`.")

llm = init_chat_model(model)

response = llm.invoke("hi, how are you?")
print(response)
