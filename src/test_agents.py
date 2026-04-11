"""
Cognitive Nodes Integration Test Script
Author: Dhiraj Malwade
"""
import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.reconnaissance.market_data import fetch_ticker_info
from src.reconnaissance.search import fetch_news
from src.memory.vector_store import ingest_data
from src.state import AgentState
from src.agents.nodes import triage_node, auth_node, synthesis_node, formatting_node

def test_cognitive_nodes():
    load_dotenv()
    ticker = "BARC.L"
    print(f"[*] Initializing cognitive node test for {ticker}...")
    
    # 1. Fetch live data & Ingest to memory
    print("[*] Acquiring and embedding fresh intelligence...")
    try:
        market_data = fetch_ticker_info(ticker)
        raw_text = market_data['text']
        ingest_data(market_data['text'], market_data['url'])
    except Exception as e:
        print(f"[-] Market fetch failed: {e}")
        raw_text = ""
        
    news_data = fetch_news(f"{ticker} finance news", max_results=2)
    for news in news_data:
        raw_text += "\n" + news['text']
        ingest_data(news['text'], news['url'])

    if not raw_text:
        print("[-] Critical Failure: No data retrieved to test nodes.")
        return

    # 2. Construct State
    state = AgentState(ticker=ticker, raw_data=raw_text)
    
    # 3. Simulate sequential graph execution
    print("[*] Activating Triage Node (llama-3.1-8b-instant)...")
    triage_update = triage_node(state)
    state.raw_data = triage_update.get("raw_data", state.raw_data)
    
    print("[*] Activating Authentication Node (llama-4-maverick fallback enabled)...")
    auth_update = auth_node(state)
    state.verified = auth_update.get("verified", False)
    state.retrieved_docs = auth_update.get("retrieved_docs", [])
    state.source_links = auth_update.get("source_links", [])
    print(f"[+] Cryptographic Verification Status: {state.verified}")
    
    print("[*] Activating Synthesis Node (deepseek-r1-distill-qwen-32b)...")
    synth_update = synthesis_node(state)
    state.final_brief = synth_update.get("final_brief", "")
    
    print("[*] Activating Formatting Node (llama-3.1-8b-instant)...")
    format_update = formatting_node(state)
    state.final_brief = format_update.get("final_brief", "")
    
    print("\n--- FINAL FORMATTED BRIEF ---")
    print(state.final_brief)
    print("\n[SUCCESS] Phase 3 Node Pipeline executed successfully.")

if __name__ == "__main__":
    test_cognitive_nodes()