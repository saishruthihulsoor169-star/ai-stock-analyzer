import streamlit as st
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from stock_utils import analyze_stock

st.set_page_config(page_title="AI Stock Analyzer", layout="centered")

st.title("📊 AI Stock Analyzer")

stocks_input = st.text_input("Enter Stock Symbols (comma separated)", "TCS.NS, INFY.NS")
receiver = st.text_input("Enter your Email")

if st.button("Analyze & Send Report"):

    if stocks_input and receiver:

        stocks = [s.strip() for s in stocks_input.split(",")]

        results = []

        for stock in stocks:
            result = analyze_stock(stock)
            results.append((stock, result))

        st.subheader("📈 Results")

        for stock, res in results:
            st.markdown(f"### {stock}")
            st.write("Trend:", res["trend"])
            st.write("Change:", f'{res["change"]}%')
            st.write("Sentiment:", res["sentiment"], f'({res["sentiment_score"]})')

            for h in res["headlines"]:
                st.write("-", h)

        # 📧 Email
        sender = os.getenv("EMAIL_USER")
        password = os.getenv("EMAIL_PASS")

        try:
            msg = MIMEMultipart()
            msg["Subject"] = "📊 Multi-Stock Report"
            msg["From"] = sender
            msg["To"] = receiver

            html = "<h2>📊 Stock Report</h2>"

            for stock, res in results:
                html += f"""
                <h3>{stock}</h3>
                <p>Trend: {res['trend']}</p>
                <p>Change: {res['change']}%</p>
                <p>Sentiment: {res['sentiment']} ({res['sentiment_score']})</p>
                <ul>
                """

                for h in res["headlines"]:
                    html += f"<li>{h}</li>"

                html += "</ul>"

            msg.attach(MIMEText(html, "html"))

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
            server.quit()

            st.success("📧 Email sent successfully!")

        except Exception as e:
            st.error(f"Error sending email: {e}")

    else:
        st.warning("Enter stock(s) and email")

       

       
