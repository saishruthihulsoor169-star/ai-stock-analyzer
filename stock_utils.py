import yfinance as yf
import pandas as pd


def get_stock_data(symbol):
    data = yf.download(symbol, period="3mo")

    # 🔥 Fix: ensure clean dataframe
    if data.empty:
        return None

    # Sometimes columns are multi-index
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data


def analyze_stock(data):
    if data is None or data.empty:
        return None

    close = data["Close"]

    # 🔥 FIX: force scalar values
    start = float(close.values[0])
    end = float(close.values[-1])

    change = ((end - start) / start) * 100

    trend = "UP 📈" if change > 0 else "DOWN 📉"

    score = round(change / 10, 2)

    if score > 0:
        sentiment = "Positive 😊"
        recommendation = "BUY"
    elif score < 0:
        sentiment = "Negative 😐"
        recommendation = "SELL"
    else:
        sentiment = "Neutral 😶"
        recommendation = "HOLD"

    confidence = min(abs(score) * 10, 95)

    return {
        "trend": trend,
        "change": round(change, 2),
        "sentiment": sentiment,
        "score": score,
        "recommendation": recommendation,
        "confidence": round(confidence, 2)
    }


def get_news(symbol):
    return [
        f"{symbol} reacting to market trends",
        f"Analysts discuss {symbol} outlook",
        f"{symbol} influenced by global economy",
        f"Investors tracking {symbol} performance"
    ]
