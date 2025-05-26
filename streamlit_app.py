from email.policy import default

import streamlit as st
import numpy as np
import pandas as pd
import json
from streamlit_lightweight_charts import renderLightweightCharts
from lightweight_charts.widgets import StreamlitChart
import ast


# --- PAGE SETUP & NAVIGATION ---

# Page Setup
about_page = st.Page(
    title="About Me",
    page = "views/about_me.py",
    icon = ":material/account_circle:",
)
chatbot_page = st.Page(
    title="Gemini Chatbot",
    page = "views/chatbot.py",
    icon = ":material/smart_toy:",
)
chart_page = st.Page(
    title="TSLA Stock Chart",
    page = "views/chart.py",
    icon = ":material/finance_mode:",
    default = True,
)

# Navigation Setup
pg = st.navigation(
    {
        "Dashboard": [chart_page, chatbot_page],
        "Info": [about_page],
    }
)

# Shared on all pages
st.sidebar.text("Made by Aditya Swami")

# Run navigation
pg.run()


# --- DATA PREPROCESSING ---

df = pd.read_csv("data/TSLA_data.csv", parse_dates=['timestamp'])
df['Support'] = df['Support'].apply(ast.literal_eval)
df['Resistance'] = df['Resistance'].apply(ast.literal_eval)

COLOR_BULL = 'rgba(38,166,154,0.9)'  # #26a69a
COLOR_BEAR = 'rgba(239,83,80,0.9)'  # #ef5350

# Convert timestamp to UNIX time in seconds and determine color based on open and close prices
df['time'] = df['timestamp'].astype('int64') // 10 ** 9
df['color'] = np.where(df['open'] > df['close'], COLOR_BEAR, COLOR_BULL)

# Export to JSON format for lightweight charts
candles = json.loads(
    df.filter(['time', 'open', 'high', 'low', 'close'], axis=1).to_json(orient="records"))
