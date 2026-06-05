import requests
from bs4 import BeautifulSoup

# 通知済みURLを読む
try:
    with open("seen_events.txt", "r", encoding="utf-8") as f:
        seen = set(line.strip() for line in f if line.strip())
except FileNotFoundError:
    seen = set()

print("通知済み件数:", len(seen))

url = "https://www.kyoto-u.ac.jp/ja/event"
html = requests.get(url, timeout=30).text
soup = BeautifulSoup(html, "html.parser")

count = 0

for a in soup.find_all("a", href=True):

    text = a.get_text(" ", strip=True)

    if "講演" in text or "公開講座" in text:

        link = a["href"]

        if link.startswith("/"):
            link = "https://www.kyoto-u.ac.jp" + link

        if link not in seen:
            print("NEW:", text)
            print(link)
            count += 1

print("新規イベント数:", count)
