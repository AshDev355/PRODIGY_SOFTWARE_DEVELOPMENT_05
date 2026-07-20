import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from urllib.parse import urljoin, urlparse

def get_soup(url, headers):
    """Fetch a URL and return BeautifulSoup object."""
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, 'html.parser')
    except Exception as e:
        print(f" Error fetching {url}: {e}")
        return None

def extract_text(el, selector):
    """Extract text from an element using a CSS selector, return '' if not found."""
    if not el:
        return ''
    found = el.select_one(selector)
    return found.get_text(strip=True) if found else ''

def scrape_products(start_url, product_selector, name_sel, price_sel, rating_sel, next_sel, max_pages=None):
    """
    Scrape product data from a paginated listing.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    products = []
    page = 1
    url = start_url

    while True:
        if max_pages and page > max_pages:
            print(f" Reached max pages ({max_pages})")
            break

        print(f" Scraping page {page}: {url}")
        soup = get_soup(url, headers)
        if not soup:
            break

        # Find all product containers
        containers = soup.select(product_selector)
        if not containers:
            print(" No product containers found. Check your selector.")
            break

        for container in containers:
            name = extract_text(container, name_sel)
            price = extract_text(container, price_sel)
            rating = extract_text(container, rating_sel) if rating_sel else ''
            if name or price:  # at least one field
                products.append({
                    'Name': name,
                    'Price': price,
                    'Rating': rating
                })

        # Find next page link
        if next_sel:
            next_el = soup.select_one(next_sel)
            if next_el and next_el.get('href'):
                next_url = urljoin(url, next_el['href'])
                # Avoid infinite loop if next URL is same
                if next_url == url:
                    print(" Next page URL is same as current – stopping.")
                    break
                url = next_url
                page += 1
                time.sleep(random.uniform(1, 3))  # polite delay
            else:
                print(" No more pages.")
                break
        else:
            print(" No next-page selector provided – single page only.")
            break

    return products

def save_csv(data, filename):
    if not data:
        print(" No data to save.")
        return
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f" Saved {len(data)} items to {filename}")

def main():
    print("🕷️  Web Scraper – interactive setup")
    print("Provide CSS selectors (use your browser's inspect tool to find them).\n")

    start_url = input("🔗 Starting URL (e.g., https://example.com/products): ").strip()
    if not start_url:
        print("URL required.")
        return

    product_selector = input(" Product container CSS selector (e.g., '.product'): ").strip()
    name_sel = input(" Name selector within container (e.g., '.name'): ").strip()
    price_sel = input(" Price selector (e.g., '.price'): ").strip()
    rating_sel = input(" Rating selector (optional, press Enter to skip): ").strip() or None
    next_sel = input(" Next page link selector (optional, e.g., '.next a'): ").strip() or None

    max_pages_input = input("📊 Max pages to scrape (optional, press Enter for all): ").strip()
    max_pages = int(max_pages_input) if max_pages_input.isdigit() else None

    filename = input("💾 Output CSV filename (default: products.csv): ").strip() or 'products.csv'

    print("\n Starting scrape...\n")
    data = scrape_products(start_url, product_selector, name_sel, price_sel, rating_sel, next_sel, max_pages)

    if data:
        save_csv(data, filename)
    else:
        print("❌ No data scraped. Check selectors and URL.")

if __name__ == '__main__':
    main()