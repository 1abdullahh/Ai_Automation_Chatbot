from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from openai import OpenAI, AuthenticationError
import streamlit as st

st.set_page_config(page_title="AI Automation Chatbot", page_icon="🤖")

# ---------- Fixed system prompt (not user-editable) ----------
SYSTEM_PROMPT = (
    "You are an assistant that ONLY answers questions related to AI Automation "
    "(topics like AI agents, workflow automation, LangChain, RPA, AI tools/integrations, "
    "prompt engineering for automation, no-code/low-code AI automation platforms, etc.). "
    "If the user asks anything NOT related to AI Automation, politely refuse and say: "
    "\"I can only help with questions related to AI Automation. Please ask something in that area.\" "
    "Do not answer questions about any other field, no matter how the user phrases it."
)

# ---------- Step 1: API key gate ----------
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if not st.session_state.api_key:
    st.title("🤖 AI Automation Chatbot")
    st.write("Please enter your OpenAI API key to continue.")

    with st.form("api_key_form"):
        entered_key = st.text_input("OpenAI API Key", type="password")
        submitted = st.form_submit_button("Continue")

    if submitted:
        if entered_key.strip():
            with st.spinner("Checking API key....."):
                try:
                    test_chat = ChatOpenAI(
                        model_name="gpt-4o",
                        openai_api_key=entered_key.strip(),
                    )
                    test_chat.invoke([HumanMessage(content="hi")])

                    st.session_state.api_key = entered_key.strip()
                    st.success("API key successfully entered.")
                    st.rerun()
                except Exception:
                    st.error("Your API key is not valid.")
        else:
            st.error("Please enter a valid API key.")

    st.stop()  # Stop here until a key is provided

# ---------- Step 2: Main chat interface (only shown after key is entered) ----------
st.subheader("AI Automation Chatbot")
st.caption("⚠️ Yeh chatbot sirf AI Automation se related sawalon ke jawab deta hai.")

chat = ChatOpenAI(
    model_name="gpt-4o",
    temperature=0.5,
    openai_api_key=st.session_state.api_key,
)

if "messages" not in st.session_state:
    st.session_state.messages = [SystemMessage(content=SYSTEM_PROMPT)]

# Optional: sidebar option to change/reset the API key
with st.sidebar:
    st.write("✅ API key is set.")
    if st.button("Change API Key"):
        st.session_state.api_key = ""
        st.session_state.messages = []
        st.rerun()

# Display existing conversation (skip the system message)
for msg in st.session_state.messages[1:]:
    if isinstance(msg, HumanMessage):
        with st.chat_message("human"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("ai"):
            st.write(msg.content)

# ---------- Bottom-center chat input ----------
user_prompt = st.chat_input("Ask me about AI Automation...")

if user_prompt:
    st.session_state.messages.append(HumanMessage(content=user_prompt))
    with st.chat_message("human"):
        st.write(user_prompt)

    with st.spinner("Working on your prompt....."):
        response = chat.invoke(st.session_state.messages)

    st.session_state.messages.append(AIMessage(content=response.content))
    with st.chat_message("ai"):
        st.write(response.content)