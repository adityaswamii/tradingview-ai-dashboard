import google.generativeai as genai
import streamlit as st

st.title("Chatbot")
st.markdown("Ask me anything! Powered by Google Gemini.")

# --- GOOGLE GEMINI CONFIGURATION ---

# Configure Google Generative AI with the API key
genai.configure(api_key=st.secrets["gemini"]["api_key"])

# Initialize the GenerativeModel for the Gemini API
model = genai.GenerativeModel("gemini-2.0-flash")


def ask_gemini(messages):
    try:
        prompt_parts = []
        for m in messages:
            role = m["role"]
            content = m["content"]
            if role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        prompt_text = "\n".join(prompt_parts) + "\nAssistant:"
        
        model_response = model.generate_content(prompt_text)
        return model_response.text
    except Exception as e:
        return f"❌ Gemini error: {e}"



# --- CHATBOT INTERFACE ---

# Initialize session state for chat messages if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input from the chat input box
if prompt := st.chat_input("Say something..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        if st.secrets["gemini"]["demo_mode"] == "true":
            response = "🔒 Gemini chatbot is disabled in demo mode."
        else:
            with st.spinner("Thinking..."):
                response = ask_gemini(st.session_state.messages)
        
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})


# Clear chat button functionality
def clear_chat():
    st.session_state.messages = []


# Add a clear chat button
if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
    st.button("Clear Chat", key="clear_chat_button", on_click=clear_chat)