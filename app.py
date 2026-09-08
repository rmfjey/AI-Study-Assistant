
import streamlit as st
import ollama

# Page settings
st.set_page_config(
    page_title="AI Learning & Study Assistant",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 AI Learning & Study Assistant")
st.caption("Your personal AI-powered study companion")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("💬 Ask your study question..."):

    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            response = ollama.chat(
                model="llama3.2",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful AI study assistant. "
                            "Explain concepts clearly and simply for students. "
                            "Give accurate and easy-to-understand answers."
                        )
                    }
                ] + st.session_state.messages
            )

            answer = response["message"]["content"]
            st.markdown(answer)

    # Save AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

# Clear chat button
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()
