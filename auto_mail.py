import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from stock_utils import analyze_stock

# 🔐 Email credentials (from GitHub Secrets)
sender = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASS")

# 📊 Stocks you want to track daily
stocks = ["TCS.NS", "INFY.NS"]

# 📂 Check if emails file exists
if not os.path.exists("emails.txt"):
    print("No emails.txt file found ❌")
    exit()

# 📥 Read emails
with open("emails.txt", "r") as f:
    emails = f.readlines()

# 🚀 Loop through each user
for receiver in emails:
    receiver = receiver.strip()

    if not receiver:
        continue

    try:
        data, trend, headlines = analyze_stock(stocks[0])

        suggestion = "BUY 🟢" if "UP" in trend else "SELL 🔴"

        # ✉️ Create email
        msg = MIMEMultipart()
        msg["Subject"] = "📊 Daily Stock Report"
        msg["From"] = sender
        msg["To"] = receiver

        html = f"""
        <h2>📊 Daily Stock Report</h2>
        <p><b>Stock:</b> {stocks[0]}</p>
        <p><b>Trend:</b> {trend}</p>
        <p><b>Suggestion:</b> {suggestion}</p>

        <h3>📈 Price Chart</h3>
        <img src="cid:chart" width="600">

        <h3>📰 News</h3>
        <ul>
        """

        for h in headlines:
            html += f"<li>{h}</li>"

        html += "</ul>"

        msg.attach(MIMEText(html, "html"))

        # 📈 Attach chart image
        try:
            with open("chart.png", "rb") as img_file:
                img = MIMEImage(img_file.read())
                img.add_header('Content-ID', '<chart>')
                msg.attach(img)
        except:
            print("Chart not found, skipping image")

        # 📤 Send email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()

        print(f"Email sent to {receiver} ✅")

    except Exception as e:
        print(f"Failed for {receiver}: {e}")