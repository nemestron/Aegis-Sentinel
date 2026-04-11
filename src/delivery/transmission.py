"""
Telegram Transmission Adapter
"""
import os
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from src.utils.logger import log

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def send_telegram_message(text: str) -> bool:
    """Sends a Markdown-formatted message to Telegram with retry logic and truncation."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        log.error("Telegram credentials missing or incomplete. Cannot send message.")
        return False
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # Truncate to 4096 characters per Telegram limits
    if len(text) > 4096:
        text = text[:4050] + "\n\n...[TRUNCATED DUE TO LENGTH]"
        
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    
    log.info("Transmitting compiled report to Telegram network...")
    response = requests.post(url, json=payload, timeout=15)
    response.raise_for_status()
    log.info("Transmission successful.")
    return True