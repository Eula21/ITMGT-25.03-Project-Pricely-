import time
import re
from playwright.sync_api import sync_playwright

def scrape_lazada(query):
    Lazada_list_of_products = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
            page = context.new_page()

            try:
                page.goto("https://www.lazada.com.ph/", timeout=60000)
            except Exception as e:
                print("[Lazada] Failed to load homepage:", e)
                return []

            search_input_selector = 'input[name="q"]'
            if not page.query_selector(search_input_selector):
                print("[Lazada] Search box not found.")
                return []

            page.fill(search_input_selector, query)
            page.press(search_input_selector, "Enter")
            time.sleep(2)

            try:
                page.wait_for_selector("div.Bm3ON", timeout=10000)
            except:
                print("[Lazada] Search results didn't load.")
                return []

            products = page.query_selector_all("div.Bm3ON")[:8]

            for product in products:
                try:
                    name_tag = product.query_selector("div.RfADt a")
                    product_title = name_tag.inner_text().strip() if name_tag else "No name"

                    price_tag = product.query_selector("span.ooOxS")
                    price = price_tag.inner_text().strip() if price_tag else "N/A"

                    stars = product.query_selector_all("div.mdmmT i._9-ogB.Dy1nx")
                    rating = str(len(stars)) if stars else None  # ensure string

                    count_tag = product.query_selector("div.mdmmT span.qzqFw")
                    rating_count_text = count_tag.inner_text().strip() if count_tag else None
                    if rating_count_text:
                        digits = re.sub(r"[^\d]", "", rating_count_text)
                        rating_count = digits if digits else "N/A"
                    else:
                        rating_count = "N/A"

                    if rating is None:
                        lazmall_badge = product.query_selector("i.ic-dynamic-badge")
                        rating = "5" if lazmall_badge else "4"  # as string

                    url_tag = product.query_selector("a")
                    href = url_tag.get_attribute("href") if url_tag else None
                    product_url = "https:" + href if href and href.startswith("//") else href or "N/A"

                    image_tag = product.query_selector("img")
                    image_url = image_tag.get_attribute("src") if image_tag else "N/A"

                    Lazada_list_of_products.append({
                        "product_title": product_title,
                        "price": price,
                        "rating": rating,
                        "rating_count": rating_count,
                        "product_url": product_url,
                        "image_url": image_url,
                        "platform": "Lazada",
                        "shop_name": "Lazada Seller"
                    })

                except Exception as e:
                    print(f"[Lazada] Error parsing product: {e}")
                    continue

            browser.close()

    except Exception as e:
        print(f"[Lazada] Scraper failed completely: {e}")
        return []

    return Lazada_list_of_products
