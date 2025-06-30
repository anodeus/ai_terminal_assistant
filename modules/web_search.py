
"""web_search.py
Simple DuckDuckGo HTML scraping to get the first result title.
"""
from __future__ import annotations
import requests
from bs4 import BeautifulSoup

def web_search(query: str) -> str:
    try:
        url = "https://duckduckgo.com/html/?q=" + requests.utils.quote(query)
        html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        res = soup.find("a", class_="result__a")
        return res.text.strip() if res else "No result found."
    except Exception as e:
        return f"Search error: {e}"
