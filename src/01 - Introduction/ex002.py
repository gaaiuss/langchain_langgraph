import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from rich import print

load_dotenv()

model = os.getenv("MODEL", "Model not found. Check you `.env` file.")
llm = ChatOllama(model=model)

system_message = SystemMessage(
    "You are a study guide, who helps students to learn new topics. \n\n"
    "Your job is to guide their ideas for them to be able to understand the "
    "chosen topic without receiving done answers from yourself. "
    "Avoid talking parallels from the chosen topic. If the student do not "
    "chose a topic, your first job is to ask for a topic until the student "
    "informs it. \n\n"
    "You can be friendly, cool and treat the student as a teenager. "
    "We want to avoid the fatigue of a rigid study and keep them "
    "engaged on whatever topic they are studying. \n\n"
    "The next messages will be done by a student. ",
)
human_message = HumanMessage("hi, how are you?")

messages = [system_message, human_message]
response = llm.invoke(messages)
print(f"{' AI ':-^80}")
print(response.content)

while True:
    print(f"{'Human':-^80}")
    user_input = input("Type your message: ")
    human_message = HumanMessage(user_input)

    if user_input.lower() in ["exit", "quit", "bye", "q"]:
        break

    messages.append(human_message)
    response = llm.invoke(messages)

    print(f"{'AI':-^80}")
    print(response.content)
    print()

    messages.append(response)

print()
print(f"{'History':-^80}")
print(*[f"{m.type.upper()}\n{m.content}\n\n" for m in messages], sep="", end="")
print()
