import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.bayut.com/for-sale/property/dubai/?sort=date_desc"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}


def fetch_data(url=BASE_URL):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article", class_="fbc619bc _058bd30f")
    links = []

    for article in articles:
        try:
            href = article.find_all('a', class_='d40f2294')[1]['href']
            full_link = 'https://www.bayut.com/' + href
            links.append(full_link)
        except IndexError:
            pass

    return links

