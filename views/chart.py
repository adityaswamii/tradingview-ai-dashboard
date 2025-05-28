
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts

st.title('Interactive TSLA Stock Chart')
st.divider()
col1, col2, col3 = st.columns(3)
show_markers = col1.toggle('Show Markers', value=False)
show_support = col2.toggle('Show Support Band', value=False)
show_resistance = col3.toggle('Show Resistance Band', value=False)
c1, c2, c3, c4, c5 = st.columns(5)
select_timeframe = c5.selectbox('Select timeframe', ['15D', '1M', '3M', '1Y', '500D'])
select_date = c1.date_input('Select date', value=pd.to_datetime('2025-05-02'), max_value=pd.to_datetime('2025-05-02'),
                              min_value=pd.to_datetime('2022-09-15'))

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
date_diff = (pd.to_datetime('2025-05-02') - pd.to_datetime(select_date)).days
total_count = len(candles) - date_diff  # 660
# number of candles to display in the chart
candle_count = 500 if select_timeframe == '500D' \
    else 365 if select_timeframe == '1Y' \
    else 90 if select_timeframe == '3M' \
    else 30 if select_timeframe == '1M' \
    else 15  # default to 15D if '15D' is selected
start_range = total_count - candle_count if total_count - candle_count > 0 else 0


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
        "data": candles[start_range:total_count],
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
            } for candle in candles[start_range:total_count]
        ],
    },
    {
        "type": "Line",
        "data": support_max_line[start_range:total_count] if show_support else [],
        "options": {
            "lineStyle": 0,
            "color": "rgba(0,255,0,0.2)",
            "lineWidth": 1.5,
        },
    },
    {
        "type": "Line",
        "data": support_min_line[start_range:total_count] if show_support else [],
        "options": {
            "lineStyle": 0,
            "color": "rgba(0,255,0,0.2)",
            "lineWidth": 1,
        }
    },
    {
        "type": "Line",
        "data": resistance_max_line[start_range:total_count] if show_resistance else [],
        "options": {
            "lineStyle": 0,
            "color": "rgba(255,0,0,0.2)",
            "lineWidth": 1.5,
        },
    },
    {
        "type": "Line",
        "data": resistance_min_line[start_range:total_count] if show_resistance else [],
        "options": {
            "lineStyle": 0,
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
