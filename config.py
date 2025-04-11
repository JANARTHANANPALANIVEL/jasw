import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configurations
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
