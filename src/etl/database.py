import sqlite3
import pandas as pd
import os

def load_data_to_db(db_path, data_dir, ticker_list):
    conn = sqlite3.connect(db_path)
    print(f"Connected to the database: {db_path}")

    for ticker_symbol in ticker_list:
        files = {
            f"{ticker_symbol}_historical_processed.csv": 'historical_data',
            f"{ticker_symbol}_financials_processed.csv": 'financials',
            f"{ticker_symbol}_actions_processed.csv": 'stock_actions'
        }

        for file_name, table_name in files.items():
            file_path = os.path.join(data_dir, file_name)
            
            if os.path.exists(file_path):
                try:
                    df = pd.read_csv(file_path, index_col='Date', parse_dates=True)
                    df.to_sql(table_name, conn, if_exists='append', index=True) 
                    print(f"Data from {file_name} loaded into table '{table_name}'.")
                except Exception as e:
                    print(f"Error loading {file_name}: {e}")
            else:
                print(f"Warning: File '{file_name}' not found.")

    conn.close()
    print("Connection to the database closed.")
    

def check_database(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print(f"Connected to the database: {db_path}\n")
    
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if not tables:
            print("No tables found in the database.")
            return

        for table_name_tuple in tables:
            table_name = table_name_tuple[0]
            print(f"--- Table: {table_name} ---")

            df = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 5;", conn)
            print(df.to_string())
            print("\n")

    except sqlite3.Error as e:
        print(f"Error connecting to or querying the database: {e}")
    finally:
        if conn:
            conn.close()
            print("Connection to the database closed.")


if __name__ == "__main__":
    db_file = "fintrack.db"
    processed_data_dir = "data/processed"
    tickers = ["AAPL", "GOOGL", "MSFT"]
    
    load_data_to_db(db_file, processed_data_dir, tickers)
    check_database(db_file)