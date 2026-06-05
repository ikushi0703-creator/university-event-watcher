import requests
from bs4 import BeautifulSoup

# 通知済みURLを読む
try:
    with open("seen_osaka.txt", "r", encoding="utf-8") as f:
        seen = set(line.strip() for line in f if line.strip())
except FileNotFoundError:
    seen = set()

print("通知済み件数:", len(seen))

url = "https://www.osaka-u.ac.jp/ja/event"

html = requests.get(url, timeout=30).text

soup = BeautifulSoup(html, "html.parser")

new_links = []

keywords = [
    "講演",
    "講演会",
    "公開講座",
    "講習会",
    "セミナー",
    "シンポジウム",
    "フォーラム"
]

for a in soup.find_all("a", href=True):

    text = a.get_text(" ", strip=True)

    if any(keyword in text for keyword in keywords):

        link = a["href"]

        if link.startswith("/"):
            link = "https://www.osaka-u.ac.jp" + link

        if link not in seen:

            print("NEW:", text)
            print(link)

            new_links.append(link)

with open("seen_osaka.txt", "a", encoding="utf-8") as f:
    for link in new_links:
        f.write(link + "\n")

print("追加保存:", len(new_links))

if not new_links:
    print("新規イベントなし")
