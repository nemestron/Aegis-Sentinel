"""
Environment Validation Script
Author: Dhiraj Malwade
"""
import os
from dotenv import load_dotenv

def test_environment():
    load_dotenv()
    groq_key = os.getenv("GROQ_API_KEY")
    tg_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if groq_key and tg_bot_token and tg_chat_id:
        print("[SUCCESS] Environment variables loaded successfully.")
    else:
        print("[ERROR] Missing one or more required environment variables. Please check the .env file.")

if __name__ == "__main__":
    test_environment()