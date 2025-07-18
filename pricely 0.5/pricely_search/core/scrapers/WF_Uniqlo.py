import time
import re
from playwright.sync_api import sync_playwright

def scrape_uniqlo(query):
    UNIQLO_list_of_products = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
            page = context.new_page()

            try:
                page.goto("https://www.uniqlo.com/ph/en/", timeout=60000)
            except Exception as e:
                print("[UNIQLO] Failed to load homepage:", e)
                return []

            try:
                page.click("button.bottom-navigation-icon-wrapper.bottom-navigation-icon-wrapper-center")
            except:
                print("[UNIQLO] Search icon not found or not clickable.")
                return []

            try:
                page.wait_for_selector('input[name="searchTerm"]', timeout=5000)
                page.fill('input[name="searchTerm"]', query)
                page.press('input[name="searchTerm"]', "Enter")
            except:
                print("[UNIQLO] Failed to input search query.")
                return []

            try:
                page.wait_for_selector("div.product-tile", timeout=10000)
            except:
                print("[UNIQLO] Product results not found.")
                return []

            products = page.query_selector_all("div.product-tile")[:5]

            for product in products:
                try:
                    title_tag = product.query_selector("h3.product-tile-product-description")
                    product_title = title_tag.inner_text().strip() if title_tag else "No title"

                    # Try original price first, fallback to current price if needed
                    price_tag = (
                        product.query_selector("span.price-original-ER span:nth-child(2)")
                        or product.query_selector("span.sales span:nth-child(2)")
                    )
                    price = price_tag.inner_text().strip() if price_tag else "N/A"

                    rating_tag = product.query_selector("span.bold.ml-xxxs.small-rating")
                    try:
                        rating = float(rating_tag.inner_text().strip()) if rating_tag else "N/A"
                    except:
                        rating = "N/A"

                    rating_count_tag = product.query_selector("span.fr-review-count span")
                    rating_count = re.sub(r"[^\d]", "", rating_count_tag.inner_text()) if rating_count_tag else "N/A"

                    image_tag = product.query_selector("img.thumb-img")
                    image_url = image_tag.get_attribute("src") if image_tag else "N/A"

                    link_tag = product.query_selector("div.product-tile-image a")
                    href = link_tag.get_attribute("href") if link_tag else None
                    product_url = "https://www.uniqlo.com" + href if href else "N/A"

                    UNIQLO_list_of_products.append({
                        "product_title": product_title,
                        "price": price,
                        "rating": rating,
                        "rating_count": rating_count,
                        "product_url": product_url,
                        "image_url": image_url,
                        "platform": "UNIQLO",
                        "shop_name": "UNIQLO Official"
                    })

                except Exception as e:
                    print(f"[UNIQLO] Error parsing product: {e}")
                    continue

            browser.close()

    except Exception as e:
        print(f"[UNIQLO] Scraper failed completely: {e}")
        return []

    return UNIQLO_list_of_products
