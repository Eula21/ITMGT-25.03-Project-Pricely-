from core.tasks import start_scrape_all
from celery.result import AsyncResult
import time

def run_all_scrapers(*args, **kwargs):
    print("[DEPRECATED] run_all_scrapers() should not be used.")
    raise NotImplementedError("Use AJAX + start_scrape_all instead.")
