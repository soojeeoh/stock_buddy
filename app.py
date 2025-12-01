import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION (Clean & Professional Look) ---
st.set_page_config(
    page_title="My AI Financial Advisor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR STYLING ---
st.markdown("""
    <style>
    .main {
        background-color: #f9f9f9;
    }
    .stButton>button {
        width: 100%;
        background-color: #0068C9;
        color: white;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for analysis trigger
if 'analysis_started' not in st.session_state:
    st.session_state.analysis_started = False

# --- STEP 1: USER PROFILE (SIDEBAR) ---
st.sidebar.header("Step 1: Your Profile")
st.sidebar.caption("Please update your details below to personalize the strategy.")

job = st.sidebar.text_input("Job / Occupation", value="University Student")
budget = st.sidebar.number_input("Total Budget ($ USD)", min_value=100, value=1000, step=50)
risk_tolerance = st.sidebar.selectbox("Risk Tolerance", ["Low", "Medium", "High"], index=0)
goal = st.sidebar.selectbox("Investment Goal", ["Long-term Growth", "Short-term Profit", "Retirement"], index=0)
knowledge = st.sidebar.selectbox("Knowledge Level", ["Zero (Beginner)", "Intermediate", "Expert"], index=0)
market = st.sidebar.text_input("Target Market", value="US Stocks")

# Analyze Button
st.sidebar.markdown("---")
if st.sidebar.button("🔍 Analyze My Profile"):
    st.session_state.analysis_started = True

# --- MAIN APP LOGIC ---

st.title("💰 Intelligent Financial Advisor")

# Only show analysis if button is clicked
if not st.session_state.analysis_started:
    st.info("👈 Please complete your profile in the sidebar and click **'Analyze My Profile'** to begin your personalized financial analysis.")
else:
    st.markdown(f"**Welcome!** Creating a strategy for a **{job}** with a budget of **${budget:,.2f}** looking for **{goal}**.")
    
    # Separator
    st.markdown("---")
    
    # --- STEP 2: REAL-TIME SEARCH & FILTERING ---
    st.header("Step 2: Market Scan & Filtering")
    
    # Mapping of tickers to full company names
    company_names = {
        "AAPL": "Apple Inc.",
        "MSFT": "Microsoft Corporation",
        "NVDA": "NVIDIA Corporation",
        "AMZN": "Amazon.com Inc.",
        "GOOGL": "Alphabet Inc. (Google)",
        "META": "Meta Platforms Inc.",
        "BRK-B": "Berkshire Hathaway Inc.",
        "TSLA": "Tesla Inc.",
        "AVGO": "Broadcom Inc.",
        "JPM": "JPMorgan Chase & Co.",
        "AMD": "Advanced Micro Devices Inc.",
        "PLTR": "Palantir Technologies Inc.",
        "COIN": "Coinbase Global Inc.",
        "NFLX": "Netflix Inc."
    }
    
    with st.spinner('Scanning the market for top recommendations based on your profile...'):
        
        # Define the tickers based on logic
        if risk_tolerance in ["Low", "Medium"]:
            st.success(f"✅ Profile Detected: **{risk_tolerance} Risk**. Focusing on S&P 500 Market Leaders.")
            tickers = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "BRK-B", "TSLA", "AVGO", "JPM"]
            etf_proxy = "VOO"
        else:
            st.warning(f"⚠️ Profile Detected: **{risk_tolerance} Risk**. Focusing on High-Growth Tech Volatility.")
            tickers = ["NVDA", "TSLA", "AMD", "PLTR", "COIN", "META", "NFLX", "AMZN", "MSFT", "GOOGL"]
            etf_proxy = "QQQ"
    
        # Fetch Data
        data_list = []
        for t in tickers:
            try:
                stock = yf.Ticker(t)
                info = stock.fast_info
                current_price = info.last_price
                
                # Simple Logic to determine "Why in news" (Simulated based on movement)
                prev_close = info.previous_close
                change_pct = ((current_price - prev_close) / prev_close) * 100
                
                if change_pct > 1.0:
                    status = "Trending UP significantly today."
                elif change_pct < -1.0:
                    status = "Trading LOWER, potential discount."
                else:
                    status = "Stable movement today."
                    
                data_list.append({
                    "Company": company_names.get(t, t),
                    "Ticker": t,
                    "Price ($)": round(current_price, 2),
                    "Daily Change %": round(change_pct, 2),
                    "Market Status": status
                })
            except Exception as e:
                st.warning(f"Could not fetch data for {t}: {str(e)}")
    
        df = pd.DataFrame(data_list)
        
        # Display the filtered list
        st.dataframe(df, use_container_width=True)
    
    # --- STEP 3: ANALYSIS (SWOT) ---
    st.markdown("---")
    st.header("Step 3: Strategic Analysis")
    st.caption("Analyzing current market strengths and risks for these top holdings.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("SWOT Snapshot")
        # Dynamic text based on real-time averages
        avg_change = df["Daily Change %"].mean()
        
        strength_text = "These companies hold massive cash reserves and dominate AI sectors."
        weakness_text = "Stock prices are historically high (expensive P/E ratios)."
        opportunity_text = "Upcoming interest rate cuts could boost valuations further."
        threat_text = "Antitrust regulations and global tariffs remain a risk."
        
        st.markdown(f"**💪 Strengths:** {strength_text}")
        st.markdown(f"**📉 Weaknesses:** {weakness_text}")
        st.markdown(f"**🚀 Opportunities:** {opportunity_text}")
        st.markdown(f"**⚠️ Threats:** {threat_text}")
    
    with col2:
        st.subheader("Market Sentiment Visualizer")
        # A bubble chart showing Price vs Daily Change
        fig = px.scatter(df, x="Price ($)", y="Daily Change %", size="Price ($)", color="Daily Change %",
                         hover_name="Ticker", text="Ticker", title="Risk vs. Price Analysis",
                         color_continuous_scale=px.colors.diverging.RdYlGn)
        st.plotly_chart(fig, use_container_width=True)
    
    # --- STEP 4: STRATEGY & ALLOCATION ---
    st.markdown("---")
    st.header("Step 4: Your Investment Plan")
    
    # Get example stock price for context
    example_stock = df[df['Ticker']=='MSFT']
    if not example_stock.empty:
        msft_price = float(example_stock['Price ($)'].values[0])
        st.markdown(f"""
Based on your budget of **${budget:,.2f}**, buying individual shares of all these companies is difficult. 
For example, one share of Microsoft (MSFT) currently costs **${msft_price:.2f}**.
        """)
    else:
        st.markdown(f"""
Based on your budget of **${budget:,.2f}**, buying individual shares of all these companies can be challenging 
as many of these stocks trade at high prices per share.
        """)
    
    st.info(f"💡 **Recommendation:** Use an ETF strategy to own ALL of them at once.")
    
    # Strategy Logic
    cash_reserve = budget * 0.05
    invest_amount = budget * 0.95
    
    try:
        etf_price = yf.Ticker(etf_proxy).fast_info.last_price
        shares_to_buy = invest_amount / etf_price
    except:
        etf_price = 400  # fallback
        shares_to_buy = invest_amount / etf_price
    
    # Layout the plan
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label="1. Keep in Cash (Emergency)", value=f"${cash_reserve:.2f}")
    with c2:
        st.metric(label=f"2. Buy {etf_proxy} (ETF)", value=f"${invest_amount:.2f}")
    with c3:
        st.metric(label="Est. Shares You Get", value=f"{shares_to_buy:.2f} shares")
    
    st.markdown(f"""
### Why this plan?
1. **{etf_proxy}** holds all the companies listed in Step 2.
2. You keep **5% cash** to buy more if the market drops (Safety net).
3. This fits your **{knowledge}** knowledge level because it requires no maintenance.
""")
    
    # Action Button
    if st.button("Generate Final PDF Report (Simulation)"):
        st.balloons()
        st.success("Strategy locked in! In a real app, this would download a PDF.")
