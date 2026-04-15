import streamlit as st
from stock_utils import get_stock_data
from supabase import create_client
import matplotlib.pyplot as plt

# =========================
# 🔐 Supabase (Streamlit Secrets)
# =========================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# =========================
# 🎨 UI
# =========================
st.set_page_config(page_title="AI Stock Analyzer", layout="wide")

st.title("📊 AI Stock Analyzer Pro")
st.markdown("Analyze any stock, visualize trends, and get daily reports 🚀")

# =========================
# 🧾 Inputs
# =========================
stock_input = st.text_input("📌 Enter Stock (AAPL, TSLA, TCS.NS, BTC-USD)")
email = st.text_input("📧 Enter Email for Daily Reports")

# =========================
# 🔍 Button
# =========================
if st.button("🚀 Analyze & Save"):

    if not stock_input:
        st.warning("Enter stock symbol")
        st.stop()

    result = get_stock_data(stock_input.upper())

    if result is None:
        st.error("Invalid stock / Rate limit")
        st.stop()

    st.success("Analysis Ready ✅")

    st.subheader(f"{stock_input.upper()} Analysis")

    col1, col2, col3 = st.columns(3)
    col1.metric("Price", result["price"])
    col2.metric("Change %", result["change"])
    col3.metric("Trend", result["trend"])

    # =========================
    # 📊 Chart (FIXED SIZE)
    # =========================
    st.subheader("📉 Price Trend")

    fig, ax = plt.subplots(figsize=(6, 3))
    result["data"]["Close"].plot(ax=ax)

    ax.set_title(f"{stock_input.upper()} Price Movement", fontsize=10)
    ax.set_xlabel("")
    ax.set_ylabel("Price", fontsize=8)

    st.pyplot(fig, use_container_width=True)

    # =========================
    # 💾 Save User
    # =========================
    if email:
        try:
            response = supabase.table("users").upsert({
                "email": email,
                "stocks": stock_input.upper()
            }).execute()

            st.write("DEBUG:", response)

            st.success("Saved! Daily emails at 9 AM 🚀")

        except Exception as e:
            st.error(f"Save failed: {e}")
    else:
        st.info("Enter email to receive daily reports")


       

       
