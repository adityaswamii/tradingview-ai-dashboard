

import pandas as pd
import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts

st.title('TSLA Stock Price Chart')

# --- DATA PREPROCESSING ---

COLOR_BULL = 'rgba(38,166,154,0.9)'  # #26a69a
COLOR_BEAR = 'rgba(239,83,80,0.9)'  # #ef5350

# Load the TSLA stock data from the CSV file
df = pd.read_csv("data/TSLA_data.csv", parse_dates=['timestamp'])

# Convert timestamp to milliseconds for lightweight charts
df['time'] = df['timestamp'].astype('int64') // 10 ** 9

# Fill empty values in the 'direction' column with "NEUTRAL"
df['direction'] = df['direction'].fillna("NEUTRAL")

# Convert 'Support' and 'Resistance' columns from string representation of lists to actual lists
df['Support'] = df['Support'].apply(eval)
df['Resistance'] = df['Resistance'].apply(eval)

# Create a dictionary for candlestick data
candles = df[['open', 'high', 'low', 'close', 'time']].to_dict(orient='records')


df.info()
print(candles[0:5])  # Print the first candle data for verification
print(type(df['Support'][0]))
print(type(df['Resistance'][0]))

# %%

# --- CHART CONFIGURATION ---


chartOptions = {
    "layout": {
        "textColor": 'black',
        "background": {
            "type": 'solid',
            "color": 'white'
        }
    }
}

seriesCandlestickChart = [{
    "type": 'Candlestick',
    "data": candles[0:500],
    "options": {
        "upColor": COLOR_BULL,
        "downColor": COLOR_BEAR,
        "borderVisible": False,
        "wickUpColor": COLOR_BULL,
        "wickDownColor": COLOR_BEAR
    }
}]

renderLightweightCharts([
    {
        "chart": chartOptions,
        "series": seriesCandlestickChart
    }
], 'candlestick')
