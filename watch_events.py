import requests
from bs4 import BeautifulSoup

try:
    with open("seen_events.txt", "r", encoding="utf-8") as f:
        seen = set(line.strip() for line in f if line.strip())
except FileNotFoundError:
    seen = set()

print("通知済み件数:", len(seen))

url = "https://www.kyoto-u.ac.jp/ja/event"
html = requests.get(url, timeout=30).text
soup = BeautifulSoup(html, "html.parser")

new_links = []

for a in soup.find_all("a", href=True):

    text = a.get_text(" ", strip=True)

    if "講演" in text or "公開講座" in text:

        link = a["href"]

        if link.startswith("/"):
            link = "https://www.kyoto-u.ac.jp" + link

        if link not in seen:

            print("NEW:", text)
            print(link)

            new_links.append(link)

with open("seen_events.txt", "a", encoding="utf-8") as f:
    for link in new_links:
        f.write(link + "\n")

print("追加保存:", len(new_links))
