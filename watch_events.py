import requests
from bs4 import BeautifulSoup

url = "https://www.kobe-u.ac.jp/ja/news/events/"

r = requests.get(url, timeout=30)

print("encoding =", r.encoding)
print("apparent =", r.apparent_encoding)

r.encoding = r.apparent_encoding

html = r.text

soup = BeautifulSoup(html, "html.parser")

for a in soup.find_all("a", href=True):
    text = a.get_text(" ", strip=True)

    if text:
        print(text[:200])
