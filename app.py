import streamlit as st
from google import genai

# Page settings
st.set_page_config(
    page_title="AI Learning & Study Assistant",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 AI Learning & Study Assistant")
st.caption("Your personal AI-powered study companion")

# Gemini client
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("Gemini API key is not configured. Add GEMINI_API_KEY in Streamlit Cloud → Settings → Secrets.")
    st.stop()

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
            try:
                system_instruction = (
                    "You are a helpful AI study assistant. "
                    "Explain concepts clearly and simply for students. "
                    "Give accurate and easy-to-understand answers."
                )

                conversation = []
                for message in st.session_state.messages:
                    conversation.append(
                        f'{message["role"].upper()}: {message["content"]}'
                    )

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=system_instruction + "\n\n" + "\n".join(conversation)
                )

                answer = response.text
                st.markdown(answer)

            except Exception as e:
                answer = "Sorry, I couldn't generate a response right now. Please check your Gemini API key and try again."
                st.error(f"AI service error: {e}")

    # Save AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

# Clear chat button
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()
