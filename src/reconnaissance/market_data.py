import yfinance as yf
from tenacity import retry, stop_after_attempt, wait_exponential
from src.utils.logger import log

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def fetch_ticker_info(ticker_symbol: str) -> dict:
    """Fetches live market data and dynamically converts USD commodities to INR."""
    # Fetch live USD/INR exchange rate
    try:
        inr_ticker = yf.Ticker("INR=X")
        inr_rate = inr_ticker.info.get('regularMarketPrice', inr_ticker.info.get('previousClose', 83.5))
    except Exception as e:
        log.warning(f"Failed to fetch live INR rate, defaulting to 83.5. Error: {e}")
        inr_rate = 83.5

    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    
    long_name = info.get('shortName', info.get('longName', ticker_symbol))
    summary = info.get('description', info.get('longBusinessSummary', 'Global Commodity Future.'))
    
    usd_price = info.get('currentPrice', info.get('regularMarketPrice', info.get('previousClose', 0.0)))
    usd_prev_close = info.get('previousClose', usd_price)
    
    # Calculate percentage change
    change_pct = 0.0
    if usd_prev_close and usd_prev_close > 0:
        change_pct = ((usd_price - usd_prev_close) / usd_prev_close) * 100
        
    # Convert USD price to INR
    inr_price = usd_price * inr_rate
    
    # Format currency and change
    formatted_price = f"Rs. {inr_price:,.2f}"
    formatted_change = f"{change_pct:+.2f}%"
    
    text_data = f"Asset: {long_name}. Current Price: {formatted_price} (Converted from USD at {inr_rate:.2f} INR/USD). Summary: {summary}"
    
    return {
        "text": text_data,
        "url": f"https://finance.yahoo.com/quote/{ticker_symbol}",
        "price": formatted_price,
        "change": formatted_change,
        "name": long_name
    }