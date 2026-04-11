from ddgs import DDGS
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _execute_news_fetch(query: str, max_results: int) -> list[dict]:
    results = []
    # Standard browser User-Agent to mitigate basic blocking
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
                    "url": url
                })
    return results

def fetch_news(query: str, max_results: int = 3) -> list[dict]:
    """Fetches live news, catching rate limits gracefully to prevent pipeline crashes."""
    try:
        return _execute_news_fetch(query, max_results)
    except Exception as e:
        print(f"[!] Notice: News fetch rate limited or blocked. Proceeding with partial intelligence. Details: {e}")
        return []