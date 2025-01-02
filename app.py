import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import csv

# Initialize undetected ChromeDriver
options = uc.ChromeOptions()
options.add_argument("--window-size=1920x1080")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = uc.Chrome(options=options)

# URL Template for OLX Search
url_template = "https://www.olx.com.pk/items/q-iphone-{model}?page={page}"

# List of iPhone models
iphone_models = [6, 7, 8, 9, 11, 12, 13, 14]
page_numbers = [1, 2, 3, 4, 5]

try:
    for model in iphone_models:
        # Set to store unique links
        unique_links = set()

        for page in page_numbers:
            url = url_template.format(model=model, page=page)
            print(f"Attempting to open URL: {url}")

            # Open the URL
            driver.get(url)

            # Simulate a random delay
            time.sleep(random.uniform(5, 15))

            # Wait for page to load
            try:
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'ul._1aad128c'))
                )
            except TimeoutException:
                print(f"Timeout: Element not found for URL: {url}")
                continue

            # Parse page source with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            listings = soup.select('ul._1aad128c li a[href]')

            # Add links to the set to ensure uniqueness
            for listing in listings:
                link = listing['href']
                if '/item/' in link:
                    full_link = f"https://www.olx.com.pk{link}"
                    unique_links.add(full_link)

        # Save all unique links for this model into a single CSV file
        csv_filename = f"iphone{model}.csv"
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Link"])  # Write header

            for link in unique_links:
                writer.writerow([link])
                print(f"Saved Link: {link}")

        print(f"All unique links for iPhone {model} saved to {csv_filename}")

finally:
    driver.quit()
