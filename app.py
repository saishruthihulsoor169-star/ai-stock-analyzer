import streamlit as st
from stock_utils import get_stock_data
from supabase import create_client
import matplotlib.pyplot as plt

# =========================
# 🔐 Supabase Connection
# =========================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# =========================
# 🎨 Page Config
# =========================
st.set_page_config(page_title="AI Stock Analyzer", layout="wide")

st.title("📊 AI Stock Analyzer Pro")
st.markdown("Analyze any stock, visualize trends, and receive daily reports 🚀")

# =========================
# 🧾 Inputs
# =========================
stock_input = st.text_input(
    "📌 Enter Stock Symbol (e.g. AAPL, TSLA, TCS.NS, BTC-USD)"
)

email = st.text_input("📧 Enter your Email for daily reports")

# =========================
# 🔍 Analyze Button
# =========================
if st.button("🚀 Analyze & Save"):

    if not stock_input:
        st.warning("Please enter a stock symbol")
        st.stop()

    result = get_stock_data(stock_input.upper())

    # =========================
    # ❌ Error Handling
    # =========================
    if result is None:
        st.error("❌ Invalid stock / API rate limit hit")
        st.stop()

    # =========================
    # ✅ Show Results
    # =========================
    st.success("✅ Analysis Complete")

    st.subheader(f"📈 {stock_input.upper()} Analysis")

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Price", result["price"])
    col2.metric("📊 Change %", result["change"])
    col3.metric("📉 Trend", result["trend"])

    # =========================
    # 📊 Chart
    # =========================
    st.subheader("📉 Price Trend")

    fig, ax = plt.subplots()
    result["data"]["Close"].plot(ax=ax)
    ax.set_title(f"{stock_input.upper()} Price Movement")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")

    st.pyplot(fig)

    # =========================
    # 💾 Save to Supabase
    # =========================
    if email:

        try:
            supabase.table("users").upsert({
                "email": email,
                "stocks": stock_input.upper()
            }).execute()

            st.success("💾 Saved! You will receive daily reports at 9 AM 🚀")

        except Exception as e:
            st.error(f"❌ Failed to save user: {e}")

    else:
        st.info("💡 Enter email to receive daily automated reports")


       

       
