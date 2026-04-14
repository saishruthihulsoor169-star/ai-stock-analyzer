import os
from supabase import create_client
from stock_utils import get_stock_data
import smtplib
from email.mime.text import MIMEText

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def send_email(to_email, content):
    msg = MIMEText(content)
    msg["Subject"] = "Daily Stock Report"
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)
    server.send_message(msg)
    server.quit()

def run():
    users = supabase.table("users").select("*").execute().data

    for user in users:
        stocks = user["stocks"].split(",")

        report = ""

        for s in stocks:
            result = get_stock_data(s.strip())
            if result:
                report += f"{s}\nPrice: {result['price']}\nChange: {result['change']}%\nTrend: {result['trend']}\n\n"

        if report:
            send_email(user["email"], report)

if __name__ == "__main__":
    run()
