import pandas as pd
import yfinance as yf

from config import AI_TICKERS, STOCK_START_DATE, STOCK_END_DATE


def extract_stock_data(tickers=None, start=None, end=None):
    tickers = tickers or AI_TICKERS
    start = start or STOCK_START_DATE
    end = end or STOCK_END_DATE

    all_data = []

    for ticker in tickers:
        print(f"  Fetching {ticker} stock data...")
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start, end=end)

            if hist.empty:
                print(f"  Warning: No data returned for {ticker}")
                continue

            hist = hist.reset_index()
            hist["Ticker"] = ticker

            if hasattr(hist["Date"].dtype, "tz") and hist["Date"].dtype.tz is not None:
                hist["Date"] = hist["Date"].dt.tz_localize(None)

            cols = ["Date", "Open", "High", "Low", "Close", "Volume", "Ticker"]
            hist = hist[[c for c in cols if c in hist.columns]]
            all_data.append(hist)

        except Exception as e:
            print(f"  Error fetching {ticker}: {e}")

    if not all_data:
        raise RuntimeError(
            "Failed to fetch stock data for any ticker. "
            "Check your internet connection and try again."
        )

    df = pd.concat(all_data, ignore_index=True)
    print(f"  Extracted {len(df)} stock records for {len(all_data)} tickers.")
    return df
