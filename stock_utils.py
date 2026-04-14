import yfinance as yf
import pandas as pd

def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period="6mo")

        if df.empty:
            return None

        latest = df.iloc[-1]
        prev = df.iloc[-2]

        change = ((latest["Close"] - prev["Close"]) / prev["Close"]) * 100

        trend = "UP 📈" if change > 0 else "DOWN 📉"

        return {
            "data": df,
            "price": round(latest["Close"], 2),
            "change": round(change, 2),
            "trend": trend
        }

    except:
        return None
