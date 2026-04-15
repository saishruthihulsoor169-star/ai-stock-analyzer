import yfinance as yf
import pandas as pd


def get_stock_data(symbol):
    data = yf.download(symbol, period="3mo")

    if data.empty:
        return None

    # Fix multi-index issue
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data


def analyze_stock(data):
    close = data["Close"].dropna()

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
        f"{symbol} sees movement due to earnings impact",
        f"Market sentiment shifts around {symbol}",
        f"Analysts discuss future growth of {symbol}",
        f"{symbol} influenced by global tech trends"
    ]
