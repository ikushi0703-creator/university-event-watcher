import requests
from bs4 import BeautifulSoup

url = "https://www.kyoto-u.ac.jp/ja/event"

html = requests.get(url, timeout=30).text

soup = BeautifulSoup(html, "html.parser")

for a in soup.find_all("a", href=True):

    text = a.get_text(" ", strip=True)

    if "講演" in text or "公開講座" in text:
        print("TITLE:", text)
        print("URL:", a["href"])
        print("-" * 50)
