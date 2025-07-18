import time
from playwright.sync_api import sync_playwright

def scrape_amazon(query):
    Amazon_list_of_products = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
            page = context.new_page()

            page.goto("https://www.amazon.com/")

            # Identify search input
            search_input_selector = None
            if page.query_selector("input#twotabsearchtextbox"):
                search_input_selector = "input#twotabsearchtextbox"
            elif page.query_selector("input#nav-bb-search"):
                search_input_selector = "input#nav-bb-search"
            else:
                print("[Amazon] Search input not found")
                return []

            page.fill(search_input_selector, query)
            page.press(search_input_selector, "Enter")
            time.sleep(2)

            try:
                page.wait_for_selector("div[data-component-type='s-search-result']", timeout=10000)
            except:
                print("[Amazon] Search results didn't load.")
                return []

            products = page.query_selector_all("div[data-component-type='s-search-result']")[:5]
            if not products:
                print("[Amazon] No products found.")
                return []

            for product in products:
                try:
                    name_tag = product.query_selector("h2 > span")
                    url_tag = product.query_selector("a.a-link-normal[href*='/dp/']")
                    if not name_tag or not url_tag:
                        continue

                    product_title = name_tag.inner_text().strip()
                    product_url = "https://www.amazon.com" + url_tag.get_attribute("href")

                    price_tag = product.query_selector("span.a-price > span.a-offscreen")
                    price = price_tag.inner_text().strip() if price_tag else "N/A"

                    rating_tag = product.query_selector("span.a-icon-alt")
                    rating = rating_tag.inner_text().strip() if rating_tag else "N/A"

                    image_tag = product.query_selector("img.s-image")
                    image_url = image_tag.get_attribute("src") if image_tag else "N/A"

                    Amazon_list_of_products.append({
                        "product_title": product_title,
                        "price": price,
                        "rating": rating,
                        "product_url": product_url,
                        "image_url": image_url,
                        "platform": "Amazon",
                        "shop_name": "Amazon Seller"
                    })
                except Exception as e:
                    print(f"[Amazon] Error parsing product: {e}")
                    continue

            browser.close()

    except Exception as e:
        print(f"[Amazon] Scraper failed: {e}")
        return []

    return Amazon_list_of_products
