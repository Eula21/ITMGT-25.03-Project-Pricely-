from celery import shared_task, chord, group
from core.scrapers import WF_Amazon, WF_Lazada, WF_SM, WF_Uniqlo, WF_eBay

SCRAPER_MAP = {
    "amazon": WF_Amazon.scrape_amazon,
    "lazada": WF_Lazada.scrape_lazada,
    "sm": WF_SM.scrape_SM,
    "uniqlo": WF_Uniqlo.scrape_uniqlo,
    "ebay": WF_eBay.scrape_ebay,
}

@shared_task
def run_scraper(scraper_key, query):
    scraper_func = SCRAPER_MAP.get(scraper_key)
    if not scraper_func:
        return []
    return scraper_func(query)

def process_and_rank_products(products):
    def compute_weighted_score(p):
        # Parse rating safely
        try:
            rating = float(p["rating"].split()[0])
            count = int(p.get("rating_count", 100))  # default count
        except:
            rating = 3.0
            count = 100

        # Parse matched_words relevance (e.g., "2/10")
        try:
            matched_raw = p.get("matched_words", "0/10")
            numerator, denominator = map(int, matched_raw.split("/"))
            relevance = numerator / denominator if denominator else 0
        except:
            relevance = 0.0

        # Weighted score: 70% rating * count, 30% relevance
        return (rating * count) + (relevance * 100)

    return sorted(products, key=compute_weighted_score, reverse=True)

@shared_task
def aggregate_results(results):
    combined = []
    for result in results:
        combined.extend(result)
    return process_and_rank_products(combined)

# Main entry point
def start_scrape_all(query):
    scraper_keys = list(SCRAPER_MAP.keys())
    header = group(run_scraper.s(key, query) for key in scraper_keys)
    final_task = chord(header)(aggregate_results.s())
    return final_task.id  # This is the task_id for tracking
