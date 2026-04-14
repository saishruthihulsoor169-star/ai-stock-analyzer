import streamlit as st
from stock_utils import analyze_stock

st.title("📊 AI Stock Analyzer")

stock = st.text_input("Enter Stock Symbol (e.g. TCS.NS)")

if st.button("Analyze"):
    if stock:
        result = analyze_stock(stock)

        # Handle errors safely
        if not result or "trend" not in result:
            st.error("❌ Failed to fetch stock data")
        else:
            suggestion = "BUY 🟢" if "UP" in result["trend"] else "SELL 🔴"

            st.subheader("📈 Result")
            st.write("Trend:", result["trend"])
            st.write("Change:", result["change"], "%")
            st.write("Sentiment:", result["sentiment"])
            st.write("Suggestion:", suggestion)

            st.subheader("📰 News")
            for h in result["headlines"]:
                st.write("-", h)

            st.image("chart.png")

    else:
        st.warning("Please enter a stock name")


       

       
