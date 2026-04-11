"""
Telegram Transmission Adapter
Author: Dhiraj Malwade
"""
import os
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from src.utils.logger import log

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _post_telegram(url: str, payload: dict) -> requests.Response:
    """Internal function handling the raw HTTP request and retry logic."""
    response = requests.post(url, json=payload, timeout=15)
    
    # Second-Order Thinking: If Telegram rejects the Markdown, strip it and fallback to plain text instantly.
    if response.status_code == 400:
        log.warning("Telegram rejected Markdown formatting. Applying plain-text fallback.")
        if "parse_mode" in payload:
            del payload["parse_mode"]
            response = requests.post(url, json=payload, timeout=15)
            
    response.raise_for_status()
    return response

def send_telegram_message(text: str) -> bool:
    """Public adapter that prevents exceptions from crashing the autonomous graph."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        log.error("Telegram credentials missing or incomplete. Cannot send message.")
        return False
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    if len(text) > 4096:
        text = text[:4050] + "\n\n...[TRUNCATED DUE TO LENGTH]"
        
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    
    log.info("Transmitting compiled report to Telegram network...")
    try:
        _post_telegram(url, payload)
        log.info("Transmission successful.")
        return True
    except Exception as e:
        # Catching the exception here ensures it is filtered by the logger and doesn't leak secrets
        log.error(f"Transmission failed after all retries. Error caught securely.")
        return False