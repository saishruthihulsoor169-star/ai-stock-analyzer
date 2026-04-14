import streamlit as st
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from stock_utils import analyze_stock

# ⚙️ Page config
st.set_page_config(page_title="AI Stock Analyzer", layout="centered")

# 🎯 UI Header
st.markdown("<h1 style='text-align: center;'>📊 AI Stock Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Analyze any stock & get instant email reports</p>", unsafe_allow_html=True)

st.divider()

# 🧾 Inputs
stocks_input = st.text_input(
    "📌 Enter Stock Symbols (comma separated)",
    placeholder="e.g. TCS.NS, INFY.NS, AAPL"
)

receiver = st.text_input("📧 Enter your Email")

# 💡 Help text
st.info("💡 Use correct ticker format:\n- Indian stocks: TCS.NS\n- US stocks: AAPL\n- Crypto: BTC-USD")

# 🚀 Button
if st.button("🚀 Analyze & Send Report", use_container_width=True):

    if not stocks_input or not receiver:
        st.warning("⚠️ Please enter stock symbols and email")
        st.stop()

    stocks = [s.strip() for s in stocks_input.split(",")]

    # 🛑 Limit to avoid API rate limit
    if len(stocks) > 3:
        st.warning("⚠️ Max 3 stocks allowed (to avoid rate limit)")
        st.stop()

    results = []

    with st.spinner("🔍 Analyzing stocks..."):

        for stock in stocks:
            result = analyze_stock(stock)

            if result is None:
                st.error(f"❌ {stock} is invalid or no data found")
                continue

            if "error" in result:
                st.error(f"❌ Failed to fetch {stock} (Rate limit or invalid)")
                continue

            results.append((stock, result))

    if not results:
        st.error("❌ No valid stock data fetched")
        st.stop()

    # 📊 Display Results
    st.subheader("📈 Analysis Results")

   for stock, res in results:
    st.markdown(f"### {stock}")
    st.markdown(f"**📊 Trend:** {res['trend']}")
    st.markdown(f"**📈 Change:** {res['change']}%")
    st.markdown(f"**😊 Sentiment:** {res['sentiment']} ({res['sentiment_score']})")

    if "recommendation" in res:
        st.markdown(f"**💡 Recommendation:** {res['recommendation']}")
        st.markdown(f"**🎯 Confidence:** {res['confidence']}%")

    for h in res["headlines"]:
        st.write("•", h)

    # 📧 Email Sending
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    try:
        msg = MIMEMultipart()
        msg["Subject"] = "📊 Multi-Stock Analysis Report"
        msg["From"] = sender
        msg["To"] = receiver

        html = """
        <h2>📊 AI Stock Analysis Report</h2>
        <hr>
        """

        for stock, res in results:
            html += f"""
            <h3>{stock}</h3>
            <p><b>Trend:</b> {res['trend']}</p>
            <p><b>Change:</b> {res['change']}%</p>
            <p><b>Sentiment:</b> {res['sentiment']} ({res['sentiment_score']})</p>
            """

            # Step 2 support
            if "recommendation" in res:
                html += f"""
                <p><b>Recommendation:</b> {res['recommendation']}</p>
                <p><b>Confidence:</b> {res['confidence']}%</p>
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

        st.success("📧 Email sent successfully!")

    except Exception as e:
        st.error(f"❌ Email failed: {e}")


       

       
