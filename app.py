import streamlit as st
import matplotlib.pyplot as plt
from supabase import create_client
from stock_utils import get_stock_data, analyze_stock, get_news
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(layout="wide")

st.title("📊 AI Stock Analyzer (Pro Version)")

col1, col2 = st.columns(2)

with col1:
    symbol = st.text_input("Enter Stock (AAPL, TCS.NS)", "AAPL")

with col2:
    email = st.text_input("Enter Email")

portfolio = st.text_input("Portfolio (optional)")
alert = st.text_input("Alert (optional)")

if st.button("🚀 Analyze Stock"):

    data = get_stock_data(symbol)

    if data is None:
        st.error("Invalid stock")
        st.stop()

    result = analyze_stock(data)

    # 🔥 PROFESSIONAL GRAPH
    plt.style.use("dark_background")

    fig, ax = plt.subplots(figsize=(12, 4))

    smooth = data["Close"].rolling(5).mean()

    ax.plot(data["Close"], alpha=0.3)
    ax.plot(smooth, linewidth=2)

    ax.set_title(f"{symbol} Price Trend")
    ax.grid(alpha=0.2)

    st.pyplot(fig)

    # METRICS
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Trend", result["trend"])
    c2.metric("Change %", f"{result['change']}%")
    c3.metric("Sentiment", result["sentiment"])
    c4.metric("Confidence", f"{result['confidence']}%")

    st.success(f"Recommendation: {result['recommendation']}")

    # NEWS
    st.subheader("📰 News")
    for n in get_news(symbol):
        st.write("•", n)

    # SAVE USER
    if email:
        supabase.table("users").upsert({
            "email": email,
            "stocks": symbol,
            "portfolio": portfolio,
            "alert": alert
        }).execute()

        st.success("Saved successfully!")



       

       
