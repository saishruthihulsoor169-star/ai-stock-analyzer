import yfinance as yf
import requests

def get_stock_data(symbol):
    try:
        df = yf.download(symbol, period="6mo")

        if df is None or df.empty:
            return None

        # 🔥 IMPORTANT FIX
        df = df.dropna()

        return df

    except Exception as e:
        print("Stock fetch error:", e)
        return None


def analyze_stock(df):
    close = df["Close"].dropna()

    # 🔥 SAFETY CHECK
    if len(close) < 2:
        return {
            "trend": "N/A",
            "change": 0
        }

    start = float(close.iloc[0])
    end = float(close.iloc[-1])

    change = ((end - start) / start) * 100

    trend = "UP 📈" if change > 0 else "DOWN 📉"

    return {
        "trend": trend,
        "change": change
    }


def get_news(stock):
    try:
        url = f"https://newsapi.org/v2/everything?q={stock}&apiKey=YOUR_NEWS_API_KEY"
        res = requests.get(url).json()

        articles = res.get("articles", [])[:5]

        return [a["title"] for a in articles]

    except:
        return ["No news available"]
