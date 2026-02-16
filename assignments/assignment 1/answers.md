# Assignment 1 - Answers to All Questions
## AI Labor Markets Theme | AI 620: Data Engineering for AI Systems
**Taimour Abdul Karim — 24280047**

---

## Part 1 Questions

### (a) Data Heterogeneity

Our pipeline uses three data sources and each one is a different type of data:

1. **Structured Data - AI Jobs Dataset (Kaggle):** This is a tabular dataset with columns like work_year, experience_level, employment_type, job_title, salary_in_usd, etc. Every row has the same columns and the data types are consistent like integers for year and floats for salary. This is structured data that could be loaded directly into a database.

2. **Semi-structured Data - HackerNews Stories (Algolia API):** The HackerNews data has both structured fields like points and num_comments (which are numbers) and unstructured text fields like title and story_text. The JSON response has variable length text content. Some stories have text, some are just links with no text. So it is semi-structured because it has a schema but the content within the fields varies a lot.

3. **Time-series Data - Stock Prices (yfinance):** The Yahoo Finance data gives us numerical data (Open, High, Low, Close, Volume) that is organized by date and ticker symbol. It is structured but different from the jobs data because the ordering of dates matters and there are natural gaps on weekends and holidays.

Examples from our data:
- Structured: `{"work_year": 2023, "experience_level": "Senior", "salary_in_usd": 175000}`
- Semi-structured: `{"title": "Is the AI job market oversaturated?", "story_text": "I've been applying for 6 months...", "points": 342}`
- Time-series: `{"Date": "2024-06-15", "Ticker": "NVDA", "Close": 135.58, "Volume": 437261200}`

### (b) Extraction Challenges

There were several challenges during data extraction:

1. **Duplicate Results from HackerNews API:** When we searched for different queries like "AI jobs" and "ML engineer hiring", some of the same stories came up in both results. We fixed this by using story_id as a key in a dictionary so each story only appears once.

2. **Rate Limiting:** Both the HackerNews API and yfinance can block you if you make too many requests too fast. We added a 0.5 second delay between API calls to avoid this.

3. **Different Date Formats:** HackerNews gives ISO 8601 timestamps, yfinance gives timezone-aware datetime objects, and the Kaggle dataset just has integer years. We had to convert all of these to a consistent datetime format in each extraction script.

4. **Missing Data:** Some HackerNews stories have no text (they are just links), some have missing URLs or missing point counts. The Kaggle dataset had missing values for salary, company size, and work setting. Stock data has gaps on non-trading days. Each of these needed different handling.

5. **Kaggle Dataset Access:** The Kaggle API needs an authentication token and the kaggle package installed. As an alternative our pipeline also supports just downloading the CSV manually and putting it in the data/raw/ folder.

### (c) Storage Justification

We store data in multiple formats because each format has different advantages:

**CSV:**
- Works with almost everything like Excel, databases, and all programming languages
- Easy to read in a text editor
- Good for structured tabular data
- Best when sharing with people who use spreadsheets or when you want simplicity

**JSON:**
- Can handle nested and hierarchical data that CSV cannot
- Field names are included in every record so it is self-describing
- Good for semi-structured data like API responses
- Better at preserving data types (can tell the difference between null and empty string)
- Best when data has nested structures or when feeding data to web applications

**When to use which:**
- Use CSV for tabular analysis like the AI jobs salary dataset
- Use JSON for data with mixed types like HackerNews stories with variable text
- In our pipeline we save both so that different users can use whichever format works best for them

---

## Part 2 Questions

### (a) Cleaning Rationale

Here is why we made each cleaning decision:

1. **Missing Salary Values (Median Imputation):** We filled missing salaries with the median instead of the mean. The median is better because very high executive salaries would pull the mean up and make the imputed values too high. We did not want to drop these rows because the other columns like experience level and job title were still useful.

2. **Missing Company Size (Mode Imputation):** We filled missing company sizes with the mode which is the most common value. Since company size is a category (Small, Medium, Large) we cannot use mean or median. The mode is the best option for categorical data.

3. **Missing Work Setting (Mode Imputation):** We filled missing work setting values with the mode for the same reason as company size. Work setting is also categorical with values like In-person, Remote, and Hybrid so mode imputation makes the most sense.

4. **Duplicate Removal:** We removed exact duplicate rows from the AI jobs dataset using drop_duplicates(). Keeping duplicates would mess up frequency counts and make our analysis inaccurate.

5. **Date Standardization:** We converted all dates to pandas datetime objects using to_datetime() so we could do things like sorting by date, grouping by month or year, and making time-series plots. The different date formats from HackerNews and yfinance both needed to be normalized.

### (b) Visualization Insights

**Temporal Analysis (Stock Prices):**
- NVIDIA had the most growth among all five AI companies, going from around $60 in 2020 to over $700 by 2025 because of the demand for GPUs for AI training.
- All five companies showed upward trends that got faster around 2023 when ChatGPT came out.
- Trading volume went up during major AI news events.

**Categorical Analysis (Job Distribution):**
- Senior-level positions make up the biggest share at around 64%, which means the AI field needs mostly experienced workers.
- Data Engineer and Data Scientist are the most common job titles with around 1,100 and 1,039 listings each.
- In-person work is the most common at about 54.5% but remote work is also significant at around 42%. Hybrid is only about 3.5%.

**Correlation Analysis (Salary Patterns):**
- There is a clear relationship between experience level and salary where each level gets about $40-60K more than the one below it.
- All the AI stocks are positively correlated which means they tend to go up and down together.
- The salary growth from 2020-2025 lines up with the stock price growth which suggests the AI boom is driving both.

### (c) Visualization Critique

**Current Limitations:**

1. The stock price chart shows raw closing prices which makes it hard to compare companies fairly. NVIDIA at $700 versus Amazon at $200 does not mean NVIDIA performed better in percentage terms. A normalized view where all start at 100 would be better.

2. The HackerNews data might be skewed toward popular or recent stories because of how the Algolia search API ranks results. A more complete historical dataset would give stronger conclusions.

3. The plots are static matplotlib images that you cannot interact with. Using something like Plotly or Tableau would let users hover over data points and filter.

**Improvements for Different Audiences:**

- **Technical stakeholders:** Add confidence intervals, significance tests, and log-scale options for stock prices.
- **Business stakeholders:** Simplify the charts, add annotations with key takeaways like "Remote AI roles grew 25% year over year", and use dollar-formatted axes.
- **General improvements:** Use Plotly for interactive dashboards, add filters for date ranges, and compare AI salaries to overall tech salaries.
