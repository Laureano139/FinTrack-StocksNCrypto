import streamlit as st
import pandas as pd
import sqlite3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils import calculate_moving_average, calculate_daily_return

@st.cache_data
def load_data_from_db(db_path, table_name, ticker_symbol=None):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    
    if 'Date' in df.columns and not df.index.name == 'Date':
        df.set_index('Date', inplace=True)
    
    df.index = pd.to_datetime(df.index, errors='coerce', utc=True)
    df = df[df.index.notna()]
    if df.index.tz is not None:
        df.index = df.index.tz_convert(None)
        
    if ticker_symbol and 'Ticker' in df.columns:
        df = df[df['Ticker'] == ticker_symbol]
    
    return df

st.set_page_config(layout="wide")
st.title("FinTrack")

db_file = "fintrack.db"

try:
    conn_tickers = sqlite3.connect(db_file)

    available_tickers_df = pd.read_sql("SELECT DISTINCT Ticker FROM historical_data", conn_tickers)
    available_tickers = available_tickers_df['Ticker'].tolist()
    conn_tickers.close()
    if not available_tickers:
        available_tickers = ["AAPL", "GOOGL", "MSFT"]
except Exception:
    available_tickers = ["AAPL", "GOOGL", "MSFT"]

st.sidebar.header("Pick the stock")
ticker_symbol = st.sidebar.selectbox("Stock Symbol:", available_tickers).upper()

if ticker_symbol:
    st.markdown(f"## Report for {ticker_symbol}")

    historical_df = load_data_from_db(db_file, 'historical_data', ticker_symbol)
    financials_df = load_data_from_db(db_file, 'financials', ticker_symbol)
    actions_df = load_data_from_db(db_file, 'stock_actions', ticker_symbol)

    if historical_df.empty:
        st.warning(f"No historical data found for ticker: {ticker_symbol}. Please run the ETL pipeline.")
    else:
        historical_df['SMA_20'] = calculate_moving_average(historical_df, 20)
        historical_df['SMA_50'] = calculate_moving_average(historical_df, 50)
        historical_df['Daily_Return'] = calculate_daily_return(historical_df)

        st.subheader("Closing price and moving average")
        st.line_chart(historical_df[['Close', 'SMA_20', 'SMA_50']])

        st.subheader("Daily return (%)")
        st.line_chart(historical_df['Daily_Return'])

        st.markdown("### Additional info")
        col1, col2 = st.columns(2)

        with col1:
            if not financials_df.empty:
                st.subheader("Last key financial metrics")
                last_financials = financials_df.iloc[-1]
                st.write(f"**Date:** {last_financials.name.strftime('%Y-%m-%d')}")

                metrics_to_show = {
                    "Total Revenue": 'Total Revenue',
                    "Net Income": 'Net Income',
                    "EBITDA": 'Normalized EBITDA',
                    "Gross Profit": 'Gross Profit'
                }
                
                for display_name, col_name in metrics_to_show.items():
                    if col_name in last_financials.index:
                        st.metric(label=display_name, value=f"{last_financials[col_name]:,.0f} €")
                    else:
                        st.write(f"- {display_name}: N/A")

            else:
                st.info(f"No financial data found for {ticker_symbol}.")

        with col2:
            if not actions_df.empty:
                st.subheader("Recent stocks (Dividends and Stock Splits)")
                st.dataframe(actions_df[['Dividends', 'Stock Splits']].tail(3))
            else:
                st.info(f"No recent stock actions found for {ticker_symbol}.")

else:
    st.info("Please select a stock symbol from the sidebar to view the report.")