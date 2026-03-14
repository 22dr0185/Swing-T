import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Simple Stock App", page_icon="📈")

st.title("📈 Indian Stocks - Simple Version")
st.write("Loading data...")

# Just 5 stocks for speed
stocks = {
    'RELIANCE': 'RELIANCE.NS',
    'TCS': 'TCS.NS',
    'HDFC Bank': 'HDFCBANK.NS',
    'Infosys': 'INFY.NS',
    'ICICI Bank': 'ICICIBANK.NS'
}

data = []
for name, symbol in stocks.items():
    try:
        # Simple data fetch
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1d")
        if not hist.empty:
            price = hist['Close'].iloc[-1]
            data.append({
                'Company': name,
                'Price (₹)': round(price, 2)
            })
        else:
            data.append({'Company': name, 'Price (₹)': 'N/A'})
    except:
        data.append({'Company': name, 'Price (₹)': 'Error'})

# Show data
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True, hide_index=True)

# Simple time display
st.caption(f"Updated: {datetime.now().strftime('%H:%M:%S')}")
st.caption("✅ Simple version - should load fast!")
