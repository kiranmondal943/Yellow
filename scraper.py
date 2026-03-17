import requests
from bs4 import BeautifulSoup
import pandas as pd
from config import BASE_URL, QUERY, PAGES_TO_SCRAPE, HEADERS
from utils import random_delay

data = []

def get_search_page(page):
    params = {
        "q": QUERY,
        "page": page
    }
    response = requests.get(BASE_URL, params=params, headers=HEADERS)
    return response.text


def parse_listing(html):
    soup = BeautifulSoup(html, "lxml")
    listings = soup.select(".company-card")  # may need adjustment

    links = []
    for listing in listings:
        a_tag = listing.find("a", href=True)
        if a_tag:
            links.append("https://www.yellowpages.uz" + a_tag["href"])
    
    return links


def parse_detail(url):
    try:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "lxml")

        name = soup.find("h1")
        email = soup.find("a", href=lambda x: x and "mailto" in x)
        address = soup.find("address")

        return {
            "Name": name.text.strip() if name else "",
            "Email": email.text.strip() if email else "",
            "Address": address.text.strip() if address else "",
            "URL": url
        }

    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    for page in range(1, PAGES_TO_SCRAPE + 1):
        print(f"Scraping page {page}")
        
        html = get_search_page(page)
        links = parse_listing(html)

        for link in links:
            print(f"Scraping: {link}")
            item = parse_detail(link)
            if item:
                data.append(item)

            random_delay()

    df = pd.DataFrame(data)
    df.to_csv("output/data.csv", index=False)
    print("✅ Data saved to output/data.csv")


if __name__ == "__main__":
    main()
