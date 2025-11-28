
"""Configuration settings for Thai-Jazz ML Dataset."""
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Output directories
OUTPUT_DIR = PROJECT_ROOT / "output"
ML_DATASET_DIR = OUTPUT_DIR / "ml_dataset"
PHIN_DATASET_DIR = OUTPUT_DIR / "phin_dataset"
NOTATION_DATASET_DIR = OUTPUT_DIR / "music_notation_dataset"

# PDF source
PDF_PATH = PROJECT_ROOT / "attached_assets" / "Tanarat Chaichana - PhD Dissertation [complete] 14_04_2022_1764338380212.pdf"

# Flask settings
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = True

# Dataset settings
MAX_SEARCH_RESULTS = 50
MAX_DISPLAY_PAGES = 100
