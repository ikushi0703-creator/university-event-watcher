import requests
from bs4 import BeautifulSoup

url = "https://www.osaka-u.ac.jp/ja/event"

html = requests.get(url, timeout=30).text

soup = BeautifulSoup(html, "html.parser")

for a in soup.find_all("a", href=True):
    text = a.get_text(" ", strip=True)

    if text:
        print(text)
