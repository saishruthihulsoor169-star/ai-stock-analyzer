import yfinance as yf
import requests
import os

def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period="6mo")

        if df is None or df.empty:
            return None

        df = df.reset_index()
        return df

    except:
        return None


def analyze_stock(df):
    close = df["Close"]

    start = float(close.iloc[0])
    end = float(close.iloc[-1])

    change = ((end - start) / start) * 100
    change = round(change, 2)

    trend = "UP 📈" if change > 0 else "DOWN 📉"

    if change > 2:
        rec = "BUY"
    elif change < -2:
        rec = "SELL"
    else:
        rec = "HOLD"

    confidence = min(abs(change) * 5, 100)

    return {
        "trend": trend,
        "change": change,
        "recommendation": rec,
        "confidence": round(confidence, 2)
    }


def get_news(symbol):
    try:
        url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={os.getenv('NEWS_API_KEY')}"
        res = requests.get(url).json()

        articles = res.get("articles", [])[:5]

        return [a["title"] for a in articles]

    except:
        return ["No news available"]
