
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Initialize LLM
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

# Create prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI chatbot. Answer the user's questions."),
    ("human", "{question}")
])

# Create chain
parser = StrOutputParser()
chain = prompt | llm | parser

# Streamlit UI
st.title("Simple AI Chatbot")
st.write("Chat with AI. Type 'bye' or 'exit' to stop.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Get user input
user_input = st.chat_input("Ask something...")

if user_input:

    if user_input.lower().strip() in ["bye", "exit"]:
        st.chat_message("user").write(user_input)
        st.success("Chat ended. Goodbye!")
        st.session_state.messages = []

    else:
        # Display user message
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.write(user_input)

        # Get LLM response
        response = chain.invoke({"question": user_input})

        # Display bot response
        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )

        with st.chat_message("assistant"):
            st.write(response)
