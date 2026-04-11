"""
Telegram Transmission Adapter
Author: Dhiraj Malwade
"""
import os
import re
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from src.utils.logger import log

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _post_telegram(url: str, payload: dict) -> requests.Response:
    """Internal function handling the raw HTTP request, dialect translation, and fallback."""
    
    # First-Order Thinking: Translate standard Markdown to Telegram Legacy Dialect
    if payload.get("parse_mode") == "Markdown":
        text = payload["text"]
        # Convert standard bold to Telegram bold
        text = text.replace("**", "*")
        # Convert Markdown headers to Telegram bold text
        text = re.sub(r'^#+\s*(.*?)\s*$', r'*\1*', text, flags=re.MULTILINE)
        # Convert horizontal rules to simple dashes
        text = re.sub(r'^={3,}|-{3,}$', '---', text, flags=re.MULTILINE)
        payload["text"] = text

    response = requests.post(url, json=payload, timeout=15)
    
    # Second-Order Thinking: Clean plain-text fallback if dialect parsing still fails
    if response.status_code == 400 and payload.get("parse_mode") == "Markdown":
        log.warning("Telegram rejected dialect formatting. Applying clean plain-text fallback.")
        del payload["parse_mode"]
        # Scrub all remaining markdown artifacts for a pristine plain-text UI
        clean_text = re.sub(r'[*_`]', '', payload["text"])
        payload["text"] = clean_text
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
        log.error(f"Transmission failed after all retries. Error caught securely.")
        return False