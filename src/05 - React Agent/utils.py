import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama


def load_ollama(ollama_model: str | None = None) -> ChatOllama:
    """Load a ollama model from a string or get it from `.env` file"""

    if ollama_model:
        return ChatOllama(model=ollama_model, base_url="http://127.0.0.1:11434")

    load_dotenv()
    model = os.getenv("MODEL", "No model found. See your `.env` file.")
    return ChatOllama(model=model, base_url="http://127.0.0.1:11434")
