import smtplib
from email.mime.text import MIMEText
import os


def send_email(to_email, subject, content):

    sender = os.getenv("EMAIL_ID")
    password = os.getenv("EMAIL_PASS")

    msg = MIMEText(content)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)

        server.sendmail(sender, to_email, msg.as_string())
        server.quit()

        print("Email sent successfully")

    except Exception as e:
        print("Email failed:", e)

