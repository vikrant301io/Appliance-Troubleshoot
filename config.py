"""Configuration settings for the application"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
# Load from project root directory
BASE_DIR = Path(__file__).parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

# File paths
BASE_DIR = Path(__file__).parent
KNOWLEDGE_BASE_PATH = BASE_DIR / "data" / "knowledge_base.json"
BOOKINGS_PATH = BASE_DIR / "data" / "bookings.json"

# OpenAI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_TEXT = "gpt-4o-mini"
OPENAI_MODEL_VISION = "gpt-4o"

# App settings
TECHNICIAN_FEE = 125.0
MAX_IMAGE_SIZE_MB = 10

# Streamlit settings
PAGE_TITLE = "Appliance Troubleshoot Assistant"
PAGE_ICON = "🔧"

