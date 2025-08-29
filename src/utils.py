import pandas as pd

"""
Simple moving average for the 'Close' column of a df
"""
def calculate_moving_average(df, window):
    if 'Close' in df.columns:
        return df['Close'].rolling(window=window).mean()
    return pd.Series(dtype='float64')

"""
Calculates the daily return percentage for the 'Close' column of a df

Daily Return = (Today's Close Price - Yesterday's Close Price) / Yesterday's Close Price
"""
def calculate_daily_return(df):
    if 'Close' in df.columns:
        price_today = df['Close']
        # Yesterday's price
        price_yesterday = df['Close'].shift(1)
        
        daily_return = ((price_today - price_yesterday) / price_yesterday) * 100
        return daily_return
    return pd.Series(dtype='float64')