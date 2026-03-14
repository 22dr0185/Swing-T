import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Swing Trading Signals",
    page_icon="📈",
    layout="wide"
)

# Title
st.title("📈 Swing Trading Signal Generator")
st.markdown("---")

# Simple stock list
stocks = {
    'RELIANCE': 'RELIANCE.NS',
    'TCS': 'TCS.NS',
    'HDFC Bank': 'HDFCBANK.NS',
    'Infosys': 'INFY.NS',
    'ICICI Bank': 'ICICIBANK.NS',
    'SBIN': 'SBIN.NS',
    'BHARTIARTL': 'BHARTIARTL.NS',
    'ITC': 'ITC.NS',
    'HINDUNILVR': 'HINDUNILVR.NS',
    'KOTAKBANK': 'KOTAKBANK.NS'
}

# Sidebar
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("🔄 Refresh Data"):
        st.rerun()
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This app shows real-time Indian stock prices")
    st.markdown("📊 Data from Yahoo Finance")

# Main content
st.subheader("🎯 Live Stock Prices")

# Create a table
data = []
for name, symbol in stocks.items():
    try:
        # Get stock data
        stock = yf.Ticker(symbol)
        
        # Get current price - simpler approach
        hist = stock.history(period="1d", interval="1m")
        
        if not hist.empty:
            price = hist['Close'].iloc[-1]
            change = hist['Close'].iloc[-1] - hist['Open'].iloc[0]
            change_pct = (change / hist['Open'].iloc[0]) * 100
            
            data.append({
                'Stock': name,
                'Price': f"₹{price:.2f}",
                'Change': f"{change:.2f}",
                'Change %': f"{change_pct:.2f}%",
                'Volume': f"{int(hist['Volume'].iloc[-1]):,}"
            })
        else:
            # Try daily data if intraday not available
            hist = stock.history(period="1d")
            if not hist.empty:
                price = hist['Close'].iloc[-1]
                data.append({
                    'Stock': name,
                    'Price': f"₹{price:.2f}",
                    'Change': 'N/A',
                    'Change %': 'N/A',
                    'Volume': 'N/A'
                })
            else:
                data.append({
                    'Stock': name,
                    'Price': 'N/A',
                    'Change': 'N/A',
                    'Change %': 'N/A',
                    'Volume': 'N/A'
                })
    except Exception as e:
        data.append({
            'Stock': name,
            'Price': 'Error',
            'Change': 'Error',
            'Change %': 'Error',
            'Volume': 'Error'
        })

# Convert to DataFrame and display
if data:
    df = pd.DataFrame(data)
    
    # Color coding for changes
    def color_change(val):
        if isinstance(val, str):
            return ''
        try:
            if float(str(val).replace('%', '')) > 0:
                return 'color: green'
            elif float(str(val).replace('%', '')) < 0:
                return 'color: red'
        except:
            return ''
        return ''
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Stock": "Company",
            "Price": "Price (₹)",
            "Change": "Change (₹)",
            "Change %": "Change %",
            "Volume": "Volume"
        }
    )
else:
    st.warning("No data available. Please refresh.")

# Market Overview
st.subheader("📊 Market Overview")

# Get indices data
indices = {
    'Nifty 50': '^NSEI',
    'Bank Nifty': '^NSEBANK',
    'India VIX': '^INDIAVIX'
}

indices_data = []
for name, symbol in indices.items():
    try:
        index = yf.Ticker(symbol)
        hist = index.history(period="1d")
        if not hist.empty:
            price = hist['Close'].iloc[-1]
            prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else price
            change = price - prev_close
            change_pct = (change / prev_close) * 100
            
            indices_data.append({
                'Index': name,
                'Value': f"{price:.2f}",
                'Change': f"{change:.2f}",
                'Change %': f"{change_pct:.2f}%"
            })
    except:
        pass

if indices_data:
    st.dataframe(pd.DataFrame(indices_data), use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption(f"📅 Date: {datetime.now().strftime('%Y-%m-%d')}")
with col2:
    st.caption(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
with col3:
    st.caption("⚠️ For educational purposes only")
