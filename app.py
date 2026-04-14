import streamlit as st
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from stock_utils import analyze_stock

# Page config
st.set_page_config(page_title="AI Stock Analyzer", layout="centered")

# Header
st.markdown("<h1 style='text-align: center;'>📊 AI Stock Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Analyze any stock & get email reports</p>", unsafe_allow_html=True)

st.divider()

# Input
stocks_input = st.text_input(
    "📌 Enter Stock Symbols (comma separated)",
    placeholder="e.g. tesla, AAPL, TCS.NS"
)

receiver = st.text_input("📧 Enter your Email")

st.info("💡 Examples:\n- tesla → TSLA\n- apple → AAPL\n- tcs → TCS.NS")

# Name → ticker mapping
name_to_ticker = {
    "tesla": "TSLA",
    "apple": "AAPL",
    "google": "GOOGL",
    "amazon": "AMZN",
    "microsoft": "MSFT",
    "tcs": "TCS.NS",
    "infosys": "INFY.NS",
    "reliance": "RELIANCE.NS"
}

# Button
if st.button("🚀 Analyze & Send Report", use_container_width=True):

    if not stocks_input or not receiver:
        st.warning("⚠️ Enter stock and email")
        st.stop()

    # Convert input → ticker
    stocks = []
    for s in stocks_input.split(","):
        s = s.strip().lower()
        if s in name_to_ticker:
            stocks.append(name_to_ticker[s])
        else:
            stocks.append(s.upper())

    # Limit
    if len(stocks) > 3:
        st.warning("⚠️ Max 3 stocks allowed")
        st.stop()

    results = []

    # Analyze
    with st.spinner("Analyzing stocks..."):
        for stock in stocks:
            result = analyze_stock(stock)

            if result is None:
                st.error(f"❌ {stock} invalid")
                continue

            if "error" in result:
                st.error(f"❌ Failed: {stock}")
                continue

            results.append((stock, result))

    if not results:
        st.error("❌ No valid stock data")
        st.stop()

    # Display
    st.subheader("📈 Results")

    for stock, res in results:
        st.markdown(f"### {stock}")
        st.markdown(f"**Trend:** {res['trend']}")
        st.markdown(f"**Change:** {res['change']}%")
        st.markdown(f"**Sentiment:** {res['sentiment']} ({res['sentiment_score']})")

        # Step 2 (AI part)
        if "recommendation" in res:
            st.markdown(f"**Recommendation:** {res['recommendation']}")
            st.markdown(f"**Confidence:** {res['confidence']}%")

        for h in res["headlines"]:
            st.write("•", h)

    # Email
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    try:
        msg = MIMEMultipart()
        msg["Subject"] = "📊 Stock Report"
        msg["From"] = sender
        msg["To"] = receiver

        html = "<h2>Stock Report</h2><hr>"

        for stock, res in results:
            html += f"""
            <h3>{stock}</h3>
            <p>Trend: {res['trend']}</p>
            <p>Change: {res['change']}%</p>
            <p>Sentiment: {res['sentiment']} ({res['sentiment_score']})</p>
            """

            if "recommendation" in res:
                html += f"""
                <p>Recommendation: {res['recommendation']}</p>
                <p>Confidence: {res['confidence']}%</p>
                """

            html += "<ul>"
            for h in res["headlines"]:
                html += f"<li>{h}</li>"
            html += "</ul><hr>"

        msg.attach(MIMEText(html, "html"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()

        st.success("📧 Email sent!")

    except Exception as e:
        st.error(f"❌ Email error: {e}")


       

       
