import streamlit as st
import matplotlib.pyplot as plt
from supabase import create_client
from stock_utils import get_stock_data, analyze_stock, get_news
import os

# ---------- SUPABASE ----------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------- PAGE CONFIG ----------
st.set_page_config(layout="wide")

st.title("📊 AI Stock Analyzer (Pro Version)")

# ---------- INPUT SECTION ----------
col1, col2 = st.columns(2)

with col1:
    symbol = st.text_input("Enter Stock Symbol (AAPL, TCS.NS)", "AAPL")

with col2:
    email = st.text_input("Enter Email for Reports")

portfolio = st.text_input("Portfolio (optional)")
alert = st.text_input("Alert (optional)")

# ---------- BUTTON ----------
if st.button("🚀 Analyze Stock"):

    # ---------- FETCH DATA ----------
    data = get_stock_data(symbol)

    if data is None:
        st.error("❌ Invalid stock symbol or no data found")
        st.stop()

    # ---------- ANALYSIS ----------
    result = analyze_stock(data)

    if result is None:
        st.error("❌ Analysis failed")
        st.stop()

    # ---------- GRAPH ----------
    st.subheader(f"{symbol} Price Analysis")

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(data["Close"], linewidth=2)

    ax.set_title(f"{symbol} Price Trend", color="white")
    ax.set_xlabel("Time", color="white")
    ax.set_ylabel("Price", color="white")

    ax.tick_params(colors="white")

    fig.patch.set_facecolor("#0e1117")
    ax.set_facecolor("#0e1117")

    st.pyplot(fig)

    # ---------- METRICS ----------
    st.subheader("📈 AI Insights")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Trend", result["trend"])
    c2.metric("Change %", f"{result['change']}%")
    c3.metric("Sentiment", result["sentiment"])
    c4.metric("Confidence", f"{result['confidence']}%")

    st.success(f"💡 Recommendation: {result['recommendation']}")

    # ---------- NEWS ----------
    st.subheader("📰 Market News")

    news = get_news(symbol)

    for n in news:
        st.write("•", n)

    # ---------- SAVE TO SUPABASE ----------
    if email:
        try:
            supabase.table("users").upsert({
                "email": email,
                "stocks": symbol,
                "portfolio": portfolio,
                "alert": alert
            }).execute()

            st.success("✅ Data saved successfully!")

        except Exception as e:
            st.error(f"❌ Save failed: {e}")


       

       
