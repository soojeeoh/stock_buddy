import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from textblob import TextBlob
from datetime import datetime, timedelta

# --- Page Config ---
st.set_page_config(page_title="Stock Buddy", layout="wide")

st.title("📈 Stock Buddy: AI-Powered Market Assistant")
st.markdown("I analyze price trends and news sentiment to help you decide.")

# --- Sidebar Inputs ---
st.sidebar.header("User Configuration")
ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL").upper()
investment = st.sidebar.number_input("Investment Amount ($)", value=1000, step=100)
risk_profile = st.sidebar.selectbox("Your Risk Profile", ["Conservative", "Aggressive"])

# --- Functions ---

def get_sentiment(ticker_symbol):
    """Fetches news and calculates average sentiment using TextBlob."""
    try:
        stock = yf.Ticker(ticker_symbol)
        news = stock.news
        
        if not news:
            return 0, "No news found"

        sentiment_score = 0
        headlines = []
        
        for article in news[:5]: # Analyze top 5 articles
            title = article.get('title', '')
            blob = TextBlob(title)
            sentiment_score += blob.sentiment.polarity
            headlines.append(title)
            
        avg_score = sentiment_score / len(news[:5])
        return avg_score, headlines
    except Exception as e:
        return 0, []

def get_stock_data(ticker_symbol):
    """Fetches historical price data."""
    try:
        stock = yf.Ticker(ticker_symbol)
        df = stock.history(period="6mo")
        return df
    except:
        return pd.DataFrame()

# --- Main Logic ---

if ticker:
    # 1. Get Data
    df = get_stock_data(ticker)
    
    if not df.empty:
        # Calculate Technical Indicators (Simple Moving Average)
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        current_price = df['Close'].iloc[-1]
        
        # 2. Get AI Sentiment
        sentiment_score, headlines = get_sentiment(ticker)
        
        # Display Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"${current_price:.2f}")
        
        # Sentiment Logic
        if sentiment_score > 0.1:
            sent_label = "Positive 🚀"
            sent_color = "green"
        elif sentiment_score < -0.1:
            sent_label = "Negative 📉"
            sent_color = "red"
        else:
            sent_label = "Neutral 😐"
            sent_color = "gray"
            
        col2.metric("News Sentiment (AI Analysis)", sent_label)
        
        # 3. The "Stock Buddy" Verdict Logic
        recommendation = ""
        reasoning = ""
        
        is_uptrend = current_price > df['SMA_50'].iloc[-1]
        
        if is_uptrend and sentiment_score > 0:
            recommendation = "STRONG BUY"
            reasoning = "The trend is up (Technical) AND news is positive (Sentiment)."
        elif is_uptrend and sentiment_score < 0:
            recommendation = "HOLD / CAUTION"
            reasoning = "The price is rising, but recent news is negative. Be careful."
        elif not is_uptrend and sentiment_score < 0:
            recommendation = "AVOID / SELL"
            reasoning = "The trend is down and news is bad."
        else:
            recommendation = "WATCH"
            reasoning = "Signals are mixed. Wait for a clearer direction."

        col3.metric("Buddy's Verdict", recommendation)

        # 4. Visualizations
        st.subheader(f"Price Chart: {ticker}")
        
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=df.index,
                        open=df['Open'], high=df['High'],
                        low=df['Low'], close=df['Close'], name='Price'))
        
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], line=dict(color='orange', width=1), name='50-Day SMA'))
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 5. Explain the Decision (The "Why")
        st.info(f"**Why this result?** {reasoning}")
        
        # Show News Sources
        with st.expander("See Analyzed News Headlines"):
            for h in headlines:
                st.write(f"- {h}")

    else:
        st.error("Invalid Ticker or No Data Found. Please try 'AAPL', 'TSLA', 'MSFT', etc.")

# --- Disclaimer ---
st.divider()
st.caption("⚠️ **Disclaimer:** This tool uses AI to analyze sentiment and mathematical averages. It is a computer science project, not financial advice. Do not trade real money based on this app.")
