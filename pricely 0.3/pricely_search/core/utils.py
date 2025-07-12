from .scrapers.WF_Amazon import scrape_amazon

def scrape_and_rank(query):
    raw_results = scrape_amazon(query)  # Already returns structured data

    def get_rating(prod):
        try:
            return float(prod["rating"].split()[0])
        except:
            return 0

    ranked = sorted(raw_results, key=get_rating, reverse=True)
    return ranked