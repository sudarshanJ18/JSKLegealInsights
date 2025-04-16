import requests
from bs4 import BeautifulSoup
import os
import logging

# Assume you are using Django-style settings
from django.conf import settings

logger = logging.getLogger(__name__)

def fetch_case_law(query):
    """
    Fetch case law data from Indian Kanoon via web scraping.
    Returns structured data with status.
    """
    try:
        base_url = "https://www.indiankanoon.org/search/"
        params = {"formInput": query}

        response = requests.get(base_url, params=params, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for item in soup.select("div.result_title"):
            title = item.get_text(strip=True)
            url = "https://www.indiankanoon.org" + item.find("a")["href"]
            date = item.find_next_sibling("div").get_text(strip=True) if item.find_next_sibling("div") else "Unknown Date"
            results.append({"title": title, "url": url, "date": date})

        return {
            'results': results,
            'status': 'success'
        } if results else {
            'results': [],
            'status': 'success',
            'message': 'No results found.'
        }

    except Exception as e:
        logger.error(f"Error in fetch_case_law: {e}")
        return {
            'results': [],
            'status': 'error',
            'message': str(e)
        }

def fetch_legal_news():
    """
    Fetch legal news from NewsAPI.
    Returns a list of articles or empty list on failure.
    """
    try:
        api_key = settings.NEWS_API_KEY
        url = f"https://newsapi.org/v2/everything?q=law+legal&language=en&apiKey={api_key}"

        response = requests.get(url)
        response.raise_for_status()

        articles = response.json().get("articles", [])
        return articles

    except Exception as e:
        logger.error(f"Error in fetch_legal_news: {e}")
        return []

def fetch_legal_articles_from_newsdata():
    """
    Fetch legal articles from NewsData.io
    Returns list of articles or empty list on failure.
    """
    try:
        api_key = settings.NEWSDATA_API_KEY
        url = f"https://newsdata.io/api/1/news?apikey={api_key}&q=legal%20OR%20law%20OR%20court&language=en&country=in"

        response = requests.get(url)
        response.raise_for_status()

        articles = response.json().get("results", [])
        return articles

    except Exception as e:
        logger.error(f"Error in fetch_legal_articles_from_newsdata: {e}")
        return []
