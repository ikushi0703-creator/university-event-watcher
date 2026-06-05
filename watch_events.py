import requests

url = "https://www.kyoto-u.ac.jp/ja/event"

r = requests.get(url, timeout=30)

print("status:", r.status_code)
print(r.text[:3000])
