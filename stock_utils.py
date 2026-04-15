import yfinance as yf
import pandas as pd


def get_stock_data(symbol):
    data = yf.download(symbol, period="6mo")

    if data.empty:
        return None

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data


def calculate_change(data):
    close = data["Close"].dropna()

    start = float(close.values[0])
    end = float(close.values[-1])

    return round(((end - start) / start) * 100, 2)
