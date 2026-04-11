import yfinance as yf
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def fetch_ticker_info(ticker_symbol: str) -> dict:
    """Fetches live market data and company information with strict network headers."""
    session = requests.Session()
    session.headers.update({"User-Agent": "AegisSentinel/1.0 (Research Pipeline)"})
    
    # yfinance uses the custom session for its internal requests
    ticker = yf.Ticker(ticker_symbol, session=session)
    info = ticker.info
    
    long_name = info.get('longName', ticker_symbol)
    summary = info.get('longBusinessSummary', 'No summary available.')
    price = info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))
    
    text_data = f"Company: {long_name}. Current Price: {price}. Business Summary: {summary}"
    
    return {
        "text": text_data,
        "url": f"https://finance.yahoo.com/quote/{ticker_symbol}"
    }