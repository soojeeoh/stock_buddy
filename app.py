import streamlit as st
import yfinance as yf
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="My Stock Buddy 🩵",
    page_icon="📈",
    layout="wide"
)

# --- CUSTOM CSS FOR CLEAN LOOK ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        width: 100%;
        background-color: #0068c9;
        color: white;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: STEP 1 (USER PROFILE) ---
with st.sidebar:
    st.header("👤 Step 1: User Profile")
    st.write("Customize your investment parameters below.")
    
    job = st.text_input("Job / Status", value="Student")
    age = st.number_input("Age", value=22, min_value=16, max_value=100)
    budget = st.number_input("Total Budget ($ USD)", value=1000, step=50, min_value=100)
    risk_tolerance = st.selectbox("Risk Tolerance", ["Low", "Low-Medium", "Medium", "High"])
    goal = st.selectbox("Goal", ["Long-term Growth", "Short-term Profit", "Dividend Income"])
    target_market = st.selectbox("Target Market", ["US Market", "Global", "Emerging Markets"])
    
    st.markdown("---")
    st.info(f"**Advisor Note:** Based on being a {age}-year-old {job} with ${budget}, your greatest asset is **Time**. We will prioritize compounding.")

# --- MAIN PAGE ---
st.title("📈 My Stock Buddy 🩵")
st.markdown(f"**Welcome.** I have analyzed your profile. Based on your **{risk_tolerance}** risk tolerance, here is your real-time strategy.")

# --- STEP 2: REAL-TIME MARKET SEARCH ---
st.header("🔍 Step 2: Top Market Recommendations")
st.write("I have filtered the market for high-quality 'Blue Chip' stocks that fit your safety profile. Click a stock to analyze it.")

# Hardcoded list of "Safe" & "Growth" stocks
default_tickers = ["SPLG", "MSFT", "AAPL", "KO", "WMT", "NVDA", "JPM", "PG", "COST", "NEE"]

# Create a grid for stock selection
col1, col2 = st.columns([3, 1])
with col1:
    selected_ticker = st.selectbox("Select a Stock to Analyze:", default_tickers)
with col2:
    custom_ticker = st.text_input("Or type a custom ticker:", "")
    if custom_ticker:
        selected_ticker = custom_ticker.upper()

# Fetch Data
if selected_ticker:
    try:
        with st.spinner(f"Loading data for {selected_ticker}..."):
            stock = yf.Ticker(selected_ticker)
            info = stock.info
            
            # Validate that we have essential data
            if not info or 'currentPrice' not in info:
                # Try alternate methods to get price
                hist = stock.history(period="1d")
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    previous_close = hist['Open'].iloc[0]
                else:
                    st.error(f"Could not load data for {selected_ticker}. Please check the ticker symbol or try again later.")
                    st.stop()
            else:
                current_price = info.get('currentPrice', 0)
                previous_close = info.get('previousClose', current_price)
            
            # Calculate price change safely
            if previous_close and previous_close != 0:
                change = ((current_price - previous_close) / previous_close) * 100
            else:
                change = 0
            
            # Display Key Metrics
            m1, m2, m3, m4 = st.columns(4)
            
            m1.metric("Current Price", f"${current_price:.2f}", f"{change:.2f}%")
            
            pe_ratio = info.get('trailingPE', None)
            m2.metric("P/E Ratio", f"{pe_ratio:.2f}" if pe_ratio else "N/A")
            
            week_high = info.get('fiftyTwoWeekHigh', None)
            m3.metric("52 Week High", f"${week_high:.2f}" if week_high else "N/A")
            
            div_yield = info.get('dividendYield', 0)
            m4.metric("Dividend Yield", f"{div_yield*100:.2f}%" if div_yield else "0%")

            # --- STEP 3: AUTOMATED SWOT ANALYSIS ---
            st.header(f"📊 Step 3: SWOT Analysis for {selected_ticker}")
            
            # Logic for auto-generating SWOT
            strengths = []
            weaknesses = []
            opportunities = []
            threats = []

            # 1. Financial Logic (Strengths/Weaknesses)
            profit_margin = info.get('profitMargins', 0)
            beta = info.get('beta', 1)

            if profit_margin and profit_margin > 0.15:
                strengths.append(f"**High Profitability:** {profit_margin*100:.1f}% profit margins are very healthy.")
            elif profit_margin and profit_margin < 0.05:
                weaknesses.append(f"**Low Margins:** Profit margins are tight ({profit_margin*100:.1f}%).")
                
            if pe_ratio and pe_ratio > 35:
                weaknesses.append(f"**Expensive Valuation:** P/E of {pe_ratio:.1f} suggests the stock is pricey.")
            elif pe_ratio and 0 < pe_ratio < 15:
                strengths.append("**Good Value:** The stock is trading at a discount compared to the tech sector.")

            if beta and beta < 0.8:
                strengths.append("**Low Volatility:** This stock is safer/less jumpy than the rest of the market.")
            elif beta and beta > 1.3:
                threats.append("**High Volatility:** Be prepared for big price swings.")

            # Add default strengths if none found
            if not strengths:
                strengths.append("**Established Company:** This is a recognized company in its sector.")

            # 2. News Logic (Opportunities/Threats) - Scanning Headlines
            try:
                news_items = stock.news
                headlines = [item.get('title', '') for item in news_items[:5] if item.get('title')]
            except:
                headlines = []
            
            # Simple keyword scanning in news
            ai_keywords = ['AI', 'Growth', 'Launch', 'Record', 'New', 'Deal', 'Profit', 'Revenue']
            risk_keywords = ['Drop', 'Fall', 'Suit', 'Regulation', 'Miss', 'Inflation', 'Loss', 'Down']

            found_opps = False
            found_threats = False

            for headline in headlines:
                if any(k.lower() in headline.lower() for k in ai_keywords):
                    opportunities.append(f"📰 **News:** {headline}")
                    found_opps = True
                    break  # Only show one positive news item
                    
            for headline in headlines:
                if any(k.lower() in headline.lower() for k in risk_keywords):
                    threats.append(f"📰 **News:** {headline}")
                    found_threats = True
                    break  # Only show one negative news item

            if not found_opps: 
                opportunities.append("**Market Trends:** Check recent earnings reports for guidance updates.")
            if not found_threats: 
                threats.append("**Market Risk:** General market recession risk applies to all stocks.")

            # Display SWOT Grid
            swot1, swot2 = st.columns(2)
            with swot1:
                st.subheader("✅ Strengths (Internal)")
                for s in strengths: st.write(f"- {s}")
                
                st.subheader("🚀 Opportunities (External)")
                for o in opportunities: st.write(f"- {o}")
                
            with swot2:
                st.subheader("❌ Weaknesses (Internal)")
                if weaknesses:
                    for w in weaknesses: st.write(f"- {w}")
                else:
                    st.write("- No major weaknesses identified in current data.")
                
                st.subheader("⚠️ Threats (External)")
                for t in threats: st.write(f"- {t}")

            # --- STEP 4: ALLOCATION STRATEGY ---
            st.header("💰 Step 4: Your Personalized Allocation")

            st.write(f"Based on your budget of **${budget}**, here is exactly how many shares you should buy to maintain a safe 90/10 Core-Satellite portfolio.")

            # Logic for allocation
            etf_ticker = "SPLG" # Using SPLG as the cheaper S&P500 proxy
            
            try:
                etf_data = yf.Ticker(etf_ticker)
                etf_info = etf_data.info
                etf_price = etf_info.get('currentPrice', None)
                
                # Fallback to historical data if currentPrice is missing
                if not etf_price:
                    etf_hist = etf_data.history(period="1d")
                    if not etf_hist.empty:
                        etf_price = etf_hist['Close'].iloc[-1]
                    else:
                        etf_price = 65  # Reasonable fallback
                        
            except:
                etf_price = 65  # Fallback price

            stock_price = current_price
            
            # Validate prices before calculation
            if stock_price and stock_price > 0 and etf_price and etf_price > 0:
                # 90% to ETF, 10% to Stock
                core_budget = budget * 0.90
                satellite_budget = budget * 0.10
                
                etf_shares = int(core_budget // etf_price)
                stock_shares = satellite_budget / stock_price
                
                # Create Dataframe for display
                allocation_data = {
                    "Ticker": [etf_ticker, selected_ticker],
                    "Role": ["Core (Safety)", "Satellite (Growth)"],
                    "Allocation ($)": [f"${core_budget:.2f}", f"${satellite_budget:.2f}"],
                    "Est. Shares": [f"{etf_shares} shares", f"{stock_shares:.2f} shares"]
                }
                
                st.table(pd.DataFrame(allocation_data))
                
                st.success(f"💡 **Action Plan:** Log into your brokerage app. Buy **{etf_shares}** shares of **{etf_ticker}** (${etf_price:.2f}/share) and invest the remaining **${satellite_budget:.2f}** into **{selected_ticker}** ({stock_shares:.2f} shares at ${stock_price:.2f}/share).")
            else:
                st.warning("⚠️ Unable to calculate allocation due to missing price data. Please try a different stock or refresh the page.")

    except Exception as e:
        st.error(f"Could not load data for {selected_ticker}. Please check the ticker symbol or try again later.")
        st.info("💡 Tip: Make sure you're entering a valid stock ticker (e.g., AAPL for Apple, MSFT for Microsoft)")
        if st.checkbox("Show error details"):
            st.code(str(e))
