import requests
from bs4 import BeautifulSoup
import os

def fetch_case_law(query):
    """Scrapes case law results from Indian Kanoon based on the search query."""
    
    base_url = "https://www.indiankanoon.org/search/"
    params = {"formInput": query}

    try:
        response = requests.get(base_url, params=params, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # Raise an error for bad responses

        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        # Extract case law titles and links
        for item in soup.select("div.result_title"):
            title = item.get_text(strip=True)
            url = "https://www.indiankanoon.org" + item.find("a")["href"]
            date = item.find_next_sibling("div").get_text(strip=True) if item.find_next_sibling("div") else "Unknown Date"
            results.append({"title": title, "url": url, "date": date})

        return {"cases": results} if results else {"error": "No results found."}

    except requests.exceptions.RequestException as e:
        return {"error": f"Scraping failed: {str(e)}"}

def fetch_legal_news():
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return {"error": "Missing News API Key"}

    url = f"https://newsapi.org/v2/everything?q=law+legal&language=en&apiKey={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("articles", [])
    except requests.exceptions.RequestException as e:
        print("Error fetching news:", e)
        return {"error": str(e)}

def fetch_legal_articles_from_newsdata():
    api_key = os.getenv("NEWSDATA_API_KEY")
    if not api_key:
        return {"error": "Missing NewsData API Key"}

    url = f"https://newsdata.io/api/1/news?apikey={api_key}&q=legal%20OR%20law%20OR%20court&language=en&country=in"

    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get("results", [])
        return articles
    except requests.exceptions.RequestException as e:
        print("Error fetching articles:", e)
        return []
