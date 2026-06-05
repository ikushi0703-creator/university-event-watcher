import requests
from bs4 import BeautifulSoup

url = "https://www.osaka-u.ac.jp/ja/event"

html = requests.get(url, timeout=30).text

soup = BeautifulSoup(html, "html.parser")

text = soup.get_text(" ", strip=True)

print(text[:10000])
