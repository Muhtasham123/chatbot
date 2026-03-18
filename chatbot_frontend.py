import streamlit as st
from langchain_core.messages import HumanMessage
from chatbot_backend import chatbot

# load chat and display history

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

chat_history = st.session_state['chat_history']

for msg in chat_history:
    with st.chat_message(msg['role']):
        st.text(msg['content'])

# User input box
user_input = st.chat_input("Type here")

if user_input:
    st.session_state['chat_history'].append({'role':'user', 'content':user_input})  
    with st.chat_message("user"):
        st.text(user_input)


    initial_state = {'chat': [HumanMessage(content = user_input)]}
    thread_id = '-1'
    config1 = {'configurable':{'thread_id':thread_id}}
    
    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, matadata in chatbot.stream(
                initial_state, 
                config=config1,
                stream_mode="messages"
            )
        )
    st.session_state['chat_history'].append({'role':'assistant', 'content':ai_message})
