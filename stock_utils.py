import yfinance as yf
import requests
import pandas as pd

def get_stock_data(symbol):
    try:
        df = yf.download(symbol, period="6mo", auto_adjust=True)

        if df is None or df.empty:
            return None

        # 🔥 FIX ALL DATA ISSUES
        df = df.reset_index()

        df = df[["Date", "Close"]]

        df = df.dropna()

        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

        df = df.dropna()

        df.set_index("Date", inplace=True)

        return df

    except Exception as e:
        print("Stock fetch error:", e)
        return None


def analyze_stock(df):
    close = df["Close"]

    if len(close) < 2:
        return {"trend": "N/A", "change": 0}

    start = close.iloc[0]
    end = close.iloc[-1]

    change = ((end - start) / start) * 100

    trend = "UP 📈" if change > 0 else "DOWN 📉"

    return {
        "trend": trend,
        "change": float(change)
    }


def get_news(stock):
    try:
        url = f"https://newsapi.org/v2/everything?q={stock}&apiKey=YOUR_NEWS_API_KEY"
        res = requests.get(url).json()

        articles = res.get("articles", [])[:5]

        return [a["title"] for a in articles]

    except:
        return ["No news available"]
