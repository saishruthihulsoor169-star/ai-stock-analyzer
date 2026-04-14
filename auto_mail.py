import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from supabase import create_client
import os

from stock_utils import analyze_stock


# -------------------- SUPABASE SETUP --------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# -------------------- LOAD USERS --------------------
def load_users():
    try:
        response = supabase.table("users").select("*").execute()
        print("Users fetched:", response.data)
        return response.data
    except Exception as e:
        print("Error loading users:", e)
        return []


# -------------------- SEND EMAIL --------------------
def send_email(receiver, results):
    try:
        sender = os.getenv("EMAIL_USER")
        password = os.getenv("EMAIL_PASS")

        msg = MIMEMultipart()
        msg["Subject"] = "Daily Stock Report"
        msg["From"] = sender
        msg["To"] = receiver

        # Create HTML content
        html = "<h2>📊 Daily Stock Report</h2>"

        for stock, res in results:
            html += f"<h3>{stock}</h3><p>Trend: {res.get('trend', 'N/A')}</p>"

        msg.attach(MIMEText(html, "html"))

        # SMTP setup
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)

        server.send_message(msg)
        server.quit()

        print(f"✅ Email sent to {receiver}")

    except Exception as e:
        print(f"❌ Error sending email to {receiver}: {e}")


# -------------------- MAIN FUNCTION --------------------
def main():
    print("🚀 Script started")

    users = load_users()

    if not users:
        print("❌ No users found. Exiting...")
        return

    for user in users:
        try:
            email = user.get("email")
            stocks = user.get("stocks", "").split(",")

            print(f"Processing user: {email}, Stocks: {stocks}")

            results = []

            for stock in stocks:
                stock = stock.strip()

                result = analyze_stock(stock)

                if result and "error" not in result:
                    results.append((stock, result))
                else:
                    print(f"⚠️ Skipping {stock}, error in result")

            if results:
                send_email(email, results)
            else:
                print(f"⚠️ No valid results for {email}")

        except Exception as e:
            print(f"❌ Error processing user: {e}")


# -------------------- ENTRY POINT --------------------
if __name__ == "__main__":
    main()
