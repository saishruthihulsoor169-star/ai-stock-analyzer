import streamlit as st
import smtplib
import os
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from stock_utils import analyze_stock

# ---------- USER STORAGE ----------
def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(data):
    with open("users.json", "w") as f:
        json.dump(data, f, indent=4)

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI Stock Analyzer", layout="centered")

# ---------- UI ----------
st.title("📊 AI Stock Analyzer")

stocks_input = st.text_input(
    "📌 Enter Stock Symbols (comma separated)",
    placeholder="e.g. tesla, AAPL, TCS.NS"
)

receiver = st.text_input("📧 Enter your Email")

portfolio_input = st.text_input(
    "💼 Portfolio (optional)",
    placeholder="e.g. TCS.NS:10, AAPL:5"
)

alert_input = st.text_input(
    "🔔 Alert (optional)",
    placeholder="e.g. TSLA > 200"
)

st.info("💡 Examples:\n- tesla → TSLA\n- apple → AAPL\n- tcs → TCS.NS")

# ---------- NAME → TICKER ----------
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

# ---------- BUTTON ----------
if st.button("🚀 Analyze & Send Report"):

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

    if len(stocks) > 3:
        st.warning("⚠️ Max 3 stocks allowed")
        st.stop()

    results = []

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

    # ---------- SAVE USER ----------
    users = load_users()
    users[receiver] = {
        "stocks": stocks,
        "portfolio": portfolio_input,
        "alert": alert_input
    }
    save_users(users)

    # ---------- DISPLAY ----------
    st.subheader("📈 Results")

    for stock, res in results:
        st.markdown(f"### {stock}")
        st.write("Trend:", res["trend"])
        st.write("Change:", f"{res['change']}%")
        st.write("Sentiment:", res["sentiment"])

        if "recommendation" in res:
            st.write("Recommendation:", res["recommendation"])
            st.write("Confidence:", f"{res['confidence']}%")

        for h in res["headlines"]:
            st.write("•", h)

    # ---------- PORTFOLIO ----------
    if portfolio_input:
        st.subheader("💼 Portfolio")

        for item in portfolio_input.split(","):
            try:
                name, qty = item.split(":")
                st.write(f"{name.strip()} → {qty.strip()} shares")
            except:
                st.warning("Invalid portfolio format")

    # ---------- ALERT ----------
    if alert_input:
        st.info(f"🔔 Alert saved: {alert_input}")

    # ---------- EMAIL ----------
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
            <p>Sentiment: {res['sentiment']}</p>
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


       

       
