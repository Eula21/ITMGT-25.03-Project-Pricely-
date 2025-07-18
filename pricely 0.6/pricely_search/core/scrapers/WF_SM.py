import time
from playwright.sync_api import sync_playwright

def scrape_SM(query):
    SM_list_of_products = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
            page = context.new_page()

            try:
                page.goto("https://smmarkets.ph/", timeout=60000)
            except Exception as e:
                print("[SM] Failed to load homepage:", e)
                return []

            search_input_selector = 'input[name="search_query"]'
            if not page.query_selector(search_input_selector):
                print("[SM] Search box not found.")
                return []

            page.fill(search_input_selector, query)
            page.keyboard.press("Enter")
            time.sleep(2)

            try:
                page.wait_for_selector("div.item-root-2yA", timeout=10000)
            except:
                print("[SM] Search results didn't load.")
                return []

            products = page.query_selector_all("div.item-root-2yA")[:8]

            for product in products:
                try:
                    name_tag = product.query_selector("a.item-name-23v span")
                    product_title = name_tag.inner_text().strip() if name_tag else "No name"

                    price_tag = product.query_selector("div.item-price-xqn")
                    price = price_tag.inner_text().strip() if price_tag else "N/A"

                    url_tag = product.query_selector("a.item-name-23v")
                    href = url_tag.get_attribute("href") if url_tag else None
                    product_url = (
                        "https://smmarkets.ph" + href
                        if href and not href.startswith("http")
                        else href or "N/A"
                    )

                    image_tag = product.query_selector("img.image-loaded-ktU")
                    image_url = image_tag.get_attribute("src") if image_tag else "N/A"

                    SM_list_of_products.append({
                        "product_title": product_title,
                        "price": price,
                        "rating": "N/A",
                        "rating_count": "N/A",
                        "product_url": product_url,
                        "image_url": image_url,
                        "platform": "SM Markets",
                        "shop_name": "SM Seller"
                    })

                except Exception as e:
                    print(f"[SM] Error parsing product: {e}")
                    continue

            browser.close()

    except Exception as e:
        print(f"[SM] Scraper failed completely: {e}")
        return []

    return SM_list_of_products
