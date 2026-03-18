from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import BaseMessage, HumanMessage
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama


model = ChatOllama(model="qwen2.5:1.5b")

class ChatState(TypedDict):
    chat:Annotated[list[BaseMessage], add_messages]

def chat_node(state : ChatState):
    chat = state['chat']

    response = model.invoke(chat)

    return {'chat' : [response]}


graph = StateGraph(ChatState)
checkpoint = InMemorySaver()

graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer = checkpoint)