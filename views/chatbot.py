import streamlit as st


st.title("Chatbot")


# --- CHATBOT INTERFACE ---

# Initialize session state for chat messages if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input from the chat input box
if prompt := st.chat_input("Ask me anything!"):
    # Display a user message in the chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add a user message to the chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Simulate a response from the chatbot
    with st.chat_message("assistant"):
        response = "This is a simulated response to: " + prompt
        st.markdown(response)
        # Add an assistant message to the chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


# Clear chat button functionality
def clear_chat():
    st.session_state.messages = []
    
# Add a clear chat button
if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
    st.button("Clear Chat", key="clear_chat_button", on_click=clear_chat)
