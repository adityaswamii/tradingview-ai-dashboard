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

# Handle user input from chat input box
if prompt := st.chat_input("Ask me anything!"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Simulate a response from the chatbot
    with st.chat_message("assistant"):
        response = "This is a simulated response to: " + prompt
        st.markdown(response)
