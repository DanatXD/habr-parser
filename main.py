import requests
from bs4 import BeautifulSoup

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

BASE_URL = "https://habr.com"
LIST_URL = "https://habr.com/ru/all/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

response = requests.get(LIST_URL, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "lxml")
articles = soup.find_all("article")

for article in articles:
    title_tag = article.find("h2")
    if title_tag is None:
        continue
    title = title_tag.text.strip()

    link_tag = title_tag.find("a")
    if link_tag is None:
        continue
    link = BASE_URL + link_tag.get("href")

    time_tag = article.find("time")
    if time_tag is None:
        continue
    date = time_tag.get("datetime")

    preview = ""
    for lead in article.find_all("div", class_="tm-article-snippet__lead"):
        preview += " " + lead.text
    for lead in article.find_all("div", class_="article-formatted-body"):
        preview += " " + lead.text
    if not preview.strip():
        paragraphs = article.find_all("p")
        preview = " ".join(p.text for p in paragraphs)

    hubs = article.find_all("a", class_="tm-publication-hub__link")
    hub_text = " ".join(h.text for h in hubs)

    full_text = (title + " " + preview + " " + hub_text).lower()

    for keyword in KEYWORDS:
        if keyword.lower() in full_text:
            print(f"{date} – {title} – {link}")
            break