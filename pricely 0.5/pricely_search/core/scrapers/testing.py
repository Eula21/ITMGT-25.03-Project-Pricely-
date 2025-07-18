# EUL JUL 16 | Don't pay attention to this, this is just how I test my scraping code.

import time
import re
from playwright.sync_api import sync_playwright

eBay_list_of_products = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    page = context.new_page()

    page.goto("https://www.ebay.com/", timeout=60000)

    search_input_selector = 'input#gh-ac'
    if not page.query_selector(search_input_selector):
        print("❌ Search box not found — page may be blocked or malformed.")
        browser.close()
        exit()

    query = input("What do you want to buy in eBay?")
    
    page.fill(search_input_selector, query)
    page.press(search_input_selector, "Enter")
    time.sleep(2)

    try:
        page.wait_for_selector("li.s-item", timeout=10000)
    except:
        print("❌ Search results didn't load — possible block or slow network.")
        browser.close()
        exit()

    products = page.query_selector_all("li.s-item")[:5]

    if not products:
        print("ℹ️ No products found.")
        browser.close()
        exit()

    for product in products:
        try:
            title_tag = product.query_selector("div.s-item__info a.s-item__link div.s-item__title")
            product_title = title_tag.inner_text().strip() if title_tag else "No title"

            price_tag = product.query_selector("span.s-item__price")
            price = price_tag.inner_text().strip() if price_tag else "N/A"

            rating_tag = product.query_selector("div.x-star-rating span.clipped")
            if rating_tag and "out of 5 stars" in rating_tag.inner_text():
                rating_text = rating_tag.inner_text()
                rating_match = re.search(r"([0-5](?:\.\d)?) out of 5 stars", rating_text)
                rating = float(rating_match.group(1)) if rating_match else "N/A"
            else:
                rating = "N/A"

            rating_count_tag = product.query_selector("span.s-item__reviews-count span")
            if rating_count_tag:
                digits = re.sub(r"[^\d]", "", rating_count_tag.inner_text())
                rating_count = int(digits) if digits.isdigit() else "N/A"
            else:
                rating_count = "N/A"

            image_tag = product.query_selector("img")
            image_url = image_tag.get_attribute("src") if image_tag else "N/A"

            url_tag = product.query_selector("a.s-item__link")
            href = url_tag.get_attribute("href") if url_tag else None
            product_url = href or "N/A"

            product_data = {
                "product_title": product_title,
                "price": price,
                "rating": rating,
                "rating_count": rating_count,
                "product_url": product_url,
                "image_url": image_url,
                "platform": "eBay",
                "shop_name": "eBay Seller"
            }

            eBay_list_of_products.append(product_data)

        except Exception as e:
            print(f"⚠️ Error parsing product: {e}")

    browser.close()

# 🔽 Print all results
if eBay_list_of_products:
    for item in eBay_list_of_products:
        print("\n--- eBay Product ---")
        for key, value in item.items():
            print(f"{key}: {value}")
else:
    print("⚠️ No valid products scraped.")
