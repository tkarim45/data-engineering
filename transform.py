import pandas as pd
import numpy as np


def assess_quality(df, dataset_name):
    print(f"\n{'='*60}")
    print(f"DATA QUALITY REPORT: {dataset_name}")
    print(f"{'='*60}")

    print(f"\nShape: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"Columns: {list(df.columns)}")

    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_report = pd.DataFrame({
        "Missing Count": missing,
        "Missing %": missing_pct,
    })
    print(f"\nMissing Values:")
    has_missing = missing_report[missing_report["Missing Count"] > 0]
    if len(has_missing) > 0:
        print(has_missing.to_string())
    else:
        print("  No missing values found.")
    print(f"Total missing values: {missing.sum()}")

    n_dupes = df.duplicated().sum()
    print(f"\nDuplicate Records: {n_dupes} ({n_dupes / len(df) * 100:.2f}%)")

    print(f"\nData Types:")
    for col, dtype in df.dtypes.items():
        print(f"  {col}: {dtype}")

    return {
        "shape": df.shape,
        "missing_total": int(missing.sum()),
        "duplicate_count": int(n_dupes),
        "missing_by_column": missing_report,
    }


def clean_hn_data(df):
    print("\nCleaning HackerNews data...")
    original_len = len(df)

    df = df.drop_duplicates(subset=["story_id"], keep="first")
    print(f"  Removed {original_len - len(df)} duplicate stories.")

    df["story_text"] = df["story_text"].fillna("")
    df["url"] = df["url"].fillna("")
    df["author"] = df["author"].fillna("[unknown]")
    df["points"] = df["points"].fillna(0).astype(int)
    df["num_comments"] = df["num_comments"].fillna(0).astype(int)

    df["created_at"] = pd.to_datetime(df["created_at"])
    df["date"] = df["created_at"].dt.date
    df["year_month"] = df["created_at"].dt.to_period("M").astype(str)

    df["title_length"] = df["title"].str.len()
    df["story_text_length"] = df["story_text"].str.len()

    df["engagement"] = pd.cut(
        df["points"],
        bins=[-1, 10, 100, 500, float("inf")],
        labels=["Low", "Medium", "High", "Viral"],
    )

    print(f"  Cleaned dataset: {len(df)} records")
    return df


def clean_jobs_data(df):
    print("\nCleaning AI jobs data...")
    original_len = len(df)

    df = df.drop_duplicates()
    dupes_removed = original_len - len(df)
    print(f"  Removed {dupes_removed} duplicate records.")

    if "salary_in_usd" in df.columns:
        median_salary = df["salary_in_usd"].median()
        n_missing = df["salary_in_usd"].isnull().sum()
        df["salary_in_usd"] = df["salary_in_usd"].fillna(median_salary)
        if n_missing > 0:
            print(f"  Filled {n_missing} missing salaries with median (${median_salary:,.0f}).")

    if "company_size" in df.columns:
        mode_size = df["company_size"].mode().iloc[0]
        n_missing = df["company_size"].isnull().sum()
        df["company_size"] = df["company_size"].fillna(mode_size)
        if n_missing > 0:
            print(f"  Filled {n_missing} missing company sizes with mode ({mode_size}).")

    if "work_setting" in df.columns:
        n_missing = df["work_setting"].isnull().sum()
        if n_missing > 0:
            mode_ws = df["work_setting"].mode().iloc[0]
            df["work_setting"] = df["work_setting"].fillna(mode_ws)
            print(f"  Filled {n_missing} missing work settings with mode ({mode_ws}).")

    exp_map = {"EN": "Entry-level", "MI": "Mid-level", "SE": "Senior", "EX": "Executive"}
    if "experience_level" in df.columns:
        mapped = df["experience_level"].map(exp_map)
        df["experience_label"] = mapped.fillna(df["experience_level"])

    emp_map = {"FT": "Full-time", "CT": "Contract", "PT": "Part-time", "FL": "Freelance"}
    if "employment_type" in df.columns:
        mapped = df["employment_type"].map(emp_map)
        df["employment_label"] = mapped.fillna(df["employment_type"])

    size_map = {"S": "Small", "M": "Medium", "L": "Large"}
    if "company_size" in df.columns:
        df["company_size_label"] = df["company_size"].map(size_map)

    print(f"  Cleaned dataset: {len(df)} records")
    return df


def clean_stock_data(df):
    print("\nCleaning stock data...")
    original_len = len(df)

    df = df.drop_duplicates(subset=["Date", "Ticker"], keep="first")
    print(f"  Removed {original_len - len(df)} duplicate records.")

    missing_close = df["Close"].isnull().sum()
    df = df.dropna(subset=["Close"])
    if missing_close > 0:
        print(f"  Dropped {missing_close} rows with missing Close price.")

    df["Date"] = pd.to_datetime(df["Date"])
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["YearMonth"] = df["Date"].dt.to_period("M").astype(str)

    df = df.sort_values(["Ticker", "Date"])
    df["Daily_Return"] = df.groupby("Ticker")["Close"].pct_change()

    df["MA_30"] = df.groupby("Ticker")["Close"].transform(
        lambda x: x.rolling(window=30, min_periods=1).mean()
    )

    print(f"  Cleaned dataset: {len(df)} records")
    return df


def generate_summary_statistics(df, dataset_name):
    print(f"\n{'='*60}")
    print(f"SUMMARY STATISTICS: {dataset_name}")
    print(f"{'='*60}")

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        stats = df[numeric_cols].describe()
        print(stats.to_string())
        return stats
    else:
        print("  No numerical columns found.")
        return None
