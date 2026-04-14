import streamlit as st
from stock_utils import get_stock_data
from supabase import create_client
import os
import matplotlib.pyplot as plt

# Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="AI Stock Analyzer", layout="wide")

st.title("📊 AI Stock Analyzer (Pro)")

stock_input = st.text_input("Enter Stock Symbol (e.g. AAPL, TSLA, TCS.NS)")
email = st.text_input("Enter your Email")

if st.button("Analyze & Save"):

    result = get_stock_data(stock_input.upper())

    if result is None:
        st.error("Invalid stock or rate limit")
    else:
        st.success("Analysis Complete")

        st.subheader(f"{stock_input.upper()} Analysis")

        col1, col2, col3 = st.columns(3)

        col1.metric("Price", result["price"])
        col2.metric("Change %", result["change"])
        col3.metric("Trend", result["trend"])

        # 📊 Chart
        fig, ax = plt.subplots()
        result["data"]["Close"].plot(ax=ax)
        ax.set_title("Price Trend")
        st.pyplot(fig)

        # Save user
        if email:
            supabase.table("users").insert({
                "email": email,
                "stocks": stock_input.upper()
            }).execute()

            st.success("Saved for daily reports 🚀")


       

       
