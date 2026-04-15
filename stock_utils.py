import yfinance as yf
import pandas as pd


def get_stock_data(symbol):
    try:
        data = yf.download(symbol.strip().upper(), period="6mo", progress=False)

        if data is None or data.empty:
            return None

        # Fix multi-index issue
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        # Ensure Close exists
        if "Close" not in data.columns:
            return None

        return data

    except Exception:
        return None


def calculate_change(data):
    close = data["Close"].dropna()

    if len(close) < 2:
        return 0

    start = float(close.iloc[0])
    end = float(close.iloc[-1])

    return round(((end - start) / start) * 100, 2)
