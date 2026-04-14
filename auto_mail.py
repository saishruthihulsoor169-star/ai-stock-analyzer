import smtplib
import json
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from stock_utils import analyze_stock

def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {}

def send_email(receiver, results):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    msg = MIMEMultipart()
    msg["Subject"] = "📊 Daily Stock Report"
    msg["From"] = sender
    msg["To"] = receiver

    html = "<h2>📊 Daily Stock Report</h2><hr>"

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

def main():
    users = load_users()

    if not users:
        print("No users found")
        return

    for email, data in users.items():
        stocks = data.get("stocks", [])

        results = []

        for stock in stocks:
            result = analyze_stock(stock)

            if result and "error" not in result:
                results.append((stock, result))

        if results:
            send_email(email, results)
            print(f"Email sent to {email}")

if __name__ == "__main__":
    main()
