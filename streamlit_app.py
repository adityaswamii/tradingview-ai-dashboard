import streamlit as st
import numpy as np
import pandas as pd

st.title("Hello Streamlit")

if st.button("Send balloons!"):
    st.balloons()
    