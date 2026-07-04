from urllib.parse import urlparse

from bs4 import BeautifulSoup

from app.config import settings
from app.db.crud import save_document_page
from app.db.database import SessionLocal
from app.docs_parser.parser import get_html, parse_main_page


def is_bitrix_docs_url(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc == "apidocs.bitrix24.ru"


def parse_page(url):
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.text.strip() if soup.title else url

    for tag in soup(["script", "style", "nav", "footer"]):
        tag.extract()

    content = soup.get_text("\n", strip=True)

    return title, content


def crawl_main_links():
    main_page = parse_main_page()
    links = main_page["links"]

    db = SessionLocal()
    saved_count = 0

    try:
        for link in links:
            url = link["href"]

            if not is_bitrix_docs_url(url):
                continue

            try:
                title, content = parse_page(url)

                if len(content) < 100:
                    continue

                save_document_page(
                    db=db,
                    url=url,
                    title=title,
                    content=content
                )

                saved_count += 1
                print("Сохранено:", title)

            except Exception as error:
                print("Ошибка при обработке:", url, error)

    finally:
        db.close()

    print("Всего сохранено страниц:", saved_count)


if __name__ == "__main__":
    crawl_main_links()
