import streamlit as st
import yfinance as yf
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="My Stock Buddy 🩵",
    page_icon="📈",
    layout="wide"
)

# --- CSS FOR CLEAN DESIGN ---
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
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("My Stock Buddy 🩵")
st.markdown("### Specialized in explaining complex concepts to beginners.")
st.markdown("---")

# --- SIDEBAR: USER PROFILE (STEP 1) ---
st.sidebar.header("Step 1: Create Your Profile")

job = st.sidebar.text_input("Current Job/Status", value="Student")
budget = st.sidebar.number_input("Total Budget ($ USD)", min_value=100, value=1000, step=50)
risk = st.sidebar.selectbox("Risk Tolerance", ["Low", "Low to Medium", "Medium", "High"])
goal = st.sidebar.selectbox("Goal", ["Long-term growth", "Day Trading", "Retirement", "Savings"])
knowledge = st.sidebar.selectbox("Knowledge Level", ["Zero (Beginner)", "Intermediate", "Advanced"])
market = st.sidebar.text_input("Target Market", value="US Stocks")

if st.sidebar.button("Generate Strategy"):
    st.session_state['profile_submitted'] = True

# --- MAIN CONTENT LOGIC ---

if 'profile_submitted' not in st.session_state:
    st.info("👈 Please fill out your profile in the sidebar and click 'Generate Strategy' to begin.")
    
else:
    # === STEP 1: STRATEGY ===
    st.header(f"👋 Hello, {job}!")
    st.success(f"Strategy: Since your goal is **{goal}** with **{risk}** risk, we recommend a 'Diversification' strategy.")
    
    with st.expander("📖 Click here to understand the basic terms"):
        st.write("""
        - **ETF (Exchange Traded Fund):** A basket of many stocks. Buying one ETF share is like buying a tiny piece of hundreds of companies at once.
        - **Diversification:** Not putting all your eggs in one basket.
        - **Blue Chip Stocks:** Huge, reliable companies (like Apple or Microsoft).
        """)

    st.markdown("---")

    # === STEP 2: REAL-TIME SEARCHING ===
    st.header("Step 2: Market Snapshot")
    st.write(f"Scanning the **{market}** for top stable companies...")

    # Define top stable stocks (Blue Chips)
    tickers = ["MSFT", "AAPL", "GOOGL", "AMZN", "NVDA"]
    
    # Fetch live data
    data_list = []
    try:
        for ticker in tickers:
            stock = yf.Ticker(ticker)
            info = stock.info
            price = info.get('currentPrice', info.get('regularMarketPrice', 0))
            name = info.get('shortName', ticker)
            # Simulating news summary (Real-time news API requires paid keys)
            news_summary = "Leading market innovation and AI development." 
            
            data_list.append({
                "Ticker": ticker,
                "Company": name,
                "Price ($)": f"${price:.2f}",
                "Status": "Stable / Blue Chip"
            })
        
        df = pd.DataFrame(data_list)
        st.table(df)
        
    except Exception as e:
        st.error(f"Could not fetch live data: {e}")

    st.markdown("---")

    # === STEP 3: SWOT ANALYSIS ===
    st.header("Step 3: AI Analysis (SWOT)")
    
    selected_ticker = st.selectbox("Select a company to analyze:", tickers)
    
    # Dictionary of pre-analyzed SWOTs (For demo purposes)
    swot_data = {
        "MSFT": {
            "S": "Strong integration of AI (OpenAI partnership).",
            "W": "Hardware dependency on other chip makers.",
            "O": "Growth in Cloud Computing (Azure).",
            "T": "Regulatory scrutiny on monopoly power.",
            "Risk": "Medium"
        },
        "AAPL": {
            "S": "Extremely loyal customer base (iPhone ecosystem).",
            "W": "Slower rollout of Generative AI features.",
            "O": "Services revenue (App Store, Music) is growing.",
            "T": "Legal battles with the DOJ.",
            "Risk": "Medium"
        },
        "NVDA": {
            "S": "Dominates 90% of the AI chip market.",
            "W": "Supply chain cannot keep up with demand.",
            "O": "New Blackwell chips sold out through 2025.",
            "T": "Big customers (Google/Microsoft) building their own chips.",
            "Risk": "High"
        },
        "GOOGL": {
            "S": "Search engine monopoly and efficient chip design (TPU).",
            "W": " reliance on ad revenue.",
            "O": "Gemini AI model integration.",
            "T": "Major government lawsuits to break up the company.",
            "Risk": "Medium-High"
        },
        "AMZN": {
            "S": "King of Logistics and Cloud (AWS).",
            "W": "Low profit margins on retail items.",
            "O": "Automation and AI in warehouses.",
            "T": "Competition from low-cost apps (Temu/Shein).",
            "Risk": "Medium"
        }
    }

    if selected_ticker:
        analysis = swot_data[selected_ticker]
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Strengths:** {analysis['S']}")
            st.warning(f"**Weaknesses:** {analysis['W']}")
        with col2:
            st.success(f"**Opportunities:** {analysis['O']}")
            st.error(f"**Threats:** {analysis['T']}")
        
        st.caption(f"**Advisor Verdict:** This stock is rated **{analysis['Risk']} Risk**.")

    st.markdown("---")

    # === STEP 4: FEASIBILITY CHECK ===
    st.header("Step 4: Can you afford it?")
    
    # Fetch VOO price (The generic recommendation)
    voo = yf.Ticker("VOO")
    voo_price = voo.info.get('currentPrice', 500) # Fallback if API fails
    
    st.subheader("Benchmark: Vanguard S&P 500 ETF (VOO)")
    st.metric(label="Current VOO Price", value=f"${voo_price:.2f}")
    
    shares_affordable = budget / voo_price
    
    st.write(f"With your budget of **${budget}**, you can buy:")
    st.markdown(f"## {shares_affordable:.2f} Shares")
    
    if shares_affordable < 1:
        st.warning("You cannot buy a full share, but don't worry! Use a broker that supports **Fractional Shares**.")
    else:
        st.success("You can buy full shares!")

    st.markdown("### Next Steps:")
    st.markdown("""
    1. Open a brokerage account (Robinhood, Fidelity, Schwab).
    2. Deposit your **$%s**.
    3. Search for **VOO** (Low Fee) or individual stocks from Step 2.
    """ % budget)

