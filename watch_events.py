import os
import smtplib
from email.message import EmailMessage

gmail = os.environ["GMAIL_ADDRESS"]
password = os.environ["GMAIL_APP_PASSWORD"]

msg = EmailMessage()
msg["Subject"] = "大学イベント監視システム テスト"
msg["From"] = gmail
msg["To"] = gmail

msg.set_content(
    "GitHub Actions からのテストメールです。"
)

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(gmail, password)
    smtp.send_message(msg)

print("mail sent")
