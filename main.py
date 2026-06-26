import streamlit as st
import pandas as pd
import yfinance as yf

# --- 1. CORE FUNCTIONS ---
def calculate_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# --- 2. PAGE CONFIGURATION & UI ---
st.set_page_config(page_title="Terminal", layout="wide")

# Sidebar (Control Panel)
st.sidebar.header("⚙️ Control Panel")
st.sidebar.write("Configure your analysis parameters here.")
run_analysis = st.sidebar.button("Run Market Analysis")

# Main Dashboard
st.title("📈Terminal")
st.write("Welcome to the main command center. System is online and awaiting orders.")
st.metric(label="System Status", value="Online", delta="Ready for Data Fetch")

# --- 3. DATA ENGINE ---
if run_analysis:
    st.markdown("---")
    st.subheader("Market Analysis: Momentum & RSI Overheating")
    
    with st.spinner("Analyzing market data and calculating technical indicators..."):
        # We start with a focused list to keep the API fast during testing
        tickers = ["NVDA", "AMD", "MSFT", "AAPL", "SNOW", "TSM", "ARM", "INTC"]
        data_list = []
        
        for symbol in tickers:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="3mo")
            
            if len(hist) > 14:
                rsi = calculate_rsi(hist, period=14).iloc[-1]
                momentum = ((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
                
                data_list.append({
                    'Ticker': symbol, 
                    'Momentum (%)': round(momentum, 2), 
                    'RSI': round(rsi, 2)
                })
        
        # Create a professional DataFrame and sort by Momentum
        df = pd.DataFrame(data_list)
        df_sorted = df.sort_values(by='Momentum (%)', ascending=False)
        
        # Display the UI
        st.success("Analysis complete! Systems normalized.")
        st.dataframe(df_sorted, use_container_width=True)