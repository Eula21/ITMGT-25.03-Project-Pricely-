from core.tasks import start_scrape_all
from celery.result import AsyncResult
import time

def run_all_scrapers(query, timeout=60, poll_interval=2):
    """
    Starts all scrapers asynchronously and waits for the result.
    This is a synchronous blocking function meant for internal logic (not AJAX).
    """
    task_id = start_scrape_all(query)
    async_result = AsyncResult(task_id)

    # Wait for result (polling)
    start_time = time.time()
    while not async_result.ready():
        if time.time() - start_time > timeout:
            raise TimeoutError("Scraper task timed out.")
        time.sleep(poll_interval)

    if async_result.successful():
        return async_result.result
    else:
        raise Exception(f"Task failed: {async_result.result}")
