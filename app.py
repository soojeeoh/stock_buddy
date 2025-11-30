# Conceptual code for app.py
import streamlit as st
import yfinance as yf

# 1. Title and Simple Terms
st.title("Stock Buddy 🤖")
st.write("Your beginner-friendly guide to the market.")

# 2. Sidebar for User Input
money = st.number_input("How much do you want to invest?", min_value=100)
strategy = st.radio("What is your goal?", ["Short-term (High Risk/High Reward)", "Long-term (Steady Growth)"])

# 3. The 'Fake' AI Logic (You will replace this with real Sentiment Analysis later)
if st.button("Ask Stock Buddy"):
    st.write(f"Analyzing current news for {strategy} investment...")
    
    # Logic placeholder
    if strategy == "Long-term (Steady Growth)":
        st.success(f"Recommendation: With ${money}, consider 'Blue Chip' stocks like Apple or Microsoft. The news today indicates steady product launches.")
    else:
        st.warning(f"Recommendation: With ${money}, you might look at Tech Startups, but be careful! Social media shows high hype but high risk.")

# 4. Dashboard
st.subheader("Today's Top Movers")
# Fetch real data here using yfinance
ticker = "AAPL"
data = yf.Ticker(ticker).history(period="1d")
st.metric(label="Apple Inc.", value=f"${data['Close'][0]:.2f}", delta="1.2%")
