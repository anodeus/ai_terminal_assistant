# web_search.py
"""
web_search.py
Opens search queries or URLs in the default web browser.
Supports Google or DuckDuckGo based on query.
"""

import webbrowser

def open_site_or_search(query: str) -> str:
    """Open a site (if it's a URL) or perform a web search."""
    query = query.strip()

    # Case: exact match "search google"
    if query.lower() == "google":
        target = "https://www.google.com"

    # Case: starts with 'google something' → Google Search
    elif query.lower().startswith("google "):
        search_term = query[7:].strip()
        target = f"https://www.google.com/search?q={search_term}"

    # Case: site or url
    elif query.lower().startswith(("site ", "url ")):
        site = query.split(" ", 1)[1] if " " in query else ""
        if not site.startswith("http"):
            site = "https://" + site
        target = site

    else:
        # Default: DuckDuckGo search
        target = f"https://duckduckgo.com/?q={query}"

    webbrowser.open(target)
    return f"✔ Opened in browser: {target}"
