import streamlit as st
import numpy as np
import pandas as pd
import json
from streamlit_lightweight_charts import renderLightweightCharts
from lightweight_charts import Chart


df = pd.read_csv("data/TSLA_data.csv", parse_dates=['timestamp'], skiprows=0, skip_blank_lines=True)


COLOR_BULL = 'rgba(38,166,154,0.9)'  # #26a69a
COLOR_BEAR = 'rgba(239,83,80,0.9)'  # #ef5350

# Convert timestamp to UNIX time in seconds and determine color based on open and close prices
df['time'] = df['timestamp'].astype('int64') // 10 ** 9
df['color'] = np.where(df['open'] > df['close'], COLOR_BEAR, COLOR_BULL)

# Export to JSON format for lightweight charts
candles = json.loads(
    df.filter(['time', 'open', 'high', 'low', 'close'], axis=1).to_json(orient="records"))

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

st.title('TSLA Stock Price Chart')
st.subheader("Candlestick Chart from CSV")

# Render the candlestick chart using the lightweight charts component
renderLightweightCharts(
    {
        "chart": chartOptions,
        "series": seriesCandlestickChart
    })

