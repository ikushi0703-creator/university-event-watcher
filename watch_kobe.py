import requests
from bs4 import BeautifulSoup

URL = "https://www.kobe-u.ac.jp/ja/news/events/"

try:
    with open("seen_kobe.txt", "r", encoding="utf-8") as f:
        seen = set(line.strip() for line in f if line.strip())
except FileNotFoundError:
    seen = set()

print("通知済み件数:", len(seen))

html = requests.get(URL, timeout=30).text
soup = BeautifulSoup(html, "html.parser")

new_events = []

for a in soup.find_all("a", href=True):

    text = a.get_text(" ", strip=True)
    href = a["href"]

    if href.startswith("/"):
        href = "https://www.kobe-u.ac.jp" + href

    href = href.split("?")[0].rstrip("/")

    # ■ ノイズ除去（ここが重要）
    if "/news/events/category/" in href:
        continue
    if "/news/events/area/" in href:
        continue
    if "/news/events/place/" in href:
        continue
    if "/news/events/audience/" in href:
        continue
    if "/news/events/format/" in href:
        continue

    # イベント以外除外
    if "/news/events" not in href:
        continue

    # 重複防止
    if href in seen:
        continue

    print("NEW:", text)
    print(href)

    new_events.append(href)

with open("seen_kobe.txt", "a", encoding="utf-8") as f:
    for href in new_events:
        f.write(href + "\n")

print("追加保存:", len(new_events))
