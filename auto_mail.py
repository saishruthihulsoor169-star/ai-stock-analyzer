import smtplib
from email.mime.text import MIMEText
import os
from supabase import create_client
from stock_utils import get_stock_data, analyze_stock

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, to_email, msg.as_string())

# FETCH USERS
users = supabase.table("users").select("*").execute().data

print("Users:", users)

for user in users:
    stock = user["stocks"]
    email = user["email"]

    data = get_stock_data(stock)

    if data is not None:
        result = analyze_stock(data)

        body = f"""
Stock: {stock}
Trend: {result['trend']}
Change: {result['change']}
Recommendation: {result['recommendation']}
"""

        send_email(email, f"{stock} Daily Report", body)
