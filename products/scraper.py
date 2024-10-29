# products/scraper.py
import requests
from bs4 import BeautifulSoup
from .models import Product, Brand
import random
import time
from fake_useragent import UserAgent

def is_captcha_page(soup):
    """Check if the page contains a CAPTCHA by looking for specific text."""
    return "Enter the characters you see below" in soup.text

def scrape_brand_products(brand):
    """Scrape products for a specific brand from Amazon."""
    print("Starting to scrape for brand:", brand.name)
    amazon_url = f"https://www.amazon.com/s?k={brand.name}"
    print("amazon url:",amazon_url)
    user_agent = UserAgent()
    headers = {
        "User-Agent": user_agent.random  # Rotates User-Agent for each request
    }

    try:
        response = requests.get(amazon_url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        # Check for CAPTCHA
        if is_captcha_page(soup):
            print(f"CAPTCHA encountered for {brand.name}. Skipping scraping for now.")
            return False

        # Parse products
        product_elements = soup.select("div.s-result-item[data-asin]")  # Adjust selector based on HTML structure
        for element in product_elements:
            asin = element.get("data-asin")
            name = element.select_one("h2 .a-size-medium").text if element.select_one("h2 .a-size-medium") else "No name found"
            image = element.select_one(".s-image").get("src") if element.select_one(".s-image") else ""
            
            # Debug: Print each product's details
            print(f"Scraped product - Name: {name}, ASIN: {asin}, Image: {image}")

            # Save to the database
            Product.objects.update_or_create(
                asin=asin,
                defaults={
                    'name': name,
                    'sku': "",  # Placeholder as SKU may not be on search page
                    'image': image,
                    'brand': brand,
                }
            )
            # Delay between requests to avoid detection
            time.sleep(random.uniform(1, 3))

    except Exception as e:
        print(f"Error scraping {brand.name}: {e}")
        return False

    print(f"Completed scraping for brand: {brand.name}")
    return True
