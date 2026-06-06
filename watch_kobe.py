from playwright.sync_api import sync_playwright

URL = "https://www.kobe-u.ac.jp/ja/news/events/"

try:
    with open("seen_kobe.txt", "r", encoding="utf-8") as f:
        seen = set(line.strip() for line in f if line.strip())
except FileNotFoundError:
    seen = set()

print("通知済み件数:", len(seen))

new_events = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(URL, wait_until="networkidle")

    html = page.content()

    browser.close()

from bs4 import BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

for a in soup.find_all("a", href=True):

    href = a["href"]
    text = a.get_text(" ", strip=True)

    if href.startswith("/"):
        href = "https://www.kobe-u.ac.jp" + href

    if "/news/events" not in href:
        continue

    if any(x in href for x in [
        "/category/",
        "/area/",
        "/place/",
        "/audience/",
        "/format/"
    ]):
        continue

    href = href.split("?")[0].rstrip("/")

    if href in seen:
        continue

    print("NEW:", text)
    print(href)

    new_events.append(href)

with open("seen_kobe.txt", "a", encoding="utf-8") as f:
    for href in new_events:
        f.write(href + "\n")

print("追加保存:", len(new_events))

if not new_events:
    print("新規イベントなし")
