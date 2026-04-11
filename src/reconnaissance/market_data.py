import yfinance as yf
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def fetch_ticker_info(ticker_symbol: str) -> dict:
    """Fetches live market data and company information."""
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    
    long_name = info.get('longName', ticker_symbol)
    summary = info.get('longBusinessSummary', 'No summary available.')
    price = info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))
    
    text_data = f"Company: {long_name}. Current Price: {price}. Business Summary: {summary}"
    
    return {
        "text": text_data,
        "url": f"https://finance.yahoo.com/quote/{ticker_symbol}"
    }