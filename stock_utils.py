import yfinance as yf
import pandas as pd


def get_stock_data(symbol):
    try:
        symbol = symbol.strip().upper()

        data = yf.download(symbol, period="6mo", progress=False)

        # Retry once if empty (important fix)
        if data is None or data.empty:
            data = yf.download(symbol, period="1mo", progress=False)

        if data is None or data.empty:
            return None

        # Flatten columns
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        # Force correct column name
        data.columns = [col.capitalize() for col in data.columns]

        if "Close" not in data.columns:
            return None

        return data

    except Exception as e:
        print("Error:", e)
        return None


def calculate_change(data):
    close = data["Close"].dropna()

    if len(close) < 2:
        return 0

    start = float(close.iloc[0])
    end = float(close.iloc[-1])

    return round(((end - start) / start) * 100, 2)
