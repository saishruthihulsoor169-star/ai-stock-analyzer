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


def get_stock_data(stock):
    data = yf.download(stock, period="3mo")
    return data


def generate_chart(data, stock):
    plt.figure(figsize=(8, 4))
    plt.plot(data["Close"])
    plt.title(f"{stock} Price Chart")
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.grid()

    filename = f"{stock}.png"
    plt.savefig(filename)
    plt.close()

    return filename


def analyze(data):
    start = float(data["Close"].iloc[0])
    end = float(data["Close"].iloc[-1])

    change = ((end - start) / start) * 100

    if change > 0:
        trend = "UP 📈"
    else:
        trend = "DOWN 📉"

    sentiment_score = round(change / 10, 2)

    sentiment = "Positive 😊" if sentiment_score > 0 else "Negative 😐"

    return trend, round(change, 2), sentiment, sentiment_score


def build_email_content(stock, trend, change, sentiment, score):
    return f"""
    <h2>📊 AI Stock Analysis Report</h2>

    <h3>{stock}</h3>
    <p><b>Trend:</b> {trend}</p>
    <p><b>Change:</b> {change}%</p>
    <p><b>Sentiment:</b> {sentiment} ({score})</p>

    <ul>
        <li>Market reacting to earnings</li>
        <li>AI sector impact visible</li>
        <li>Investor sentiment slightly shifting</li>
    </ul>

    <hr>
    """


def send_email():
    msg = MIMEMultipart("related")
    msg["Subject"] = "📊 Daily AI Stock Report"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_USER   # You can fetch from DB later

    html_content = ""

    images = []

    for stock in stocks:
        data = get_stock_data(stock)

        trend, change, sentiment, score = analyze(data)

        chart_file = generate_chart(data, stock)

        html_content += build_email_content(stock, trend, change, sentiment, score)
        html_content += f'<img src="cid:{stock}"><br><br>'

        with open(chart_file, "rb") as f:
            img = MIMEImage(f.read())
            img.add_header("Content-ID", f"<{stock}>")
            images.append(img)

    msg.attach(MIMEText(html_content, "html"))

    for img in images:
        msg.attach(img)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)


if __name__ == "__main__":
    send_email()
