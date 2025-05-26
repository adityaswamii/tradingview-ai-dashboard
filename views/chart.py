import streamlit as st

st.title('TSLA Stock Price Chart')

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
renderLightweightCharts([
    {
        "chart": chartOptions,
        "series": seriesCandlestickChart
    }])