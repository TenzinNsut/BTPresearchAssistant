from scrapers.ArxivScraper import arxiv_scrap
from scrapers.IeeeScraper import ieee_scrap
from scrapers.ScienceDirectScraper import scdir_scrap


def store_data(url):
    try:
        if "https://www.sciencedirect.com/" in url:
            data = scdir_scrap(url)
        elif "https://arxiv.org/" in url:
            data = arxiv_scrap(url)
        elif "https://ieeexplore.ieee.org" in url:
            data = ieee_scrap(url)
        else:
            raise ValueError("Enter a valid URL")
        return data
    except Exception as e:
        print(f"Error while processing URL {url}: {e}")
        return None

# store_data(url)







