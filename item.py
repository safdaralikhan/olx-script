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

# Input CSV containing links
input_csv = "iphone6.csv"

# Output CSV to save extracted details
output_csv = "iphone6_details.csv"


def extract_details(url):
    try:
        # Open the product URL
        driver.get(url)

        # Simulate a random delay
        time.sleep(random.uniform(5, 10))

        # Wait for the main content to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "fd2e2d72"))
        )

        # Parse the page source
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract details using the class names provided
        main_div = soup.find("div", class_="fd2e2d72")
        if not main_div:
            print(f"Failed to find main content on page: {url}")
            return None

        # Extract name, price, location, and description safely
        name = main_div.find("h1", class_="_75bce902")
        price = main_div.find("span", class_="_24469da7")
        location = main_div.find("span", class_="_8206696c")
        description = main_div.find("div", class_="_472bfbef")

        # Check if any of the required elements are missing
        if not name or not price or not location or not description:
            print(f"Missing details for product: {url}")
            return None

        # Get text from the elements if they exist
        return {
            "Name": name.get_text(strip=True) if name else "N/A",
            "Price": price.get_text(strip=True) if price else "N/A",
            "Location": location.get_text(strip=True) if location else "N/A",
            "Description": description.get_text(strip=True) if description else "N/A"
        }

    except TimeoutException:
        print(f"Timeout: Failed to load the page {url}")
        return None
    except Exception as e:
        print(f"Error occurred for {url}: {str(e)}")
        return None
     

# Read links from the input CSV
with open(input_csv, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    links = [row[0] for row in reader if row]  # Skip empty rows

# Open the output CSV for writing
with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Name", "Price", "Location", "Description"])
    writer.writeheader()

    # Process each link
    for link in links:
        print(f"Processing link: {link}")
        details = extract_details(link)
        if details:
            writer.writerow(details)
            print(f"Details extracted: {details}")
        else:
            print(f"Failed to extract details for link: {link}")

# Close the driver
driver.quit()

print(f"All details saved to {output_csv}")
