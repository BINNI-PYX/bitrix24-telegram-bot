from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from app.config import settings


def get_html(url):
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    response.encoding = "utf-8"
    return response.text


def parse_main_page():
    url = settings.BITRIX24_DOCS_URL
    html = get_html(url)

    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.text.strip() if soup.title else "Bitrix24 API"

    links = []
    for link in soup.find_all("a"):
        text = link.get_text(" ", strip=True)
        href = link.get("href")

        if text and href:
            links.append({
                "text": text,
                "href": urljoin(url, href)
            })

    return {
        "title": title,
        "links_count": len(links),
        "links": links[:20]
    }


if __name__ == "__main__":
    result = parse_main_page()

    print("Заголовок:", result["title"])
    print("Количество ссылок:", result["links_count"])

    print("\nПервые ссылки:")
    for item in result["links"]:
        print("-", item["text"], "=>", item["href"])
