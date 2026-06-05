import requests
from bs4 import BeautifulSoup

url = "https://www.osaka-u.ac.jp/ja/event"

html = requests.get(url, timeout=30).text

print(html[:3000])
