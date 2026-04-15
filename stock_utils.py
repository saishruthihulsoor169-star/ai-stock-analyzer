import yfinance as yf

def get_stock_data(symbol):
    try:
        data = yf.download(symbol, period="6mo", interval="1d")
        return data
    except:
        return None

def analyze_stock(data):
    change = ((data["Close"].iloc[-1] - data["Close"].iloc[0]) / data["Close"].iloc[0]) * 100

    trend = "UP 📈" if change > 0 else "DOWN 📉"
    recommendation = "BUY 🟢" if change > 0 else "SELL 🔴"

    news = [
        "Market reacting to global events",
        "Stock influenced by economic trends",
        "Investors showing mixed sentiment"
    ]

    return {
        "trend": trend,
        "change": f"{round(change,2)}%",
        "recommendation": recommendation,
        "news": news
    }
