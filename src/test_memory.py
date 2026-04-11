"""
Memory & Ingestion Test Script
Author: Dhiraj Malwade
"""
import sys
import os

# Ensure the root project directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.reconnaissance.market_data import fetch_ticker_info
from src.reconnaissance.search import fetch_news
from src.memory.vector_store import ingest_data, search_memory

def test_pipeline():
    # Changed ticker to NVDA to ensure we test fresh ingestion, not cached data
    ticker = "NVDA"
    print(f"[*] Fetching live data for {ticker}...")
    
    # 1. Fetch Market Data
    try:
        market_data = fetch_ticker_info(ticker)
        print(f"[+] Retrieved Market Data from: {market_data['url']}")
        ingest_data(market_data['text'], market_data['url'])
    except Exception as e:
        print(f"[-] Failed to fetch market data: {e}")
    
    # 2. Fetch News Data
    news_data = fetch_news(f"{ticker} finance news", max_results=2)
    if not news_data:
        print("[-] News fetch returned empty. Network might be blocking requests.")
    for news in news_data:
        print(f"[+] Retrieved News from: {news['url']}")
        ingest_data(news['text'], news['url'])
        
    # 3. Test Retrieval
    query = f"What is the business summary and current news for {ticker}?"
    print(f"\n[*] Querying ChromaDB: '{query}'")
    
    results = search_memory(query, n_results=4)
    
    print("\n--- RETRIEVED DOCUMENTS ---")
    docs = results.get('documents', [[]])[0]
    metadatas = results.get('metadatas', [[]])[0]
    
    for i in range(len(docs)):
        print(f"\nDocument {i+1}:")
        print(f"Content: {docs[i]}")
        print(f"Source URL: {metadatas[i]['source']}")
        
    print("\n[SUCCESS] Memory pipeline executed successfully.")

if __name__ == "__main__":
    test_pipeline()