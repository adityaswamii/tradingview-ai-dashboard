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



