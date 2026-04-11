"""
Autonomous State Machine Graph Engine
Author: Dhiraj Malwade
"""
import os
import uuid
import sqlite3
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from src.state import AgentState
from src.agents.nodes import triage_node, auth_node, synthesis_node, formatting_node
from src.reconnaissance.market_data import fetch_ticker_info
from src.reconnaissance.search import fetch_news
from src.memory.vector_store import ingest_data

# Ensure checkpoints database exists
checkpoint_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "checkpoints"))
db_path = os.path.join(checkpoint_dir, "aegis.db")

# Placeholder for Delivery Node (to be completed in Phase 5)
def delivery_node(state: AgentState) -> dict:
    return {}

# Conditional Routing Logic
def check_verification(state: AgentState) -> str:
    """Routes to synthesis if facts are verified, otherwise terminates."""
    if state.verified:
        return "synthesis"
    return END

# Graph Construction
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("triage", triage_node)
workflow.add_node("auth", auth_node)
workflow.add_node("synthesis", synthesis_node)
workflow.add_node("formatting", formatting_node)
workflow.add_node("delivery", delivery_node)

# Define Edges
workflow.set_entry_point("triage")
workflow.add_edge("triage", "auth")
workflow.add_conditional_edges("auth", check_verification)
workflow.add_edge("synthesis", "formatting")
workflow.add_edge("formatting", "delivery")
workflow.add_edge("delivery", END)

# Establish thread-isolated checkpointer and compile
conn = sqlite3.connect(db_path, check_same_thread=False)
memory = SqliteSaver(conn)
app = workflow.compile(checkpointer=memory)

def invoke_graph_autonomous(ticker: str) -> dict:
    """Executes the pipeline autonomously with data ingestion and checkpointing."""
    print(f"[*] Commencing Autonomous Intelligence Acquisition for: {ticker}")
    
    raw_text = ""
    current_price = None
    change_percent = None
    company_name = None
    
    # 1. Fetch Market Data & Extract Enriched Fields
    try:
        market_data = fetch_ticker_info(ticker)
        raw_text += market_data['text']
        current_price = market_data['price']
        change_percent = market_data['change']
        company_name = market_data['name']
        ingest_data(market_data['text'], market_data['url'], ticker)
    except Exception as e:
        print(f"[-] Critical: Market fetch failed: {e}")
        
    # 2. Fetch News Data
    try:
        news_data = fetch_news(f"{ticker} finance news", max_results=2)
        if not news_data:
            print("[!] Notice: News fetch rate limited or blocked. Proceeding with partial intelligence.")
        for news in news_data:
            raw_text += "\n" + news['text']
            ingest_data(news['text'], news['url'], ticker)
    except Exception as e:
        print(f"[-] News fetch error: {e}")

    # 3. Construct Initial State
    initial_state = AgentState(
        ticker=ticker,
        raw_data=raw_text,
        current_price=current_price,
        change_percent=change_percent,
        company_name=company_name
    )
    
    # 4. Generate unique thread for checkpointing isolation
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    print("[*] State Machine Engaged. Traversing Cognitive Graph...")
    result_state = app.invoke(initial_state, config=config)
    print("[+] Graph Execution Complete.")
    
    return result_state