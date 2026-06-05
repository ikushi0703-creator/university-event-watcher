import os
import requests
import smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText

# =========================
# Gmail送信
# =========================

def send_mail(subject, body):

    sender = os.environ["GMAIL_ADDRESS"]
    password = os.environ["GMAIL_APP_PASSWORD"]

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = sender

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)

# =========================
# 通知済みURL読み込み
# =========================

try:
    with open("seen_events.txt", "r", encoding="utf-8") as f:
        seen = set(line.strip() for line in f if line.strip())

except FileNotFoundError:
    seen = set()

print("通知済み件数:", len(seen))

# =========================
# 京大イベント取得
# =========================

url = "https://www.kyoto-u.ac.jp/ja/event"

html = requests.get(url, timeout=30).text

soup = BeautifulSoup(html, "html.parser")

new_events = []

for a in soup.find_all("a", href=True):

    text = a.get_text(" ", strip=True)

    if "講演" in text or "公開講座" in text:

        link = a["href"]

        if link.startswith("/"):
            link = "https://www.kyoto-u.ac.jp" + link

        if link not in seen:

            print("NEW:", text)
            print(link)

            new_events.append((text, link))

# =========================
# 通知済み保存
# =========================

with open("seen_events.txt", "a", encoding="utf-8") as f:

    for _, link in new_events:
        f.write(link + "\n")

print("追加保存:", len(new_events))

# =========================
# メール通知
# =========================

if new_events:

    body = ""

    for title, link in new_events:
        body += f"{title}\n{link}\n\n"

    send_mail(
        subject=f"【京大イベント新着】{len(new_events)}件",
        body=body
    )

    print("メール送信完了")

else:
    print("新規イベントなし")
