import yfinance as yf
import matplotlib.pyplot as plt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

stocks = ["TCS.NS", "INFY.NS"]


def analyze(data):
    close = data["Close"]
    start = float(close.iloc[0])
    end = float(close.iloc[-1])

    change = ((end - start) / start) * 100
    trend = "UP 📈" if change > 0 else "DOWN 📉"

    score = round(change / 10, 2)
    sentiment = "Positive 😊" if score > 0 else "Negative 😐"
    recommendation = "BUY" if score > 0 else "SELL"
    confidence = min(abs(score) * 10, 95)

    return trend, round(change, 2), sentiment, score, recommendation, confidence


def generate_chart(data, stock):
    plt.figure(figsize=(6, 3))
    plt.plot(data["Close"])
    plt.title(stock)
    file = f"{stock}.png"
    plt.savefig(file)
    plt.close()
    return file


def send_email():
    msg = MIMEMultipart("related")
    msg["Subject"] = "📊 AI Stock Report"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_USER

    html = "<h2>📊 AI Stock Analysis Report</h2>"

    images = []

    for stock in stocks:
        data = yf.download(stock, period="3mo")
        trend, change, sentiment, score, rec, conf = analyze(data)

        chart = generate_chart(data, stock)

        html += f"""
        <h3>{stock}</h3>
        <p><b>Trend:</b> {trend}</p>
        <p><b>Change:</b> {change}%</p>
        <p><b>Sentiment:</b> {sentiment} ({score})</p>
        <p><b>Recommendation:</b> {rec}</p>
        <p><b>Confidence:</b> {conf}%</p>
        <img src="cid:{stock}">
        <hr>
        """

        with open(chart, "rb") as f:
            img = MIMEImage(f.read())
            img.add_header("Content-ID", f"<{stock}>")
            images.append(img)

    msg.attach(MIMEText(html, "html"))

    for img in images:
        msg.attach(img)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)


if __name__ == "__main__":
    send_email()
