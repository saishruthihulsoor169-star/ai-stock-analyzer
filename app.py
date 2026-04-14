import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from supabase import create_client

from stock_utils import analyze_stock

# ---------- SUPABASE ----------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------- UI ----------
st.set_page_config(page_title="AI Stock Analyzer")

st.title("📊 AI Stock Analyzer")

stocks_input = st.text_input("📌 Enter Stock Symbols (comma separated)", placeholder="e.g. tesla, AAPL")
receiver = st.text_input("📧 Enter your Email")
portfolio_input = st.text_input("💼 Portfolio (optional)", placeholder="e.g. TSLA:2")
alert_input = st.text_input("🔔 Alert (optional)", placeholder="e.g. TSLA > 200")

# Name mapping
name_to_ticker = {
    "tesla": "TSLA",
    "apple": "AAPL",
    "tcs": "TCS.NS",
    "infosys": "INFY.NS"
}

if st.button("🚀 Analyze & Send Report"):

    if not stocks_input or not receiver:
        st.warning("Enter stock and email")
        st.stop()

    stocks = []
    for s in stocks_input.split(","):
        s = s.strip().lower()
        stocks.append(name_to_ticker.get(s, s.upper()))

    results = []

    for stock in stocks:
        result = analyze_stock(stock)

        if result and "error" not in result:
            results.append((stock, result))
        else:
            st.error(f"Failed: {stock}")

    if not results:
        st.stop()

    # ---------- SAVE TO DATABASE ----------
    try:
        supabase.table("users").upsert({
            "email": receiver,
            "stocks": ",".join(stocks),
            "portfolio": portfolio_input,
            "alert": alert_input
        }).execute()

        st.success("✅ Saved to database")

    except Exception as e:
        st.error(f"DB Error: {e}")

    # ---------- DISPLAY ----------
    for stock, res in results:
        st.subheader(stock)
        st.write("Trend:", res["trend"])
        st.write("Change:", res["change"])
        st.write("Sentiment:", res["sentiment"])

        if "recommendation" in res:
            st.write("Recommendation:", res["recommendation"])
            st.write("Confidence:", res["confidence"])

    # ---------- EMAIL ----------
    sender = st.secrets["EMAIL_USER"]
    password = st.secrets["EMAIL_PASS"]

    try:
        msg = MIMEMultipart()
        msg["Subject"] = "Stock Report"
        msg["From"] = sender
        msg["To"] = receiver

        html = "<h2>Stock Report</h2>"

        for stock, res in results:
            html += f"<h3>{stock}</h3><p>{res['trend']}</p>"

        msg.attach(MIMEText(html, "html"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()

        st.success("📧 Email sent")

    except Exception as e:
        st.error(f"Email error: {e}")


       

       
