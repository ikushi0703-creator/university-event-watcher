from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

URL = "https://www.osaka-u.ac.jp/ja/event/2026/05"

# =========================
# seen読み込み
# =========================
try:
    with open("seen_osaka.txt", "r", encoding="utf-8") as f:
        seen = set(line.strip() for line in f if line.strip())
except FileNotFoundError:
    seen = set()

print("通知済み件数:", len(seen))

new_events = []

# =========================
# ページ取得（JS実行）
# =========================
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(URL, wait_until="networkidle")

    html = page.content()

    browser.close()

# =========================
# HTML解析
# =========================
soup = BeautifulSoup(html, "html.parser")

for a in soup.find_all("a", href=True):

    text = a.get_text(" ", strip=True)
    href = a["href"]

    # =========================
    # URL正規化
    # =========================
    if href.startswith("/"):
        href = "https://www.osaka-u.ac.jp" + href

    href = href.split("?")[0].rstrip("/")

    # =========================
    # ノイズ除去
    # =========================
    if "/contents" in href:
        continue

    if "/ja/event/" not in href:
        continue

    # =========================
    # 重複排除（永続）
    # =========================
    if href in seen:
        continue

    # =========================
    # 重複排除（今回実行内）
    # =========================
    if any(h == href for _, h in new_events):
        continue

    print("NEW:", text)
    print(href)

    new_events.append((text, href))

# =========================
# 保存
# =========================
with open("seen_osaka.txt", "a", encoding="utf-8") as f:
    for _, href in new_events:
        f.write(href + "\n")

print("追加保存:", len(new_events))

if not new_events:
    print("新規イベントなし")
