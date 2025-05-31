import contextlib
import io
import random

import google.generativeai as genai
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

st.title("TSLA Data Chatbot")
st.markdown("Ask questions about the given stock data. Powered by Google Gemini AI.")
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


# --- AGENTIC CHATBOT FUNCTIONALITY ---


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


def get_last_message_pairs(messages, n=3):
    """Return last `n` user-assistant message pairs."""
    pairs = []
    temp = {}
    for m in reversed(messages):
        if m["role"] == "assistant" and "user" in temp:
            temp["assistant"] = m["content"]
            pairs.append(temp)
            temp = {}
        elif m["role"] == "user":
            temp = {"user": m["content"]}
        if len(pairs) >= n:
            break
    return list(reversed(pairs))


def generate_code(question, df_columns, sample_df):
    system_prompt = f"""
You are a Python assistant who writes pandas code to answer questions about a DataFrame named `df`.
The DataFrame columns are: {', '.join(df_columns)}.
The 'direction' column is encoded as: LONG = 0 (Bullish), SHORT = 1 (Bearish), NEUTRAL = 2.
The user question is: "{question}"
Return only Python code snippet (no header or explanation), assign your answer to a variable `result`.
Dataframe results should be assigned to `result` variable.
If the result is a pandas Series, convert it to a DataFrame before assigning it to `result`.
If you want to plot, create a matplotlib figure assigned to `fig`.
If you receive a greeting or a question about your capabilities,
then assign the value False to a variable 'show_code' and respond to the user accordingly.
In all other cases, assign the value True to 'show_code'.
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
        show_code = local_vars.get("show_code", None)
        return result, fig, show_code
    except Exception as e:
        return f"⚠️ Error executing code: {e}", None


def extract_python_code(gemini_text):
    if "```python" in gemini_text:
        return gemini_text.split("```python")[1].split("```")[0].strip()
    return gemini_text.strip()


def get_random_prompt():
    prompts = [
        "How many days in 2023 was TSLA bullish?",
        "What was the highest closing price in 2022?",
        "List the support and resistance ranges on the latest trading day.",
        "What is the average volume on days when TSLA was bearish?",
        "Show the number of bullish vs bearish days in January 2024.",
        "Did TSLA break above resistance more often than it dipped below support in \n2023?",
        "Which day had the largest candlestick range in 2025?",
        "How often did the closing price land within the support/resistance band in \n2023?",
        "When was the first day in 2024 TSLA was marked as LONG direction?",
        "Count how many times TSLA closed higher than the previous day in 2023.",
        "What was the average opening price in 2024?",
        "Show the top 5 days with the highest trading volume in 2023.",
        "What was the average daily range (high - low) in 2024?",
        "How many days in 2023 had a closing price above the previous day's high?",
        "What was the average percentage change in closing price from the previous \nday in 2024?",
        "What was the average support and resistance range in 2023?",
        "Show the top 10 days with the highest percentage change in closing price \nin 2024.",
        "What was the average daily volume in 2023?",
        "How many days in 2024 had a closing price above the opening price?",
        "What was the average daily percentage change in closing price in 2023?",
        '''
        Lesgo. Create a line chart of opening and closing prices for 2024.
        Highlight the days where the difference between them was more than 5%,
        using a blue highlight when opening was higher and purple highlight
        when closing was higher. Also use a red dot for bearish and green dot
        for bullish. '''
    ]
    return random.choice(prompts)


# Clear chat button functionality
def clear_chat():
    st.session_state.messages = []


# --- CHATBOT INTERFACE ---


# Initialize session state for chat messages if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input from the chat input box

prompt = st.chat_input("say something")

if not prompt:
    with st.chat_message("assistant"):
        st.markdown(
            "👋 Hi! I'm your TSLA stock data chatbot. "
            "Ask me anything about Tesla stock data, like trends, support/resistance levels, or specific trading days. "
            "I can also generate Python code to analyze the data and plot charts. \n\n"
            "Here's a random prompt to get you started: \n\n"
        )
        st.code(
            get_random_prompt()
        )
else:
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
                code_to_run = extract_python_code(code)
                result, fig, show_code = execute_code(code_to_run, df)
                
                if show_code:
                    st.code(code, language="python")  # optional: show code
                
                if fig:
                    st.pyplot(fig)
                elif isinstance(result, pd.DataFrame):
                    st.dataframe(result)
                else:
                    st.success(f"Answer: {result}")
                
                st.session_state.messages.append({"role": "assistant", "content": str(result)})


# Add a clear chat button
if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
    st.button("Clear Chat", key="clear_chat_button", on_click=clear_chat)