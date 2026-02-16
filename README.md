# AI Labor Markets - ELT Pipeline
## AI 620: Data Engineering for AI Systems | Assignment 1
**Taimour Abdul Karim — 24280047**

This is an ELT (Extract-Load-Transform) pipeline that pulls data from multiple sources to analyze the AI labor market including job trends, salaries, and stock prices.

## Project Structure

```
Assignment 1/
├── config.py
├── extract_api.py
├── extract_dataset.py
├── extract_timeseries.py
├── load_data.py
├── transform.py
├── run_pipeline.py
├── analysis.ipynb
├── requirements.txt
├── .env.example
├── answers.md
├── report.md
├── data/
│   ├── raw/
│   ├── processed/
│   └── cleaned/
└── visualizations/
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download the Kaggle Dataset

Download the AI Jobs dataset from Kaggle and put the CSV file in `data/raw/`:
- Dataset: `hummaamqaasim/jobs-in-data`
- Save it as `data/raw/jobs_in_data.csv`

You can also set up the Kaggle API (`~/.kaggle/kaggle.json`) and the pipeline will download it automatically.

### 3. Run the Pipeline

```bash
python run_pipeline.py
```

This runs the full ELT pipeline:
- Extracts data from all three sources
- Saves raw data to `data/raw/`
- Saves processed data in CSV and JSON to `data/processed/`
- Cleans the data and saves to `data/cleaned/`

No API keys are needed. HackerNews and Yahoo Finance are both free.

### 4. Run the Analysis Notebook

Open `analysis.ipynb` in Jupyter for Part 2:

```bash
jupyter notebook analysis.ipynb
```

## Data Sources

| Source | Type | Library | Auth Required | Records |
|--------|------|---------|--------------|---------|
| HackerNews | Semi-structured | requests | No | ~200+ stories |
| AI Jobs Dataset | Structured | Pandas/Kaggle | Kaggle account | Varies |
| Yahoo Finance | Time-series | yfinance | No | ~7,500 records |

## Assumptions

- HackerNews data covers AI/ML job related stories from the Algolia search API
- AI Jobs dataset is from Kaggle (`hummaamqaasim/jobs-in-data`)
- Stock data covers 5 AI/tech companies: NVIDIA, Microsoft, Google, Meta, Amazon (2020-2025)
- Missing salary values are filled with median
- Missing categorical values are filled with mode
