import yfinance as yf
import pandas as pd
import os

# ticker_symbol = "AAPL"
# ticker = yf.Ticker(ticker_symbol)

# Geeks4Geeks example

# historical_data = ticker.history(period="1y")
# print("Historical Data:")
# print(historical_data)

# financials = ticker.financials
# print("\nFinancials:")
# print(financials)

# actions = ticker.actions
# print("\nStock Actions:")
# print(actions)

def fetch_and_save_data(ticker_list, raw_dir):
    os.makedirs(raw_dir, exist_ok=True)
    
    for ticker_symbol in ticker_list:
        print(f"Searching for data --> {ticker_symbol}...")
        ticker = yf.Ticker(ticker_symbol)

        historical_data = ticker.history(period="5y")
        file_path_hist = os.path.join(raw_dir, f"{ticker_symbol}_historical_data.csv")
        historical_data.to_csv(file_path_hist)

        financials = ticker.financials.T
        file_path_fin = os.path.join(raw_dir, f"{ticker_symbol}_financials.csv")
        financials.to_csv(file_path_fin)

        actions = ticker.actions
        file_path_act = os.path.join(raw_dir, f"{ticker_symbol}_actions.csv")
        actions.to_csv(file_path_act)

if __name__ == "__main__":
    tickers = ["AAPL", "GOOGL", "MSFT"]
    raw_data_dir = "data/raw"
    fetch_and_save_data(tickers, raw_data_dir)