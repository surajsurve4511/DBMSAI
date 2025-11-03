# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    
    # Database Configuration
    DB_CONFIG = {
        'host': 'localhost',
        'database': 'hospital',
        'user': 'root',
        'password': '',
        'port': 3306
    }
    
    # Application Settings
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000
    
    # Pagination
    ITEMS_PER_PAGE = 10
    
    # AI Model Settings
    AI_MODEL_PATH = 'models/'
    PREDICTION_CONFIDENCE_THRESHOLD = 0.7
    
    # Google Gemini AI API Configuration
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') or 'YOUR_GEMINI_API_KEY_HERE'
    GEMINI_MODEL = 'gemini-pro'
    
    # AI Features Toggle
    USE_GEMINI_AI = True  # Set to False to use basic AI only
