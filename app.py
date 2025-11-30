import streamlit as st
import yfinance as yf
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="Stock Buddy",
    page_icon="📈",
    layout="wide"
)

# --- Helper Functions ---

@st.cache_data
def fetch_stock_data(ticker_symbol):
    """
    Fetches historical data for the last 6 months.
    Uses caching to avoid repeated API calls.
    """
    try:
        stock = yf.Ticker(ticker_symbol)
        # Fetch 6 months to ensure we have enough data for SMA calculation
        history = stock.history(period="6m")
        
        if history.empty:
            return None, None
            
        info = stock.info
        return history, info
    except Exception as e:
        return None, None

def calculate_sma(data, window=20):
    """
    Calculates the Simple Moving Average (SMA).
    Adds a new column 'SMA' to the dataframe.
    """
    data['SMA'] = data['Close'].rolling(window=window).mean()
    return data

# --- Sidebar Configuration ---
st.sidebar.header("User Settings")

ticker_input = st.sidebar.text_input("Stock Ticker", value="AAPL").upper()
investment_amount = st.sidebar.number_input("Investment Amount ($)", min_value=10.0, value=1000.0, step=100.0)
risk_level = st.sidebar.selectbox("Risk Level", options=["Low", "Medium", "High"])

st.sidebar.markdown("---")
st.sidebar.markdown("### Strategy Info")
st.sidebar.info("The Analysis uses a 20-Day Simple Moving Average (SMA) to determine trends.")

# --- Main Application Logic ---

st.title("📈 Stock Buddy: Technical Analysis")

if ticker_input:
    # 1. Fetch Data
    history_df, stock_info = fetch_stock_data(ticker_input)

    if history_df is not None and not history_df.empty:
        # 2. Perform Analysis (Calculate SMA)
        history_df = calculate_sma(history_df, window=20)
        
        # Get latest values
        current_price = history_df['Close'].iloc[-1]
        previous_close = history_df['Close'].iloc[-2]
        current_sma = history_df['SMA'].iloc[-1]
        delta = current_price - previous_close
        
        # 3. Determine Signal
        # Ensure we have an SMA value (it might be NaN if not enough data points)
        if pd.notna(current_sma):
            if current_price > current_sma:
                signal = "BUY"
                reason = "Price is TRADING ABOVE the 20-day Moving Average (Expect Rise)"
                box_color = "green"
            else:
                signal = "SELL"
                reason = "Price is TRADING BELOW the 20-day Moving Average (Expect Fall)"
                box_color = "red"
        else:
            signal = "INSUFFICIENT DATA"
            reason = "Not enough data points to calculate SMA."
            box_color = "gray"

        # --- Display Section ---
        
        # Header Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                label=f"{ticker_input} Current Price", 
                value=f"${current_price:.2f}", 
                delta=f"{delta:.2f}"
            )
        with col2:
            st.metric(
                label="Investment Value (Est.)",
                value=f"${(investment_amount / current_price) * current_price:.2f}"
            )
        with col3:
             st.metric(label="Risk Setting", value=risk_level)

        st.divider()

        # Recommendation Box
        st.subheader("🤖 Technical Recommendation")
        
        if box_color == "green":
            st.success(f"## 🟢 RECOMMENDATION: {signal}\n\n**Analysis:** {reason}\n\n*Current Price (${current_price:.2f}) > SMA (${current_sma:.2f})*")
        elif box_color == "red":
            st.error(f"## 🔴 RECOMMENDATION: {signal}\n\n**Analysis:** {reason}\n\n*Current Price (${current_price:.2f}) < SMA (${current_sma:.2f})*")
        else:
            st.warning(f"## ⚪ {signal}\n{reason}")

        # Chart Section
        st.subheader("6-Month Trend vs SMA")
        
        # Prepare chart data: We only want Close and SMA columns
        chart_data = history_df[['Close', 'SMA']]
        
        # Streamlit line chart
        st.line_chart(chart_data, color=["#2980b9", "#f39c12"]) 
        # Note: #2980b9 is Blue (Close), #f39c12 is Orange (SMA)

        # Raw Data Expander
        with st.expander("View Raw Data & Calculations"):
            st.dataframe(history_df.tail(10))

    else:
        st.error(f"Could not find data for ticker '{ticker_input}'. Please check the symbol.")
else:
    st.info("Please enter a stock ticker in the sidebar to begin.")