import requests
from bs4 import BeautifulSoup

# =========================
# 設定
# =========================

url = "https://www.osaka-u.ac.jp/ja/event"

# 阪大は幅広く拾う
keywords = [
    "講演",
    "講演会",
    "公開講座",
    "講習会",
    "セミナー",
    "シンポジウム",
    "フォーラム",
    "イベント"
]

# =========================
# 通知済み読み込み
# =========================

try:
    with open("seen_osaka.txt", "r", encoding="utf-8") as f:
        seen = set(line.strip() for line in f if line.strip())
except FileNotFoundError:
    seen = set()

print("通知済み件数:", len(seen))

# =========================
# HTML取得
# =========================

html = requests.get(url, timeout=30).text
soup = BeautifulSoup(html, "html.parser")

# =========================
# 抽出
# =========================

new_events = []

for a in soup.find_all("a", href=True):

    text = a.get_text(" ", strip=True)
    link = a["href"]

    # ★デバッグ（重要：何が取れてるか確認）
    if len(text) > 10:
        print("RAW:", text)

    # URL整形
    if link.startswith("/"):
        link = "https://www.osaka-u.ac.jp" + link

    # キーワード判定
    if any(k in text for k in keywords):

        if link not in seen:

            print("NEW:", text)
            print(link)

            new_events.append((text, link))

# =========================
# 保存
# =========================

with open("seen_osaka.txt", "a", encoding="utf-8") as f:
    for _, link in new_events:
        f.write(link + "\n")

print("追加保存:", len(new_events))

# =========================
# 結果
# =========================

if not new_events:
    print("新規イベントなし")
