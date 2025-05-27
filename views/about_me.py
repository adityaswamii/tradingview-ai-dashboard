import streamlit as st

st.title("About Me")
st.divider()
st.markdown("""Hi! I'm Aditya Swami, a Computer Science undergraduate at Krea University with a strong foundation in logic, programming languages, and data-driven systems. My academic work includes a research internship where I formalized Dilworth’s Theorem using Isabelle, resulting in a published entry in the Isabelle Archive of Formal Proofs. This experience deepened my appreciation for formal correctness, precision, and clean design—principles I aim to bring into every project I build.

This dashboard was created as part of the LLM/Python Developer Internship assessment for IndianCapital. It combines multiple layers of real-world financial data using TradingView's Lightweight Charts and Streamlit, integrating OHLCV data visualization with direction markers, dynamic support/resistance bands, and an AI-powered chatbot using the Gemini API. The goal was to not only present the data effectively, but also make it explorable and insightful.

While developing this, I enjoyed the challenge of translating financial logic into responsive visuals and layered interactions—bridging my interests in systems thinking, data visualization, and AI interfaces. I’m excited about the opportunity to contribute to teams like IndianCapital that sit at the intersection of fintech, data, and user-centric engineering.

You can find my resume below and other projects on my [GitHub](https://www.github.com/adityaswamii) and [LinkedIn](https://www.linkedin.com/in/aditya-swamii/) profiles. Feel free to reach out to me at [aditya_swami.sias22@krea.ac.in](mailto:aditya_swami.sias22@krea.ac.in) if you have any questions or would like to connect. Any feedback would be greatly appreciated! 😊
            
            """)
col1, col2, col3, col4 = st.columns(4)
col1.download_button("Download Resume", data="data/AdityaSwami_CV_Apr25.pdf", file_name="AdityaSwami_CV_Apr25.pdf")
col4.feedback("faces")
