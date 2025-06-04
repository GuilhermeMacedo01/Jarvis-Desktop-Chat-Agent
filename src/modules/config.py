import os
from dotenv import load_dotenv
import logging

load_dotenv()

HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', '')
NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')

MODEL_NAME = "facebook/blenderbot-3B"
NEWS_ENDPOINT = 'https://newsapi.org/v2/everything'

APP_NAME = "Tech Chat & News"
APP_VERSION = "1.0.0"

def validate_api_keys():
    missing_keys = []
    if not HUGGINGFACE_API_KEY:
        missing_keys.append("HUGGINGFACE_API_KEY")
    if not NEWS_API_KEY:
        missing_keys.append("NEWS_API_KEY")
    
    if missing_keys:
        error_msg = f"Chaves de API necessárias não encontradas: {', '.join(missing_keys)}"
        logging.error(error_msg)
        return False
    return True 