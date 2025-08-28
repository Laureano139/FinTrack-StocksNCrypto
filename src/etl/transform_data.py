import pandas as pd
import os

"""
Loads, transforms and saves historical data
"""
def transform_historical_data(ticker_symbol):
    raw_dir = "data/raw"
    processed_dir = "data/processed"
    os.makedirs(processed_dir, exist_ok=True)

    file_path_raw = os.path.join(raw_dir, f"{ticker_symbol}_historical_data.csv")
    file_path_processed = os.path.join(processed_dir, f"{ticker_symbol}_historical_processed.csv")

    try:
        df = pd.read_csv(file_path_raw, index_col='Date')
        
        df.index = pd.to_datetime(df.index, errors='coerce', utc=True)
        df = df[df.index.notna()]
        
        if df.index.tz is not None:
             df.index = df.index.tz_convert(None)
        
        df['Ticker'] = ticker_symbol

        df['year'] = df.index.year
        df['month'] = df.index.month
        df['weekday'] = df.index.day_name()

        price_cols = ['Open', 'High', 'Low', 'Close']
        df[price_cols] = df[price_cols].astype(float)
        
        df['Volume'] = df['Volume'].astype('int64')

        df[['Dividends', 'Stock Splits']] = df[['Dividends', 'Stock Splits']].fillna(0.0)

        df.to_csv(file_path_processed)
        print(f"Historical data transformed and saved in: {file_path_processed}")

    except FileNotFoundError:
        print(f"Error: The file '{file_path_raw}' was not found. Please run 'fetch_data.py' first.")


"""
Loads, transforms and saves financial data
"""
def transform_financial_data(ticker_symbol):
    raw_dir = "data/raw"
    processed_dir = "data/processed"
    os.makedirs(processed_dir, exist_ok=True)

    file_path_raw = os.path.join(raw_dir, f"{ticker_symbol}_financials.csv")
    file_path_processed = os.path.join(processed_dir, f"{ticker_symbol}_financials_processed.csv")

    try:
        df = pd.read_csv(file_path_raw) 

        df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
        df.set_index('Date', inplace=True)
        
        df.index = pd.to_datetime(df.index, errors='coerce', format='%Y-%m-%d')
        df = df[df.index.notna()]
        
        df['Ticker'] = ticker_symbol

        df = df.fillna(0)

        df.to_csv(file_path_processed)
        print(f"Financial data transformed and saved in: {file_path_processed}")

    except FileNotFoundError:
        print(f"Error: The file '{file_path_raw}' was not found.")


"""
Loads, transforms and saves stock data
"""
def transform_actions_data(ticker_symbol):
    raw_dir = "data/raw"
    processed_dir = "data/processed"
    os.makedirs(processed_dir, exist_ok=True)

    file_path_raw = os.path.join(raw_dir, f"{ticker_symbol}_actions.csv")
    file_path_processed = os.path.join(processed_dir, f"{ticker_symbol}_actions_processed.csv")

    try:
        df = pd.read_csv(file_path_raw, index_col='Date')
        
        df.index = pd.to_datetime(df.index, errors='coerce', utc=True)
        df = df[df.index.notna()]
        
        if df.index.tz is not None:
             df.index = df.index.tz_convert(None)
        
        df['Ticker'] = ticker_symbol
        
        df[['Dividends', 'Stock Splits']] = df[['Dividends', 'Stock Splits']].fillna(0.0)

        df.to_csv(file_path_processed)
        print(f"Stock data transformed and saved in: {file_path_processed}")

    except FileNotFoundError:
        print(f"Error: The file '{file_path_raw}' was not found.")


if __name__ == "__main__":
    tickers = ["AAPL", "GOOGL", "MSFT"]
    
    for ticker in tickers:
        transform_historical_data(ticker)
        transform_financial_data(ticker)
        transform_actions_data(ticker)