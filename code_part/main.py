from enum import Enum
import streamlit as st

st.set_page_config(
    page_title="DailyNewsBot Demo",
    page_icon=":robot:",
    layout='centered',
    initial_sidebar_state='expanded',
)

import demo_chat

DEFAULT_SYSTEM_PROMPT = '''
You are DailyNewsBot, a large language model trained by UIBE students to provide daily new information. You can answer any questions related and will do you best to assist users. Respond using markdown.
'''.strip()

with st.sidebar:
    top_p = st.slider(
        'top_p', 0.0, 1.0, 0.8, step=0.01
    )
    temperature = st.slider(
        'temperature', 0.0, 1.5, 0.95, step=0.01
    )
    system_prompt = st.text_area(
        label="System Prompt",
        height=300,
        value=DEFAULT_SYSTEM_PROMPT,
    )
    
    openai_api_key = st.text_input("OpenAI API Key or run with local LLM", key="langchain_search_api_key_openai", type="password")

st.title("DailyNewsBot Demo")

prompt_text = st.chat_input(
    'Chat with DailyNewsBot!',
    key='chat_input',
)

demo_chat.main(top_p, temperature, system_prompt, prompt_text)

    
