def fake_scraper(name, query):
    print(f"Running scraper: {name} for query: '{query}'")
    return [{"platform": name, "query": query}]

SCRAPER_MAP = {
    "amazon": lambda q: fake_scraper("Amazon", q),
    "lazada": lambda q: fake_scraper("Lazada", q),
    "sm": lambda q: fake_scraper("SM", q),
    "uniqlo": lambda q: fake_scraper("Uniqlo", q),
    "ebay": lambda q: fake_scraper("eBay", q),
}

CATEGORY_MAP = {
    "Fashion and Apparel": ["amazon", "lazada", "uniqlo"],
    "Beauty & Fitness": ["amazon", "lazada", "sm"],
    "Home Essentials": ["amazon", "lazada", "sm"],
    "Groceries": ["amazon", "lazada", "sm", "ebay"],
    "Office and School Supplies": ["amazon", "lazada", "ebay"],
}

def start_scrape_all(query, category=None):
    scraper_keys = CATEGORY_MAP.get(category, list(SCRAPER_MAP.keys()))
    print(f"\nSelected scrapers for category '{category}': {scraper_keys}")

    results = []
    for key in scraper_keys:
        scraper_func = SCRAPER_MAP.get(key)
        if scraper_func:
            result = scraper_func(query)
            results.extend(result)

    return results

# ==== RUN TEST ====
if __name__ == "__main__":
    test_query = "shirt"
    test_category = "Fashion and Apparel"  # Change this to test other categories

    scraped_data = start_scrape_all(test_query, test_category)

    print("\nFinal scraped data:")
    for item in scraped_data:
        print(item)
