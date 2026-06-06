import requests
from bs4 import BeautifulSoup

BASE = "https://www.kobe-u.ac.jp"

START_URLS = [
    "https://www.kobe-u.ac.jp/ja/news/events/category/talk",
    "https://www.kobe-u.ac.jp/ja/news/events/category/open_lecture",
    "https://www.kobe-u.ac.jp/ja/news/events/category/briefing",
    "https://www.kobe-u.ac.jp/ja/news/events/category/exhibition",
    "https://www.kobe-u.ac.jp/ja/news/events/category/activities",
]

# seen読み込み
try:
    with open("seen_kobe.txt", "r", encoding="utf-8") as f:
        seen = set(line.strip() for line in f if line.strip())
except FileNotFoundError:
    seen = set()

print("通知済み件数:", len(seen))

new_events = []

for url in START_URLS:

    html = requests.get(url, timeout=30).text
    soup = BeautifulSoup(html, "html.parser")

    for a in soup.find_all("a", href=True):

        href = a["href"]
        text = a.get_text(" ", strip=True)

        if href.startswith("/"):
            href = BASE + href

        if "/news/events/" not in href:
            continue

        # カテゴリ・ナビ除外
        if any(x in href for x in ["/category/", "/area/", "/place/", "/audience/", "/format/"]):
            continue

        href = href.split("?")[0].rstrip("/")

        if href in seen:
            continue

        print("NEW:", text)
        print(href)

        new_events.append(href)

# 保存
with open("seen_kobe.txt", "a", encoding="utf-8") as f:
    for href in new_events:
        f.write(href + "\n")

print("追加保存:", len(new_events))

if not new_events:
    print("新規イベントなし")
