"""
Telemetry and Logging Architecture
"""
import logging
from logging.handlers import RotatingFileHandler
import os

class SecretRedacter(logging.Filter):
    def __init__(self, secrets):
        super().__init__()
        self.secrets = [s for s in secrets if s and len(s) > 4]

    def filter(self, record):
        record.msg = str(record.msg)
        for secret in self.secrets:
            record.msg = record.msg.replace(secret, "***REDACTED***")
        return True

def setup_logger():
    logger = logging.getLogger("aegis_ops")
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        groq_key = os.getenv("GROQ_API_KEY", "")
        tg_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        tg_chat = os.getenv("TELEGRAM_CHAT_ID", "")
        
        secrets_to_hide = [groq_key, tg_token, tg_chat]
        
        # Rotating file handler: 5MB max, 3 backups
        handler = RotatingFileHandler("aegis_ops.log", maxBytes=5*1024*1024, backupCount=3)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        handler.addFilter(SecretRedacter(secrets_to_hide))
        
        # Console handler for local debugging visibility
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        console.addFilter(SecretRedacter(secrets_to_hide))
        
        logger.addHandler(handler)
        logger.addHandler(console)
        
    return logger

log = setup_logger()