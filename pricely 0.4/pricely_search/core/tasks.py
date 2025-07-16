from celery import shared_task, chord, group
from core.scrapers import WF_Amazon, WF_Lazada, WF_SM, WF_Uniqlo, WF_eBay

# Helper map: scraper name → actual scraper function
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

@shared_task
def aggregate_results(results):
    combined = []
    for result in results:
        combined.extend(result)
    return combined

# Main entry point
def start_scrape_all(query):
    scraper_keys = list(SCRAPER_MAP.keys())
    header = group(run_scraper.s(key, query) for key in scraper_keys)
    final_task = chord(header)(aggregate_results.s())
    return final_task.id  # This is the task_id for tracking
