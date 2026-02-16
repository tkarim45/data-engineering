# Assignment 1 - Summary Report
## AI Labor Markets: ELT Pipeline
### AI 620: Data Engineering for AI Systems
**Taimour Abdul Karim — 24280047**

---

## Thematic Focus

This project is about the AI Labor Markets domain. We are looking at job trends, salary patterns, and economic indicators related to the artificial intelligence industry. This theme was chosen because there is a lot of data available from different types of sources and it is relevant to data engineering.

## Pipeline Architecture

We built an ELT pipeline in Python that extracts data from three different sources:

1. **HackerNews API (Algolia):** We collected stories and discussions from HackerNews about AI careers and job trends. This gives us semi-structured text data.
2. **Public Dataset (Kaggle):** We used the "Jobs in Data" dataset from Kaggle which has salary data, experience levels, employment types, and company information. This is structured tabular data.
3. **Yahoo Finance (yfinance):** We got daily stock prices for five major AI companies (NVDA, MSFT, GOOG, META, AMZN) from 2020 to 2025. This is time-series financial data.

The data goes through three phases: Extract (Python scripts pull data from sources) then Load (save as raw CSV and processed CSV/JSON) then Transform (quality assessment, cleaning, and feature engineering).

## Key Findings

- AI salaries have been growing from 2020 to 2025, with senior and executive positions getting $150K to $350K+ USD.
- Remote work is common in AI jobs. About 42% of AI jobs are remote which is higher than the general job market.
- AI company stock prices have been going up a lot especially NVIDIA which correlates with the rising demand for AI talent.
- Most job listings are for senior-level positions and there are not many entry-level roles available.

## Challenges Encountered

- The HackerNews API returned duplicate results across different search queries so we had to deduplicate by story_id. Some stories did not have text content.
- The three data sources had different date formats (ISO timestamps, timezone-aware datetimes, and integer years) so we had to standardize them.
- The AI jobs dataset had 4,014 duplicate records (42.9%) that needed to be removed. Missing categorical values were filled using mode imputation.
- It was challenging to combine insights from three different types of data (text, tabular, time-series) into one coherent analysis.
