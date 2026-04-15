import streamlit as st
from stock_utils import get_stock_data, analyze_stock
from supabase import create_client
import os

# 🔹 Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🔹 UI
st.set_page_config(page_title="AI Stock Analyzer", layout="wide")

st.title("📊 AI Stock Analyzer (Pro Version)")

col1, col2 = st.columns(2)

with col1:
    stock = st.text_input("Enter Stock Symbol (e.g. AAPL, TSLA, TCS.NS)")

with col2:
    email = st.text_input("Enter Email for Reports")

portfolio = st.text_input("Portfolio (optional)")
alert = st.text_input("Alert (optional)")

# 🔹 Button
if st.button("🚀 Analyze Stock"):

    if stock == "" or email == "":
        st.warning("Please enter stock & email")
    else:
        data = get_stock_data(stock)

        if data is None:
            st.error("Invalid stock symbol")
        else:
            result = analyze_stock(data)

            # 📊 GRAPH (FIXED)
            st.subheader(f"{stock} Price Chart")
            st.line_chart(data.set_index("Date")["Close"])

            # 📊 METRICS
            c1, c2, c3 = st.columns(3)

            c1.metric("Trend", result["trend"])
            c2.metric("Change %", result["change"])
            c3.metric("Recommendation", result["recommendation"])

            st.markdown("### 🧠 AI Insight")
            st.info(result["explanation"])

            # 🔹 SAVE TO SUPABASE (UPSERT FIX)
            try:
                supabase.table("users").upsert({
                    "email": email,
                    "stocks": stock,
                    "portfolio": portfolio,
                    "alert": alert
                }).execute()

                st.success("Saved successfully!")

            except Exception as e:
                st.error(f"Save failed: {e}")


       

       
