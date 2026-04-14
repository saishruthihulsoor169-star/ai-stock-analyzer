import streamlit as st
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from stock_utils import analyze_stock

st.title("📊 AI Stock Analyzer")

# Input
stock = st.text_input("Enter Stock Symbol (e.g. TCS.NS)")
receiver = st.text_input("Enter your Email")

if st.button("Analyze & Send Report"):
    if stock and receiver:

        data, trend, headlines = analyze_stock(stock)
        suggestion = "BUY 🟢" if "UP" in trend else "SELL 🔴"

        st.subheader("📈 Result")
        st.write("Trend:", trend)
        st.write("Suggestion:", suggestion)

        st.subheader("📰 News")
        for h in headlines:
            st.write("-", h)

        st.image("chart.png")

        # 🔐 Email credentials
        sender = os.getenv("EMAIL_USER")
        password = os.getenv("EMAIL_PASS")

        try:
            msg = MIMEMultipart()
            msg["Subject"] = "📊 Stock Report"
            msg["From"] = sender
            msg["To"] = receiver

            html = f"""
            <h2>📊 Stock Report</h2>
            <p><b>Stock:</b> {stock}</p>
            <p><b>Trend:</b> {trend}</p>
            <p><b>Suggestion:</b> {suggestion}</p>

            <h3>📰 News</h3>
            <ul>
            """

            for h in headlines:
                html += f"<li>{h}</li>"

            html += "</ul>"

            msg.attach(MIMEText(html, "html"))

            # attach chart
            with open("chart.png", "rb") as img:
                image = MIMEImage(img.read())
                image.add_header('Content-ID', '<chart>')
                msg.attach(image)

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
            server.quit()

            st.success("✅ Email sent successfully!")

        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")

    else:
        st.warning("Please enter stock and email")

       

       
