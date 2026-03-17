from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

data = []

def setup_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


def scrape():
    driver = setup_driver()

    url = "https://www.yellowpages.uz/en/search/?q=dental"
    driver.get(url)

    time.sleep(5)

    listings = driver.find_elements(By.CSS_SELECTOR, "a[href*='/en/company/']")

    links = []
    for l in listings:
        href = l.get_attribute("href")
        if href and href not in links:
            links.append(href)

    print(f"Found {len(links)} links")

    for link in links[:20]:  # limit for safety
        driver.get(link)
        time.sleep(3)

        try:
            name = driver.find_element(By.TAG_NAME, "h1").text
        except:
            name = ""

        try:
            email_elem = driver.find_element(By.XPATH, "//a[contains(@href,'mailto')]")
            email = email_elem.text
        except:
            email = ""

        try:
            address = driver.find_element(By.TAG_NAME, "address").text
        except:
            address = ""

        data.append({
            "Name": name,
            "Email": email,
            "Address": address,
            "URL": link
        })

    driver.quit()

    df = pd.DataFrame(data)
    df.to_csv("output/data.csv", index=False)
    print("✅ Data saved")


if __name__ == "__main__":
    scrape()
