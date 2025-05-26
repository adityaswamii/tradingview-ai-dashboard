import ast

import pandas as pd
import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts

st.title('TSLA Stock Price Chart')

# --- DATA PREPROCESSING ---

COLOR_BULL = 'rgba(38,166,154,0.9)'  # #26a69a
COLOR_BEAR = 'rgba(239,83,80,0.9)'  # #ef5350

# Load the TSLA stock data from the CSV file
df = pd.read_csv("data/TSLA_data.csv", parse_dates=['timestamp'])

# Fill empty values in the 'direction' column with "NEUTRAL"
df['direction'] = df['direction'].fillna("NEUTRAL")

# Convert 'Support' and 'Resistance' columns from string representation of lists to actual lists
df['Support'] = df['Support'].apply(ast.literal_eval)
df['Resistance'] = df['Resistance'].apply(ast.literal_eval)

df.info()
print(df['direction'].value_counts())
# %%

# Ensure the 'timestamp' column is in datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'])
# Sort the DataFrame by timestamp
df.sort_values(by='timestamp', inplace=True)
# Convert DataFrame to a list of dictionaries for lightweight charts
candles = df[['timestamp', 'open', 'high', 'low', 'close']].to_dict(orient='records')
# Convert timestamps to milliseconds for lightweight charts
for candle in candles:
    candle['timestamp'] = int(candle['timestamp'].timestamp() * 1000)

# --- CHART CONFIGURATION ---

chartOptions = {
    "width": 800,
    "height": 600,
    "layout": {
        "background": {
            "type": "solid",
            "color": "white"
        },
        "textColor": "black"
    },
    "timeScale": {
        "timeVisible": True,
        "secondsVisible": False,
    }
}

seriesCandlestickChart = [{
    "type": "Candlestick",
    "data": candles,
    "options": {
        "upColor": COLOR_BULL,
        "downColor": COLOR_BEAR,
        "wickUpColor": COLOR_BULL,
        "wickDownColor": COLOR_BEAR
    }
}]


# Render the candlestick chart using the lightweight charts component
renderLightweightCharts([
    {
        "chart": chartOptions,
        "series": seriesCandlestickChart
    }])