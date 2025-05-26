
import pandas as pd
import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts

st.title('TSLA Stock Price Chart')
show_markers = st.checkbox('Show Markers', value=False)

# --- DATA PREPROCESSING ---

COLOR_BULL = 'rgba(38,166,154,0.9)'  # #26a69a
COLOR_BEAR = 'rgba(239,83,80,0.9)'  # #ef5350
COLOR_NEUTRAL = 'rgba(255, 192, 0, 1)'  # #ffc107

# Load the TSLA stock data from the CSV file
df = pd.read_csv("data/TSLA_data.csv", parse_dates=['timestamp'])

# Ensure there are no duplicate timestamps
df = df.drop_duplicates(subset='timestamp')

# Convert timestamp to milliseconds for lightweight charts
df['time'] = df['timestamp'].astype('int64') // 10 ** 9

# Fill empty values in the 'direction' column with "NEUTRAL"
df['direction'] = df['direction'].fillna("NEUTRAL")

# Convert direction to categorical type
df['direction'] = df['direction'].replace({"LONG": 0, "SHORT": 1, "NEUTRAL": 2})

# Convert 'Support' and 'Resistance' columns from string representation of lists to actual lists
df['Support'] = df['Support'].apply(eval)
df['Resistance'] = df['Resistance'].apply(eval)

# Create a dictionary for candlestick data
candles = df[['open', 'high', 'low', 'close', 'time', 'direction']].to_dict(orient='records')


df.info()
print(len(candles))
print(type(df['Support'][0]))
print(type(df['Resistance'][0]))

# %%

# --- CHART CONFIGURATION ---

# total number of rows in the dataframe
total_count = len(candles) - 1  # 660
# number of candles to display on the chart
candle_count = 50  # cannot be more than 500, otherwise the chart will not render properly

# Define chart options
chartOptions = {
    "height": 500,
    "rightPriceScale": {
        "scaleMargins": {
            "top": 0.2,
            "bottom": 0.25,
        },
        "borderVisible": False,
    },
    "overlayPriceScales": {
        "scaleMargins": {
            "top": 0.7,
            "bottom": 0.1,
        }
    },
    "layout": {
        "background": {
            "type": 'solid',
            "color": '#131722'
        },
        "textColor": '#d1d4dc',
    },
    "grid": {
        "vertLines": {
            "color": 'rgba(42, 46, 57, 0)',
        },
        "horzLines": {
            "color": 'rgba(42, 46, 57, 0.6)',
        }
    }
}

# Define the series for the candlestick chart
seriesCandlestickChart = [{
    "type": 'Candlestick',
    "data": candles[total_count - candle_count:],
    "options": {
        "upColor": COLOR_BULL,
        "downColor": COLOR_BEAR,
        "borderVisible": False,
        "wickUpColor": COLOR_BULL,
        "wickDownColor": COLOR_BEAR
    },
    "markers": [
        {
            "time": candle['time'],
            "position": 'belowBar' if candle['direction'] == 0 else 'aboveBar' if candle[
                                                                                      'direction'] == 1 else 'belowBar',
            # circle below candle for NEUTRAL
            "color": COLOR_BULL if candle['direction'] == 0 else COLOR_BEAR if candle[
                                                                                   'direction'] == 1 else COLOR_NEUTRAL,
            "shape": 'arrowUp' if candle['direction'] == 0 else 'arrowDown' if candle['direction'] == 1 else 'circle',
            "size": 0.5 if show_markers else 0,
        } for candle in candles[total_count - candle_count:]
    ],
}]

renderLightweightCharts([
    {
        "chart": chartOptions,
        "series": seriesCandlestickChart
    }
], 'candlestick')
