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
    result = analyze_stock(data)

    # GRAPH
    st.subheader(f"{symbol} Analysis")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(data["Close"], color="cyan")
    ax.set_facecolor("#0e1117")
    fig.patch.set_facecolor("#0e1117")
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
    news = get_news(symbol)
    for n in news:
        st.write("•", n)

    # SAVE USER (FIXED UPSERT)
    if email:
        try:
            supabase.table("users").upsert({
                "email": email,
                "stocks": symbol,
                "portfolio": portfolio,
                "alert": alert
            }).execute()

            st.success("Saved successfully!")
        except Exception as e:
            st.error(f"Save failed: {e}")


       

       
