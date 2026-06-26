import streamlit as st
import pandas as pd
import yfinance as yf
import time

# --- 1. CORE FUNCTIONS ---
def calculate_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# --- 2. PAGE CONFIGURATION & UI ---
st.set_page_config(page_title="Pistour Terminal", layout="wide")

st.sidebar.header("⚙️ Control Panel")
run_analysis = st.sidebar.button("Run Market Analysis")

st.title("📈 Pistour Terminal")
st.write("Welcome to the main command center.")

# --- 3. DATA ENGINE ---
if run_analysis:
    st.markdown("---")
    st.subheader("Market Analysis: Momentum & RSI")
    
    with st.spinner("Analyzing market data..."):
        tickers = ["NVDA", "AMD", "MSFT", "AAPL", "SNOW", "TSM", "ARM", "INTC"]
        data_list = []
        
        # Stáhneme všechna data najednou
        market_data = yf.download(tickers, period="3mo", group_by="ticker")
        
        for symbol in tickers:
            hist = market_data[symbol]
            
            if len(hist) > 14:
                rsi = calculate_rsi(hist, period=14).iloc[-1]
                momentum = ((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
                
                data_list.append({
                    'Ticker': symbol, 
                    'Momentum (%)': round(momentum, 2), 
                    'RSI': round(rsi, 2)
                })
            
            time.sleep(0.5)
        
        df = pd.DataFrame(data_list)
        df_sorted = df.sort_values(by='Momentum (%)', ascending=False)
        
        st.success("Analysis complete!")
        st.dataframe(df_sorted, use_container_width=True)