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
from src.delivery.transmission import send_telegram_message
from src.utils.logger import log

checkpoint_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "checkpoints"))
db_path = os.path.join(checkpoint_dir, "aegis.db")

# Critical Cloud Fix: Ensure the directory exists before SQLite tries to open the file
os.makedirs(checkpoint_dir, exist_ok=True)

def delivery_node(state: AgentState) -> dict:
    if os.getenv("AEGIS_SUPPRESS_DELIVERY") == "true":
        log.info(f"Delivery sequence suppressed for {state.ticker} (Scheduler Mode active).")
        return {}
        
    log.info(f"Initiating delivery sequence for {state.ticker}")
    
    message = f"*AEGIS INTELLIGENCE: {state.company_name or state.ticker}*\n"
    message += f"Current Price: {state.current_price}\n"
    message += f"24h Change: {state.change_percent}\n"
    message += f"Authentication: {'VERIFIED' if state.verified else 'UNVERIFIED'}\n\n"
    message += f"{state.final_brief}"
    
    success = send_telegram_message(message)
    if not success:
        log.error("Delivery sequence aborted due to transmission failure.")
        
    return {}

def check_verification(state: AgentState) -> str:
    if state.verified:
        return "synthesis"
    return END

workflow = StateGraph(AgentState)

workflow.add_node("triage", triage_node)
workflow.add_node("auth", auth_node)
workflow.add_node("synthesis", synthesis_node)
workflow.add_node("formatting", formatting_node)
workflow.add_node("delivery", delivery_node)

workflow.set_entry_point("triage")
workflow.add_edge("triage", "auth")
workflow.add_conditional_edges("auth", check_verification)
workflow.add_edge("synthesis", "formatting")
workflow.add_edge("formatting", "delivery")
workflow.add_edge("delivery", END)

conn = sqlite3.connect(db_path, check_same_thread=False)
memory = SqliteSaver(conn)
app = workflow.compile(checkpointer=memory)

def invoke_graph_autonomous(ticker: str) -> dict:
    log.info(f"Commencing Autonomous Intelligence Acquisition for: {ticker}")
    
    raw_text = ""
    current_price = None
    change_percent = None
    company_name = None
    
    try:
        market_data = fetch_ticker_info(ticker)
        raw_text += market_data['text']
        current_price = market_data['price']
        change_percent = market_data['change']
        company_name = market_data['name']
        ingest_data(market_data['text'], market_data['url'], ticker)
    except Exception as e:
        log.error(f"Critical Market fetch failed: {e}")
        
    try:
        news_data = fetch_news(f"{ticker} finance news", max_results=2)
        if not news_data:
            log.warning("News fetch returned empty. Network block active.")
        for news in news_data:
            raw_text += "\n" + news['text']
            ingest_data(news['text'], news['url'], ticker)
    except Exception as e:
        log.error(f"News fetch error: {e}")

    initial_state = AgentState(
        ticker=ticker,
        raw_data=raw_text,
        current_price=current_price,
        change_percent=change_percent,
        company_name=company_name
    )
    
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    log.info("State Machine Engaged. Traversing Cognitive Graph...")
    result_state = app.invoke(initial_state, config=config)
    log.info("Graph Execution Complete.")
    
    return result_state