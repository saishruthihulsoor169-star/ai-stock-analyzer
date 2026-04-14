import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from supabase import create_client
import os

from stock_utils import analyze_stock

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def load_users():
    response = supabase.table("users").select("*").execute()
    return response.data

def send_email(receiver, results):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    msg = MIMEMultipart()
    msg["Subject"] = "Daily Stock Report"
    msg["From"] = sender
    msg["To"] = receiver

    html = "<h2>Daily Report</h2>"

    for stock, res in results:
        html += f"<h3>{stock}</h3><p>{res['trend']}</p>"

    msg.attach(MIMEText(html, "html"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)
    server.quit()

def main():
    users = load_users()

    for user in users:
        email = user["email"]
        stocks = user["stocks"].split(",")

        results = []

        for stock in stocks:
            result = analyze_stock(stock)

            if result and "error" not in result:
                results.append((stock, result))

        if results:
            send_email(email, results)

if __name__ == "__main__":
    main()
