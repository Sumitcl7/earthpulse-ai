import requests
from bs4 import BeautifulSoup
import json

url = "https://www.bbc.com/news/science_and_environment"
res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")

headlines = []

for a in soup.find_all("a", href=True):
    if "/news/" in a["href"] and a.text.strip():
        headlines.append(a.text.strip())

# Save to JSON
with open("headlines.json", "w", encoding="utf-8") as f:
    json.dump(headlines, f, ensure_ascii=False, indent=4)

print(f"Saved {len(headlines)} headlines to headlines.json")
