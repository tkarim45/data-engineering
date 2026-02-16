import os
import pandas as pd

from config import RAW_DIR, PROCESSED_DIR, CLEANED_DIR


def save_raw(df, filename):
    path = os.path.join(RAW_DIR, filename)
    df.to_csv(path, index=False)
    print(f"  Saved raw data: {path} ({len(df)} records)")
    return path


def save_processed(df, name):
    csv_path = os.path.join(PROCESSED_DIR, f"{name}.csv")
    json_path = os.path.join(PROCESSED_DIR, f"{name}.json")

    df.to_csv(csv_path, index=False)
    df.to_json(json_path, orient="records", indent=2, date_format="iso")

    print(f"  Saved processed data:")
    print(f"    CSV:  {csv_path} ({len(df)} records)")
    print(f"    JSON: {json_path} ({len(df)} records)")
    return csv_path, json_path


def save_cleaned(df, name):
    csv_path = os.path.join(CLEANED_DIR, f"{name}.csv")
    json_path = os.path.join(CLEANED_DIR, f"{name}.json")

    df.to_csv(csv_path, index=False)
    df.to_json(json_path, orient="records", indent=2, date_format="iso")

    print(f"  Saved cleaned data:")
    print(f"    CSV:  {csv_path} ({len(df)} records)")
    print(f"    JSON: {json_path} ({len(df)} records)")
    return csv_path, json_path


def load_csv(directory, filename):
    path = os.path.join(directory, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    return pd.read_csv(path)


def load_json(directory, filename):
    path = os.path.join(directory, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    return pd.read_json(path)
