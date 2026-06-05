import requests
from bs4 import BeautifulSoup

url = "https://www.osaka-u.ac.jp/ja/event/2026/05"

try:
    with open("seen_osaka.txt", "r", encoding="utf-8") as f:
        seen = set(line.strip() for line in f if line.strip())
except FileNotFoundError:
    seen = set()

print("通知済み件数:", len(seen))

html = requests.get(url, timeout=30).text
soup = BeautifulSoup(html, "html.parser")

new_events = []

# ★重要：ページ内すべてのリンクをまず取得
links = soup.select("a[href]")

for a in links:

    href = a.get("href", "")
    text = a.get_text(" ", strip=True)

    # デバッグ（重要）
    if "講" in text or "セミ" in text or len(text) > 15:
        print("DEBUG:", text, href)

    # 阪大イベントページの特徴フィルタ
    if "/ja/event/2026/05/" in href:

        if href.startswith("/"):
            href = "https://www.osaka-u.ac.jp" + href

        if href not in seen:

            print("NEW:", text)
            print(href)

            new_events.append((text, href))

with open("seen_osaka.txt", "a", encoding="utf-8") as f:
    for _, href in new_events:
        f.write(href + "\n")

print("追加保存:", len(new_events))

if not new_events:
    print("新規イベントなし")
