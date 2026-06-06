import requests
from bs4 import BeautifulSoup

URL = "https://www.kobe-u.ac.jp/ja/news/events/"

# =========================
# seen読み込み
# =========================
try:
    with open("seen_kobe.txt", "r", encoding="utf-8") as f:
        seen = set(line.strip() for line in f if line.strip())
except FileNotFoundError:
    seen = set()

print("通知済み件数:", len(seen))

html = requests.get(URL, timeout=30).text
soup = BeautifulSoup(html, "html.parser")

new_events = []

# =========================
# イベントリンクだけ抽出
# =========================
for a in soup.find_all("a", href=True):

    text = a.get_text(" ", strip=True)
    href = a["href"]

    # ★神大はここが重要（ノイズ除去）
    if "/news/events" not in href:
        continue

    if href.startswith("/"):
        href = "https://www.kobe-u.ac.jp" + href

    href = href.split("?")[0].rstrip("/")

    # 重複防止
    if href in seen:
        continue

    print("NEW:", text)
    print(href)

    new_events.append(href)

# =========================
# 保存
# =========================
with open("seen_kobe.txt", "a", encoding="utf-8") as f:
    for href in new_events:
        f.write(href + "\n")

print("追加保存:", len(new_events))

if not new_events:
    print("新規イベントなし")
