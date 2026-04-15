import yfinance as yf
import pandas as pd


def get_stock_data(symbol):
    data = yf.download(symbol, period="3mo")
    return data


def analyze_stock(data):
    close = data["Close"]

    start = float(close.iloc[0])
    end = float(close.iloc[-1])

    change = ((end - start) / start) * 100

    trend = "UP 📈" if change > 0 else "DOWN 📉"

    # Fake AI sentiment (based on trend strength)
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
    # dummy realistic news (no API needed)
    return [
        f"{symbol} shows movement amid market volatility",
        f"Analysts discuss future outlook of {symbol}",
        f"Investors react to recent earnings of {symbol}",
        f"{symbol} impacted by global tech trends"
    ]
