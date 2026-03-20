from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import BaseMessage, HumanMessage
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama
import sqlite3


model = ChatOllama(model="qwen2.5:1.5b")

class ChatState(TypedDict):
    chat:Annotated[list[BaseMessage], add_messages]

def chat_node(state : ChatState):
    chat = state['chat']

    response = model.invoke(chat)

    return {'chat' : [response]}


graph = StateGraph(ChatState)

conn = sqlite3.connect('chatbot.db', check_same_thread=False)
checkpoint = SqliteSaver(conn)

graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer = checkpoint)

def fetch_threads():
    global checkpoint
    threads = set()

    for checkpoint in checkpoint.list(None):
        thread = checkpoint.config['configurable']['thread_id']
        threads.add(thread)
    return list(threads)