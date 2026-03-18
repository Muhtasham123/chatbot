import streamlit as st
from langchain_core.messages import HumanMessage
from chatbot_backend import chatbot
import uuid

#********************** UTILITY FUNCTIONS ************************

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def add_thread_id(thread_id):
    thread_id_list = st.session_state['thread_id_list']
    if thread_id not in thread_id_list:
        thread_id_list.append(thread_id)

#********************** SESSION_STATE SETUP ************************

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'thread_id_list' not in st.session_state:
    st.session_state['thread_id_list'] = []

if 'thread_id' not in st.session_state:
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id

add_thread_id(st.session_state['thread_id']) 


# ********************** SIDEBAR UI ************************

st.sidebar.title("CHATLY")

if st.sidebar.button("New Chat"):
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread_id(thread_id)
    st.session_state['chat_history'] = []

st.sidebar.header("My Conversations")

for thread_id in st.session_state['thread_id_list'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        st.session_state['chat_history'] = []

        CONFIG = {'configurable': {'thread_id': thread_id}}
        session_conversations = chatbot.get_state(CONFIG).values['chat']

        for msg in session_conversations:
            role = ''
            if isinstance(msg, HumanMessage):
                role = "user"
            else:
                role = "assistant"
            st.session_state['chat_history'].append({'role':role, 'content':msg.content})

# ******************** MAIN CHAT PANEL ************************

chat_history = st.session_state['chat_history']

for msg in chat_history:
    with st.chat_message(msg['role']):
        st.text(msg['content'])

user_input = st.chat_input("Type here")

if user_input:
    st.session_state['chat_history'].append({'role':'user', 'content':user_input})  
    with st.chat_message("user"):
        st.text(user_input)


    initial_state = {'chat': [HumanMessage(content = user_input)]}
    thread_id = st.session_state['thread_id']
    CONFIG = {'configurable':{'thread_id':thread_id}}
    
    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, matadata in chatbot.stream(
                initial_state, 
                config=CONFIG,
                stream_mode="messages"
            )
        )
    st.session_state['chat_history'].append({'role':'assistant', 'content':ai_message})
