import yfinance as yf
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def fetch_ticker_info(ticker_symbol: str) -> dict:
    """Fetches live market data using yfinance's native crumb/cookie handling."""
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    
    long_name = info.get('longName', ticker_symbol)
    summary = info.get('longBusinessSummary', 'No summary available.')
    price = info.get('currentPrice', info.get('regularMarketPrice', 0.0))
    prev_close = info.get('previousClose', price)
    
    # Calculate percentage change
    change_pct = 0.0
    if prev_close and prev_close > 0:
        change_pct = ((price - prev_close) / prev_close) * 100
        
    # Format currency and change
    currency = "Rs." if str(ticker_symbol).endswith(".NS") else "$"
    formatted_price = f"{currency}{price:.2f}"
    formatted_change = f"{change_pct:+.2f}%"
    
    text_data = f"Company: {long_name}. Current Price: {formatted_price}. Business Summary: {summary}"
    
    return {
        "text": text_data,
        "url": f"https://finance.yahoo.com/quote/{ticker_symbol}",
        "price": formatted_price,
        "change": formatted_change,
        "name": long_name
    }