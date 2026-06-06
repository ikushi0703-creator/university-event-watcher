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

# ★重要：イベント“詳細ページ”っぽいURLだけに絞る
for a in soup.find_all("a", href=True):

    text = a.get_text(" ", strip=True)
    href = a["href"]

    if href.startswith("/"):
        href = "https://www.kobe-u.ac.jp" + href

    href = href.split("?")[0].rstrip("/")

    # ■ ここが核心（詳細ページだけ残す）
    if "/news/events/" not in href:
        continue

    if any(x in href for x in [
        "/category/",
        "/area/",
        "/place/",
        "/audience/",
        "/format/"
    ]):
        continue

    # トップページ除外
    if href.rstrip("/") == "https://www.kobe-u.ac.jp/ja/news/events":
        continue

    if href in seen:
        continue

    print("NEW:", text)
    print(href)

    new_events.append(href)

with open("seen_kobe.txt", "a", encoding="utf-8") as f:
    for href in new_events:
        f.write(href + "\n")

print("追加保存:", len(new_events))
