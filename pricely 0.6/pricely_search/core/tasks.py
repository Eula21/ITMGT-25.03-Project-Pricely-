from celery import shared_task, chord, group
from core.scrapers import WF_Amazon, WF_Lazada, WF_SM, WF_Uniqlo, WF_eBay

# Map platform keys to their respective scraper functions
SCRAPER_MAP = {
    "amazon": WF_Amazon.scrape_amazon,
    "lazada": WF_Lazada.scrape_lazada,
    "sm": WF_SM.scrape_SM,
    "uniqlo": WF_Uniqlo.scrape_uniqlo,
    "ebay": WF_eBay.scrape_ebay,
}

# Map categories to the platforms to scrape
CATEGORY_SCRAPER_MAP = {
    "fashion and apparel": ["uniqlo", "lazada", "amazon"],
    "groceries": ["sm", "lazada", "amazon"],
    "household essentials": ["sm", "lazada", "amazon", "ebay"],
    "stationery and supplies": ["sm", "lazada", "amazon"],
    "all categories": list(SCRAPER_MAP.keys()),
}

# Task that runs a single scraper
@shared_task
def run_scraper(scraper_key, query):
    scraper_func = SCRAPER_MAP.get(scraper_key)
    if not scraper_func:
        return []
    return scraper_func(query)

# Function to compute score and rank products
def process_and_rank_products(products):
    def compute_weighted_score(p):
        # Default fallback rating and count
        try:
            rating = float(p["rating"].split()[0])
            count = int(p.get("rating_count", 100))
        except:
            rating = 3.0
            count = 100

        # Extract matched_words data
        try:
            matched_raw = p.get("matched_words", "0/10")
            numerator, denominator = map(int, matched_raw.split("/"))
            relevance = numerator / denominator if denominator else 0
        except:
            relevance = 0.0

        # Combine rating * count and relevance * 100
        return (rating * count) + (relevance * 100)

    return sorted(products, key=compute_weighted_score, reverse=True)

# Aggregates all results and ranks them
@shared_task
def aggregate_results(results, query=None):
    combined = []
    query_keywords = set(query.lower().split()) if query else set()

    for result in results:
        for product in result:
            title = product.get("product_title", "").lower()

            # Count how many query words appear in product title
            matched_count = sum(1 for word in query_keywords if word in title)
            total_keywords = len(query_keywords)
            product["matched_words"] = f"{matched_count}/{total_keywords}"

            combined.append(product)

    return process_and_rank_products(combined)

# Main entry point to run only the scrapers relevant to the selected category
def start_scrape_all(query, category="all categories"):
    category = (category or "all categories").strip().lower()
    print(f"[DEBUG] category = {category}")

    allowed_scrapers = CATEGORY_SCRAPER_MAP.get(category, CATEGORY_SCRAPER_MAP["all categories"])
    print(f"[DEBUG] allowed_scrapers = {allowed_scrapers}")

    if "uniqlo" in allowed_scrapers:
        print("[DEBUG WARNING] Uniqlo will be scraped!")

    header = group(run_scraper.s(key, query) for key in allowed_scrapers)
    final_task = chord(header)(aggregate_results.s(query=query))
    return final_task.id
