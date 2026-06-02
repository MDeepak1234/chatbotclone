import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Chatbot")
st.caption("Powered by LangGraph + Groq")

# ---------------- SESSION STATE ----------------

if "message_history" not in st.session_state:
    st.session_state.message_history = []

# Thread id for LangGraph memory
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "chat_session_1"

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.header("Settings")

    if st.button("🗑 Clear Chat"):

        st.session_state.message_history = []

        # change thread id so memory resets
        st.session_state.thread_id = str(
            len(st.session_state.message_history)
        ) + "_new"

        st.rerun()

# DISPLAY CHAT

for msg in st.session_state.message_history:

    with st.chat_message(
        msg["role"]
    ):

        st.markdown(msg["content"])

# CHAT INPUT 

user_input = st.chat_input(
    "Ask something..."
)

if user_input:

    # show user msg

    st.session_state.message_history.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message(
        "user"
    ):

        st.markdown(user_input)

    # assistant response

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Thinking..."
        ):

            response = chatbot.invoke(
                {
                    "messages": [
                        HumanMessage(
                            content=user_input
                        )
                    ]
                },
                config={
                    "configurable": {
                        "thread_id":
                        st.session_state.thread_id
                    }
                }
            )

            assistant_reply = \
                response["messages"][-1].content

            st.markdown(
                assistant_reply
            )

    st.session_state.message_history.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )