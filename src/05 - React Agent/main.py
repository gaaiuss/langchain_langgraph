from graph import build_graph
from langchain.messages import HumanMessage
from langgraph.graph.state import RunnableConfig
from rich import print


def main() -> None:
    config = RunnableConfig(configurable={"thread_id": 1})
    graph = build_graph()

    user_input = "Hello, my name is Caio."
    human_message = HumanMessage(user_input)

    message_history = [human_message]

    result = graph.invoke({"messages": message_history}, config=config)

    print(result)


if __name__ == "__main__":
    main()
