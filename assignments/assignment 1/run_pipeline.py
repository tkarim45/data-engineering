from datetime import datetime

from extract_api import extract_hn_stories
from extract_dataset import load_kaggle_dataset
from extract_timeseries import extract_stock_data
from load_data import save_raw, save_processed, save_cleaned
from transform import (
    assess_quality, clean_hn_data, clean_jobs_data,
    clean_stock_data, generate_summary_statistics,
)


def run_extraction():
    print("\n" + "=" * 70)
    print("PHASE 1: EXTRACTION")
    print("=" * 70)

    print("\n[1/3] HackerNews API Extraction")
    print("-" * 40)
    hn_df = extract_hn_stories()

    print("\n[2/3] Kaggle Dataset Loading")
    print("-" * 40)
    jobs_df = load_kaggle_dataset()

    print("\n[3/3] Yahoo Finance Time-Series Extraction")
    print("-" * 40)
    stock_df = extract_stock_data()

    return hn_df, jobs_df, stock_df


def run_load(hn_df, jobs_df, stock_df):
    print("\n" + "=" * 70)
    print("PHASE 2: LOADING")
    print("=" * 70)

    print("\nSaving raw data...")
    save_raw(hn_df, "hn_stories_raw.csv")
    save_raw(jobs_df, "ai_jobs_dataset_raw.csv")
    save_raw(stock_df, "stock_data_raw.csv")

    print("\nSaving processed data (CSV + JSON)...")
    save_processed(hn_df, "hn_stories")
    save_processed(jobs_df, "ai_jobs_dataset")
    save_processed(stock_df, "stock_data")


def run_transform(hn_df, jobs_df, stock_df):
    print("\n" + "=" * 70)
    print("PHASE 3: TRANSFORMATION & CLEANING")
    print("=" * 70)

    assess_quality(hn_df, "HackerNews Stories")
    assess_quality(jobs_df, "AI Jobs Dataset")
    assess_quality(stock_df, "Stock Data")

    hn_clean = clean_hn_data(hn_df.copy())
    jobs_clean = clean_jobs_data(jobs_df.copy())
    stock_clean = clean_stock_data(stock_df.copy())

    generate_summary_statistics(jobs_clean, "AI Jobs (Cleaned)")
    generate_summary_statistics(stock_clean, "Stock Data (Cleaned)")

    print("\nSaving cleaned data...")
    save_cleaned(hn_clean, "hn_stories_cleaned")
    save_cleaned(jobs_clean, "ai_jobs_cleaned")
    save_cleaned(stock_clean, "stock_data_cleaned")

    return hn_clean, jobs_clean, stock_clean


def main():
    start_time = datetime.now()

    print("=" * 70)
    print("  AI LABOR MARKETS - ELT PIPELINE")
    print(f"  Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    hn_df, jobs_df, stock_df = run_extraction()

    run_load(hn_df, jobs_df, stock_df)

    hn_clean, jobs_clean, stock_clean = run_transform(
        hn_df, jobs_df, stock_df
    )

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print("\n" + "=" * 70)
    print("  PIPELINE COMPLETE")
    print("=" * 70)
    print(f"  Duration: {duration:.1f} seconds")
    print(f"  Datasets extracted: 3")
    print(f"    - HN stories:     {len(hn_df)} raw -> {len(hn_clean)} cleaned")
    print(f"    - AI jobs dataset: {len(jobs_df)} raw -> {len(jobs_clean)} cleaned")
    print(f"    - Stock data:      {len(stock_df)} raw -> {len(stock_clean)} cleaned")
    print(f"  Data saved to: data/raw/, data/processed/, data/cleaned/")
    print(f"\n  Next step: Open analysis.ipynb for EDA and visualizations")


if __name__ == "__main__":
    main()
