import streamlit as st
from streamlit_extras.let_it_rain import rain

st.title("About Me")
st.divider()
st.markdown("""Hi! I'm Aditya Swami, a Computer Science undergraduate at Krea University with a strong foundation in logic, programming languages, and data-driven systems. My recent academic work includes a research internship where I formalized Dilworth’s Theorem using Isabelle, resulting in a published entry in the Isabelle Archive of Formal Proofs ([here](https://isa-afp.org/entries/Dilworth.html)). This experience deepened my appreciation for formal correctness, precision, and clean design—principles I aim to bring into every project I build.

This dashboard was created as part of an LLM/Python Developer Internship assessment for IndianCapital. It combines multiple layers of real-world financial data using TradingView's Lightweight Charts and Streamlit, integrating OHLCV data visualization with direction markers, dynamic support/resistance bands, and an AI-powered chatbot using the Gemini API. The goal was to not only present the data effectively, but also make it explorable and insightful.

While developing this, I enjoyed the challenge of translating financial logic into responsive visuals and layered interactions—bridging my interests in systems thinking, data visualization, and AI interfaces. Working on the chatbot in particular helped me better understand how to structure domain-specific queries and responses using LLMs, and how to integrate natural language interfaces meaningfully into data-driven applications.

You can find my resume below and other projects on my [GitHub](https://www.github.com/adityaswamii) and [LinkedIn](https://www.linkedin.com/in/aditya-swamii/) profiles. Feel free to reach out to me at [adityaswami2004@gmail.com](mailto:adityaswami2004@gmail.com) if you have any questions or would like to connect. Any feedback on this dashboard is also welcome!
            
            """)
col1, col2, col3, col4 = st.columns(4)
with open("assets/AdityaSwami_CV_Apr25.pdf", "rb") as f:
    pdf_bytes = f.read()
col1.download_button(
    label="Download Resume",
    data=pdf_bytes,
    file_name="AdityaSwami_CV_Apr25.pdf",
    mime="application/pdf"
)
feedback = col4.feedback("stars")
col4.caption("(Rate the dashboard!)" if feedback is None else "Thanks for the feedback!" if feedback > 0 else "rip")
if feedback is not None:
    rain(
        emoji="🥳" if feedback == 4 else "🤩" if feedback == 3 else "😄" if feedback == 2 else "🙂" if feedback == 1 else "💀",
        font_size=34,
        falling_speed=5,
        animation_length="2",
    )
