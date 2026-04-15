import streamlit as st
from stock_utils import get_stock_data, analyze_stock
from supabase import create_client
import os

# Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="AI Stock Analyzer", layout="wide")

st.title("📊 AI Stock Analyzer (Pro Version)")

# INPUT SECTION
col1, col2 = st.columns(2)

with col1:
    stock = st.text_input("Enter Stock Symbol (e.g. AAPL, TSLA, TCS.NS)")

with col2:
    email = st.text_input("Enter Email for Daily Reports")

portfolio = st.text_input("Portfolio (e.g. AAPL:5, TSLA:2)")
alert = st.text_input("Alert (e.g. TSLA > 200)")

if st.button("🚀 Analyze Stock"):

    if stock:
        data = get_stock_data(stock)

        if data is not None:

            result = analyze_stock(data)

            st.subheader(f"📈 {stock} Analysis")

            # CLEAN GRAPH
            st.line_chart(data["Close"])

            col1, col2, col3 = st.columns(3)

            col1.metric("Trend", result["trend"])
            col2.metric("Change %", result["change"])
            col3.metric("Recommendation", result["recommendation"])

            st.write("### 📰 News")
            for news in result["news"]:
                st.write(f"- {news}")

            # SAVE TO SUPABASE
            if email:
                try:
                    supabase.table("users").insert({
                        "email": email,
                        "stocks": stock,
                        "portfolio": portfolio,
                        "alert": alert
                    }).execute()

                    st.success("✅ Saved successfully!")

                except Exception as e:
                    st.error(f"Save failed: {e}")

        else:
            st.error("Invalid stock symbol")


       

       
