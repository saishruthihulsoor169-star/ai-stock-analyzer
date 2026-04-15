import yfinance as yf
import pandas as pd
import requests
import os

# ---------- FETCH DATA ----------
def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period="6mo")

        if df is None or df.empty:
            return None

        df = df.reset_index()
        return df

    except Exception as e:
        print("ERROR:", e)
        return None


# ---------- ANALYSIS ----------
def analyze_stock(df):
    close = df["Close"]

    start = float(close.iloc[0])
    end = float(close.iloc[-1])

    change = ((end - start) / start) * 100
    change = round(change, 2)

    trend = "UP 📈" if change > 0 else "DOWN 📉"

    # Fake AI recommendation (safe & stable)
    if change > 2:
        recommendation = "BUY"
    elif change < -2:
        recommendation = "SELL"
    else:
        recommendation = "HOLD"

    confidence = min(abs(change) * 5, 100)

    return {
        "trend": trend,
        "change": change,
        "recommendation": recommendation,
        "confidence": round(confidence, 2)
    }


# ---------- NEWS ----------
def get_news(symbol):
    try:
        url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={os.getenv('NEWS_API_KEY')}"
        res = requests.get(url).json()

        articles = res.get("articles", [])[:5]

        news = []
        for a in articles:
            news.append(a["title"])

        return news

    except:
        return ["No news available"]
