from ddgs import DDGS
from tenacity import retry, stop_after_attempt, wait_exponential
from src.utils.logger import log

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _execute_news_fetch(query: str, max_results: int) -> list[dict]:
    results = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    with DDGS(headers=headers, timeout=20) as ddgs:
        news_items = ddgs.news(query, max_results=max_results)
        if news_items:
            for item in news_items:
                title = item.get('title', 'No Title')
                body = item.get('body', 'No Content')
                url = item.get('url', 'No URL')
                
                results.append({
                    "text": f"News Title: {title}. Content: {body}",
                    "url": url,
                    "title": title
                })
    return results

def fetch_news(query: str, max_results: int = 3) -> list[dict]:
    """Fetches live news, catching rate limits gracefully."""
    try:
        return _execute_news_fetch(query, max_results)
    except Exception as e:
        log.warning(f"News fetch rate limited or blocked. Proceeding with partial intelligence. Details: {e}")
        return []

def get_market_headlines(query: str = "global financial markets breaking news", max_results: int = 3) -> list[dict]:
    """Fetches top global finance macro headlines."""
    try:
        raw_news = _execute_news_fetch(query, max_results)
        return [{"title": n["title"], "url": n["url"]} for n in raw_news]
    except Exception as e:
        log.warning(f"Macro headline fetch failed: {e}")
        return []