import os
import pandas as pd

from config import RAW_DIR, KAGGLE_DATASET


def load_kaggle_dataset(dataset_path=None):
    local_paths = [
        dataset_path,
        os.path.join(RAW_DIR, "jobs_in_data.csv"),
        os.path.join(RAW_DIR, "ai_jobs_dataset.csv"),
        os.path.join(RAW_DIR, "salaries.csv"),
    ]

    for path in local_paths:
        if path and os.path.exists(path):
            print(f"  Loading dataset from {path}")
            df = pd.read_csv(path)
            print(f"  Loaded {len(df)} records from local dataset.")
            return df

    try:
        import kaggle
        print(f"  Downloading dataset: {KAGGLE_DATASET}")
        kaggle.api.dataset_download_files(
            KAGGLE_DATASET, path=RAW_DIR, unzip=True
        )
        for f in os.listdir(RAW_DIR):
            if f.endswith(".csv"):
                df = pd.read_csv(os.path.join(RAW_DIR, f))
                print(f"  Downloaded and loaded {len(df)} records.")
                return df
    except Exception as e:
        print(f"  Kaggle API not available: {e}")

    raise FileNotFoundError(
        "No dataset found. Please either:\n"
        "  1. Download from Kaggle and place CSV in data/raw/\n"
        "  2. Configure Kaggle API credentials (~/.kaggle/kaggle.json)\n"
        f"  Expected dataset: {KAGGLE_DATASET}"
    )
