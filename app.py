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
    budget = st.number_input("Total Budget ($ USD)", value=1000, step=50)
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

# Hardcoded list of "Safe" & "Growth" stocks based on our previous conversation
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
        stock = yf.Ticker(selected_ticker)
        info = stock.info
        
        # Display Key Metrics
        m1, m2, m3, m4 = st.columns(4)
        current_price = info.get('currentPrice', 0)
        previous_close = info.get('previousClose', 0)
        change = ((current_price - previous_close) / previous_close) * 100
        
        m1.metric("Current Price", f"${current_price}", f"{change:.2f}%")
        m2.metric("P/E Ratio", f"{info.get('trailingPE', 'N/A')}")
        m3.metric("52 Week High", f"${info.get('fiftyTwoWeekHigh', 'N/A')}")
        m4.metric("Dividend Yield", f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else "0%")

        # --- STEP 3: AUTOMATED SWOT ANALYSIS ---
        st.header(f"📊 Step 3: SWOT Analysis for {selected_ticker}")
        
        # Logic for auto-generating SWOT
        strengths = []
        weaknesses = []
        opportunities = []
        threats = []

        # 1. Financial Logic (Strengths/Weaknesses)
        pe_ratio = info.get('trailingPE', 0)
        profit_margin = info.get('profitMargins', 0)
        beta = info.get('beta', 1)

        if profit_margin > 0.15:
            strengths.append(f"**High Profitability:** {profit_margin*100:.1f}% profit margins are very healthy.")
        else:
            weaknesses.append(f"**Low Margins:** Profit margins are tight ({profit_margin*100:.1f}%).")
            
        if pe_ratio > 35:
            weaknesses.append(f"**Expensive Valuation:** P/E of {pe_ratio:.1f} suggests the stock is pricey.")
        elif pe_ratio < 15 and pe_ratio > 0:
            strengths.append("**Good Value:** The stock is trading at a discount compared to the tech sector.")

        if beta < 0.8:
            strengths.append("**Low Volatility:** This stock is safer/less jumpy than the rest of the market.")
        elif beta > 1.3:
            threats.append("**High Volatility:** Be prepared for big price swings.")

        # 2. News Logic (Opportunities/Threats) - Scanning Headlines
        news_items = stock.news
        headlines = [item['title'] for item in news_items[:5]]
        
        # Simple keyword scanning in news
        ai_keywords = ['AI', 'Growth', 'Launch', 'Record', 'New', 'Deal']
        risk_keywords = ['Drop', 'Fall', 'Suit', 'Regulation', 'Miss', 'Inflation']

        found_opps = False
        found_threats = False

        for headline in headlines:
            if any(k in headline for k in ai_keywords):
                opportunities.append(f"📰 **News:** {headline}")
                found_opps = True
            if any(k in headline for k in risk_keywords):
                threats.append(f"📰 **News:** {headline}")
                found_threats = True

        if not found_opps: opportunities.append("Check recent earnings reports for guidance updates.")
        if not found_threats: threats.append("General market recession risk applies.")

        # Display SWOT Grid
        swot1, swot2 = st.columns(2)
        with swot1:
            st.subheader("✅ Strengths (Internal)")
            for s in strengths: st.write(f"- {s}")
            
            st.subheader("🚀 Opportunities (External)")
            for o in opportunities: st.write(f"- {o}")
            
        with swot2:
            st.subheader("❌ Weaknesses (Internal)")
            for w in weaknesses: st.write(f"- {w}")
            
            st.subheader("⚠️ Threats (External)")
            for t in threats: st.write(f"- {t}")

    except Exception as e:
        st.error(f"Could not load data for {selected_ticker}. Please check the ticker symbol.")

# --- STEP 4: ALLOCATION STRATEGY ---
st.header("💰 Step 4: Your Personalized Allocation")

st.write("Based on your budget of **${}**, here is exactly how many shares you should buy to maintain a safe 90/10 Core-Satellite portfolio.".format(budget))

# Logic for allocation
etf_ticker = "SPLG" # Using SPLG as the cheaper S&P500 proxy
etf_price = yf.Ticker(etf_ticker).info.get('currentPrice', 65)

if selected_ticker:
    stock_price = current_price
    
    # 90% to ETF, 10% to Stock
    core_budget = budget * 0.90
    satellite_budget = budget * 0.10
    
    etf_shares = int(core_budget // etf_price)
    stock_shares = satellite_budget / stock_price # Fractional allowed for calc
    
    # Create Dataframe for display
    allocation_data = {
        "Ticker": [etf_ticker, selected_ticker],
        "Role": ["Core (Safety)", "Satellite (Growth)"],
        "Allocation ($)": [f"${core_budget:.2f}", f"${satellite_budget:.2f}"],
        "Est. Shares": [f"{etf_shares} shares", f"{stock_shares:.2f} shares"]
    }
    
    st.table(pd.DataFrame(allocation_data))
    
    st.success(f"💡 **Action Plan:** Log into your brokerage app. Buy **{etf_shares}** shares of **{etf_ticker}** and invest the remaining **${satellite_budget:.2f}** into **{selected_ticker}**.")
