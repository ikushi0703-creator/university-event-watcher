import requests

html = requests.get(
    "https://www.osaka-u.ac.jp/ja/event",
    timeout=30
).text

for line in html.splitlines():
    if "api" in line.lower() or "json" in line.lower():
        print(line)
