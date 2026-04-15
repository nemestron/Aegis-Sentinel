"""
Hourly Scheduler and Consolidated Reporter
Author: Dhiraj Malwade
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import pytz
from dotenv import load_dotenv

from src.watchlist import WATCHLIST
from src.graph_engine import invoke_graph_autonomous
from src.reconnaissance.search import get_market_headlines
from src.delivery.transmission import send_telegram_message
from src.utils.logger import SecretRedacter

load_dotenv()

# Configure dedicated scheduler logger
s_logger = logging.getLogger("aegis_scheduler")
s_logger.setLevel(logging.INFO)
if not s_logger.handlers:
    secrets = [os.getenv("GROQ_API_KEY", ""), os.getenv("TELEGRAM_BOT_TOKEN", ""), os.getenv("TELEGRAM_CHAT_ID", "")]
    handler = RotatingFileHandler("aegis_scheduler.log", maxBytes=5*1024*1024, backupCount=3)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    handler.addFilter(SecretRedacter(secrets))
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.addFilter(SecretRedacter(secrets))
    s_logger.addHandler(handler)
    s_logger.addHandler(console)

def generate_hourly_brief() -> str:
    # Suppress individual graph deliveries to prevent spam
    os.environ["AEGIS_SUPPRESS_DELIVERY"] = "true"
    
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist).strftime('%Y-%m-%d %H:%M %Z')
    
    message = f"*AEGIS HOURLY CONSOLIDATED REPORT*\nTimestamp: {now}\n\n"
    message += "*WATCHLIST PULSE*\n"
    message += "---\n\n"
    
    for item in WATCHLIST:
        symbol = item["symbol"]
        name = item["name"]
        s_logger.info(f"Processing watchlist target: {name} ({symbol})")
        
        try:
            state = invoke_graph_autonomous(symbol)
            price = state.get("current_price", "N/A")
            change = state.get("change_percent", "N/A")
            brief = state.get("final_brief", "No brief generated.")
            verified = "VERIFIED" if state.get("verified") else "UNVERIFIED"
            
            message += f"*{name} ({symbol})* - {price} ({change})\n"
            message += f"Auth: {verified}\n"
            message += f"{brief}\n\n"
        except Exception as e:
            s_logger.error(f"Failed to process {symbol}: {e}")
            message += f"*{name} ({symbol})*\nStatus: Acquisition Failed.\n\n"

    message += "*GLOBAL MACRO HEADLINES*\n"
    message += "---\n"
    headlines = get_market_headlines()
    if headlines:
        for h in headlines:
            title = h.get("title", "No Title")
            url = h.get("url", "#")
            message += f"- [{title}]({url})\n"
    else:
        message += "No macro headlines available at this time.\n"
        
    return message

def run_hourly_update():
    s_logger.info("Initiating Aegis Sentinel Hourly Update Cycle...")
    report = generate_hourly_brief()
    
    s_logger.info("Transmitting consolidated report to Telegram...")
    success = send_telegram_message(report)
    if success:
        s_logger.info("Hourly Update Cycle completed successfully.")
    else:
        s_logger.error("Failed to transmit the hourly report.")

if __name__ == "__main__":
    run_hourly_update()