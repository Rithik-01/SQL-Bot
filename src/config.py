import os
from dotenv import load_dotenv

load_dotenv()
DB_NAME="sales data"
DB_URL=os.getenv("DB_URL")
# API Keys 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
