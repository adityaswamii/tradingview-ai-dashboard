
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts

st.title('TSLA Stock Price Chart')
show_markers = st.checkbox('Show Markers', value=False)
show_support = st.checkbox('Show Support', value=False)
show_resistance = st.checkbox('Show Resistance', value=False)

# --- DATA PREPROCESSING ---

COLOR_BULL = 'rgba(38,166,154,0.7)'  # #26a69a
COLOR_BEAR = 'rgba(166,83,80,0.7)'  # #ef5350
COLOR_NEUTRAL = 'rgba(255, 192, 0, 0.7)'  # #ffc107


@st.cache_data()
def get_data():
    # Load the TSLA stock data from the CSV file
    data = pd.read_csv("data/TSLA_data.csv", parse_dates=['timestamp'])
    
    # Ensure there are no duplicate timestamps
    data = data.drop_duplicates(subset='timestamp')
    
    # Convert timestamp to milliseconds for lightweight charts
    data['time'] = data['timestamp'].astype('int64') // 10 ** 9
    
    # Fill empty values in the 'direction' column with "NEUTRAL"
    data['direction'] = data['direction'].fillna("NEUTRAL")
    
    # Convert direction to categorical type
    data['direction'] = data['direction'].replace({"LONG": 0, "SHORT": 1, "NEUTRAL": 2})
    
    # Convert 'Support' and 'Resistance' columns from string representation of lists to actual lists
    data['Support'] = data['Support'].apply(eval)
    data['Resistance'] = data['Resistance'].apply(eval)
    
    # Forward fill and backward fill to handle missing values in 'Support' and 'Resistance'
    data['Support'] = data['Support'].apply(lambda x: x if x else np.nan)
    data['Support'] = data['Support'].ffill().bfill()
    data['Resistance'] = data['Resistance'].apply(lambda x: x if x else np.nan)
    data['Resistance'] = data['Resistance'].ffill().bfill()
    
    # Create lower and upper support and resistance values
    data['support_min'] = data['Support'].apply(min)
    data['support_max'] = data['Support'].apply(max)
    data['resistance_min'] = data['Resistance'].apply(min)
    data['resistance_max'] = data['Resistance'].apply(max)
    
    return data


df = get_data()

# Create a dictionary for candlestick data
candles = df[['open', 'high', 'low', 'close', 'time', 'direction']].to_dict('records')

# Create dictionaries for support and resistance band lines
support_min_line = df[['time', 'support_min']].rename(columns={'support_min': 'value'}).to_dict('records')
support_max_line = df[['time', 'support_max']].rename(columns={'support_max': 'value'}).to_dict('records')
resistance_min_line = df[['time', 'resistance_min']].rename(columns={'resistance_min': 'value'}).to_dict('records')
resistance_max_line = df[['time', 'resistance_max']].rename(columns={'resistance_max': 'value'}).to_dict('records')

#
# df.info()
# print(len(candles))
# print(df['Support'][16:20])
# print(df['Resistance'][24:28])
# print(len(support_min_line))

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
seriesCandlestickChart = [
    {
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
                "shape": 'arrowUp' if candle['direction'] == 0 else 'arrowDown' if candle[
                                                                                       'direction'] == 1 else 'circle',
                "size": 0.5 if show_markers else 0,
            } for candle in candles[total_count - candle_count:]
        ],
    },
    {
        "type": "Line",
        "data": support_max_line[total_count - candle_count:] if show_support else [],
        "options": {
            "lineStyle": 3,
            "color": "rgba(0,255,0,0.2)",
            "lineWidth": 1,
        },
    },
    {
        "type": "Line",
        "data": support_min_line[total_count - candle_count:] if show_support else [],
        "options": {
            "lineStyle": 3,
            "color": "rgba(0,255,0,0.2)",
            "lineWidth": 1,
        }
    },
    {
        "type": "Line",
        "data": resistance_max_line[total_count - candle_count:] if show_resistance else [],
        "options": {
            "lineStyle": 3,
            "color": "rgba(255,0,0,0.2)",
            "lineWidth": 1,
        },
    },
    {
        "type": "Line",
        "data": resistance_min_line[total_count - candle_count:] if show_resistance else [],
        "options": {
            "lineStyle": 3,
            "color": "rgba(255,0,0,0.2)",
            "lineWidth": 1,
        }
    },
]

# Render the chart with the specified options and series
renderLightweightCharts([
    {
        "chart": chartOptions,
        "series": seriesCandlestickChart
    }
], 'candlestick')
