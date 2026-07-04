from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup


def get_page_with_selenium(url):
    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        html = driver.page_source
    finally:
        driver.quit()

    return html


def parse_page_with_selenium(url):
    html = get_page_with_selenium(url)
    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.text.strip() if soup.title else url

    for tag in soup(["script", "style", "nav", "footer"]):
        tag.extract()

    content = soup.get_text("\n", strip=True)
    return title, content


if __name__ == "__main__":
    url = "https://apidocs.bitrix24.ru/limits.html"
    title, content = parse_page_with_selenium(url)

    print("Заголовок:", title)
    print("Текст:", content[:1000])
