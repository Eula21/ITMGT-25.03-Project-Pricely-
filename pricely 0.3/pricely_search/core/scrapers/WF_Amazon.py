from playwright.sync_api import sync_playwright

def scrape_amazon(query):
    Amazon_list_of_products = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://www.amazon.com/", timeout=60000)

        search_input = None
        if page.query_selector("input#twotabsearchtextbox"):
            search_input = "input#twotabsearchtextbox"
        elif page.query_selector("input#nav-bb-search"):
            search_input = "input#nav-bb-search"
        else:
            print("Search box not found — page may be blocked or malformed.")
            browser.close()
            return []

        page.fill(search_input, query)
        page.click("input[type='submit']")
        page.wait_for_selector("div.puis-padding-left-small", timeout=10000)

        products = page.query_selector_all("div[data-component-type='s-search-result']")[:5]

        for product in products:
            name_tag = product.query_selector("h2 > span")
            product_title = name_tag.inner_text() if name_tag else "No name"

            price_tag = product.query_selector("span.a-price > span.a-offscreen")
            price = price_tag.inner_text() if price_tag else "N/A"

            rating_tag = product.query_selector("span.a-icon-alt")
            rating = rating_tag.inner_text() if rating_tag else "N/A"

            url_tag = product.query_selector("a[href*='/dp/']")
            product_url = "https://www.amazon.com" + url_tag.get_attribute("href") if url_tag else "N/A"

            image_tag = product.query_selector("img.s-image")
            image_url = image_tag.get_attribute("src") if image_tag else ""

            Amazon_list_of_products.append({
                "product_title": product_title,
                "price": price,
                "rating": rating,
                "product_url": product_url,
                "image_url": image_url,
                "platform": "Amazon",
                "shop_name": "Amazon Seller"
            })

        browser.close()
    return Amazon_list_of_products