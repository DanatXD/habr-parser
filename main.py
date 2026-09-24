import time
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

    try:
        article_response = requests.get(link, headers=headers, timeout=10)
        article_response.raise_for_status()
    except requests.RequestException:
        continue

    article_soup = BeautifulSoup(article_response.text, "lxml")
    body = article_soup.find("div", class_="article-formatted-body")
    if body is None:
        body = article_soup.find("div", id="post-content-body")
    if body is None:
        continue

    text = body.text.lower()

    for keyword in KEYWORDS:
        if keyword.lower() in text:
            print(f"{date} – {title} – {link}")
            break

    time.sleep(0.5)