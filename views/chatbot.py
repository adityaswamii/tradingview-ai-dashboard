import contextlib
import io

import google.generativeai as genai
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

st.title("Chatbot")
st.markdown("Ask me anything! Powered by Google Gemini.")
st.divider()


# --- DATA PREPROCESSING ---

@st.cache_data()
def get_data():
    # Load the TSLA stock data from the CSV file
    data = pd.read_csv("data/TSLA_data.csv", parse_dates=['timestamp'])
    
    # Ensure there are no duplicate timestamps
    data = data.drop_duplicates(subset='timestamp')
    
    # Convert timestamp to milliseconds for lightweight charts
    data['time'] = data['timestamp'].astype('int64') // 10 ** 9
    
    # Fill empty values in the 'direction' column with "NEUTRAL"
    data['direction'] = data['direction'].fillna("NEUTRAL")
    
    # Convert direction to categorical type
    data['direction'] = data['direction'].replace({"LONG": 0, "SHORT": 1, "NEUTRAL": 2})
    
    # Convert 'Support' and 'Resistance' columns from string representation of lists to actual lists
    data['Support'] = data['Support'].apply(eval)
    data['Resistance'] = data['Resistance'].apply(eval)
    
    # Forward fill and backward fill to handle missing values in 'Support' and 'Resistance'
    data['Support'] = data['Support'].apply(lambda x: x if x else np.nan)
    data['Support'] = data['Support'].ffill().bfill()
    data['Resistance'] = data['Resistance'].apply(lambda x: x if x else np.nan)
    data['Resistance'] = data['Resistance'].ffill().bfill()
    
    # Create lower and upper support and resistance values
    data['support_min'] = data['Support'].apply(min)
    data['support_max'] = data['Support'].apply(max)
    data['resistance_min'] = data['Resistance'].apply(min)
    data['resistance_max'] = data['Resistance'].apply(max)
    
    return data


df = get_data()



# --- GOOGLE GEMINI CONFIGURATION ---

# Configure Google Generative AI with the API key
genai.configure(api_key=st.secrets["gemini"]["api_key"])

# Initialize the GenerativeModel for the Gemini API
model = genai.GenerativeModel("gemini-2.0-flash")


# def ask_gemini(messages):
#     try:
#         prompt_parts = []
#         for m in messages:
#             role = m["role"]
#             content = m["content"]
#             if role == "user":
#                 prompt_parts.append(f"User: {content}")
#             elif role == "assistant":
#                 prompt_parts.append(f"Assistant: {content}")
#
#         prompt_text = "\n".join(prompt_parts) + "\nAssistant:"
#
#         model_response = model.generate_content(prompt_text)
#         return model_response.text
#     except Exception as e:
#         return f"❌ Gemini error: {e}"

def extract_python_code(gemini_text):
    if "```python" in gemini_text:
        return gemini_text.split("```python")[1].split("```")[0].strip()
    return gemini_text.strip()


def generate_code(question, df_columns, sample_df):
    system_prompt = f"""
You are a Python assistant who writes pandas code to answer questions about a DataFrame named `df`.
The DataFrame columns are: {', '.join(df_columns)}.
The 'direction' column is encoded as: LONG = 0 (Bullish), SHORT = 1 (Bearish), NEUTRAL = 2.
The user question is: "{question}"
Return only Python code snippet (no header or explanation), assign your answer to a variable `result`.
If you want to plot, create a matplotlib figure assigned to `fig`.
Here's a sample of the data:
{sample_df.head(3).to_markdown()}
"""
    response = model.generate_content(system_prompt)
    return response.text.strip()


def execute_code(code, df):
    local_vars = {
        "df": df.copy(),
        "pd": pd,
        "np": np,
        "plt": plt,
        "len": len
    }
    stdout = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout):
            exec(code, {}, local_vars)
        result = local_vars.get("result", None)
        fig = local_vars.get("fig", None)
        return result, fig
    except Exception as e:
        return f"⚠️ Error executing code: {e}", None

# --- CHATBOT INTERFACE ---

# Initialize session state for chat messages if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input from the chat input box
if prompt := st.chat_input("Ask about TSLA..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        if st.secrets["gemini"]["demo_mode"] == "true":
            response = "🔒 Gemini chatbot is disabled in demo mode."
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            with st.spinner("Thinking..."):
                sample_df = df.drop(columns=["Support", "Resistance"])  # avoid clutter
                code = generate_code(prompt, df.columns.tolist(), sample_df)
                st.code(code, language="python")  # optional: show code
                
                code_to_run = extract_python_code(code)
                result, fig = execute_code(code_to_run, df)
                
                if fig:
                    st.pyplot(fig)
                elif isinstance(result, pd.DataFrame):
                    st.dataframe(result)
                else:
                    st.success(f"Answer: {result}")
                
                st.session_state.messages.append({"role": "assistant", "content": str(result)})



# Clear chat button functionality
def clear_chat():
    st.session_state.messages = []


# Add a clear chat button
if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
    st.button("Clear Chat", key="clear_chat_button", on_click=clear_chat)