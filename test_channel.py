"""
Public Channel Broadcast Validation
Author: Dhiraj Malwade
"""
import os
from dotenv import load_dotenv
from src.delivery.transmission import send_telegram_message

def verify_channel_broadcast():
    load_dotenv()
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    print(f"[*] Verifying Telegram configuration for destination: {chat_id}")
    
    if not chat_id or not chat_id.startswith('@'):
        print("[-] WARNING: For a public channel, TELEGRAM_CHAT_ID should typically start with '@'. Ensure this is correct if using a username.")
        
    test_payload = (
        "*AEGIS SENTINEL SYSTEM ALIVE*\n"
        "---\n"
        "Public broadcast routing verified successfully. "
        "The autonomous pipeline is authorized and secured."
    )
    
    success = send_telegram_message(test_payload)
    
    if success:
        print("[+] SUCCESS: Transmission authorized. Bot successfully posted to the public channel.")
    else:
        print("[-] FAILURE: Transmission rejected. Verify the bot is an Administrator in the channel with 'Post Messages' permission.")

if __name__ == "__main__":
    verify_channel_broadcast()