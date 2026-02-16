import os
from dotenv import load_dotenv

load_dotenv()

HN_API_BASE = "http://hn.algolia.com/api/v1"
HN_SEARCH_QUERIES = [
    "AI jobs",
    "machine learning career",
    "data science salary",
    "ML engineer hiring",
    "remote AI work",
    "artificial intelligence employment",
]
HN_RESULTS_PER_QUERY = 50

KAGGLE_DATASET = "hummaamqaasim/jobs-in-data"
KAGGLE_DATA_FILE = "jobs_in_data.csv"

AI_TICKERS = ["NVDA", "MSFT", "GOOG", "META", "AMZN"]
STOCK_START_DATE = "2020-01-01"
STOCK_END_DATE = "2025-12-31"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
CLEANED_DIR = os.path.join(DATA_DIR, "cleaned")
VIZ_DIR = os.path.join(BASE_DIR, "visualizations")

for directory in [RAW_DIR, PROCESSED_DIR, CLEANED_DIR, VIZ_DIR]:
    os.makedirs(directory, exist_ok=True)
