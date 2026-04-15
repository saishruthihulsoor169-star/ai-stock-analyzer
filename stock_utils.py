import yfinance as yf
import pandas as pd

# Fetch stock data
def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period="6mo")

        # DEBUG (important)
        print("DATA:", df.head())

        if df is None or df.empty:
            return None

        return df

    except Exception as e:
        print("ERROR:", e)
        return None


# Calculate % change
def calculate_change(df):
    try:
        close = df["Close"]

        start = float(close.iloc[0])
        end = float(close.iloc[-1])

        change = ((end - start) / start) * 100

        return round(change, 2)

    except:
        return 0
