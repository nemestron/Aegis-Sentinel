from duckduckgo_search import DDGS
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def fetch_news(query: str, max_results: int = 3) -> list[dict]:
    """Fetches live news articles with timeouts and custom headers."""
    results = []
    headers = {"User-Agent": "AegisSentinel/1.0 (Research Pipeline)"}
    
    # Implementing timeout and headers to prevent silent block failures
    with DDGS(headers=headers, timeout=15) as ddgs:
        news_items = ddgs.news(query, max_results=max_results)
        if news_items:
            for item in news_items:
                title = item.get('title', 'No Title')
                body = item.get('body', 'No Content')
                url = item.get('url', 'No URL')
                
                results.append({
                    "text": f"News Title: {title}. Content: {body}",
                    "url": url
                })
    return results