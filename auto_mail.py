import os
from supabase import create_client
import yfinance as yf
from stock_utils import calculate_change
from ai_engine import generate_ai_report
from mailer import send_email

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def run():
    users = supabase.table("users").select("*").execute().data

    if not users:
        print("No users found")
        return

    for user in users:
        email = user["email"]
        stock = user["stocks"]

        data = yf.download(stock, period="3mo")

        if data.empty:
            continue

        change = calculate_change(data)

        ai_report = generate_ai_report(stock, change)

        html = f"""
        <h2>📊 AI Stock Report</h2>
        <h3>{stock}</h3>
        <p>{ai_report.replace('\n','<br>')}</p>
        """

        send_email(email, "AI Stock Report", html)


if __name__ == "__main__":
    run()

