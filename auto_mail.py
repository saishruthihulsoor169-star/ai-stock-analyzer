import os
from supabase import create_client
from stock_utils import get_stock_data
import smtplib
from email.mime.text import MIMEText

# ENV
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# DEBUG
print("URL:", SUPABASE_URL)
print("KEY exists:", SUPABASE_KEY is not None)

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("❌ Supabase credentials missing")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def send_email(to_email, content):
    msg = MIMEText(content)
    msg["Subject"] = "📊 Daily Stock Report"
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)
    server.send_message(msg)
    server.quit()


def run():
    response = supabase.table("users").select("*").execute()

    users = response.data
    print("Users:", users)

    if not users:
        print("⚠️ No users found in DB")
        return

    for user in users:
        email = user.get("email")
        stocks = user.get("stocks", "")

        if not stocks:
            continue

        stock_list = stocks.split(",")

        report = ""

        for s in stock_list:
            result = get_stock_data(s.strip())

            if result:
                report += f"""
{s.upper()}
Price: {result['price']}
Change: {result['change']}%
Trend: {result['trend']}
-----------------------
"""

        if report:
            print(f"Sending email to {email}")
            send_email(email, report)


if __name__ == "__main__":
    run()
