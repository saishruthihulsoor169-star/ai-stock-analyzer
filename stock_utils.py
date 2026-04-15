import yfinance as yf
import requests

def get_stock_data(symbol):
    try:
        df = yf.download(symbol, period="6mo")
        if df.empty:
            return None
        return df
    except:
        return None


def analyze_stock(df):
    close = df["Close"]

    start = float(close.iloc[0])
    end = float(close.iloc[-1])

    change = ((end - start) / start) * 100

    trend = "UP 📈" if change > 0 else "DOWN 📉"

    return {
        "trend": trend,
        "change": change
    }


def get_news(stock):
    url = f"https://newsapi.org/v2/everything?q={stock}&apiKey={requests.utils.quote('YOUR_NEWS_API_KEY')}"

    try:
        res = requests.get(url).json()
        articles = res.get("articles", [])[:5]

        return [a["title"] for a in articles]
    except:
        return ["No news available"]
