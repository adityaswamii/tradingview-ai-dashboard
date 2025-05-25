import streamlit as st
import numpy as np
import pandas as pd
from streamlit_lightweight_charts import renderLightweightCharts


st.title("Hello Streamlit")

if st.button("Send balloons!"):
    st.balloons()


# renderLightweightCharts(charts: <List of Dicts> , key: <str>)

