import yfinance as yf
import pandas as pd


# 🔹 Fetch stock data
def get_stock_data(symbol):
    try:
        data = yf.download(symbol, period="6mo", interval="1d")

        if data.empty:
            return None

        data.reset_index(inplace=True)
        return data

    except Exception as e:
        print("Error fetching stock:", e)
        return None


# 🔹 Analyze stock
def analyze_stock(data):
    try:
        # Ensure proper values (NOT series comparison)
        start_price = float(data["Close"].iloc[0])
        end_price = float(data["Close"].iloc[-1])

        change = ((end_price - start_price) / start_price) * 100

        trend = "UP 📈" if change > 0 else "DOWN 📉"
        recommendation = "BUY 🟢" if change > 0 else "SELL 🔴"

        return {
            "trend": trend,
            "change": f"{round(change, 2)}%",
            "recommendation": recommendation,
            "start_price": round(start_price, 2),
            "end_price": round(end_price, 2),
            "news": [
                "Market reacting to global events",
                "Stock influenced by economic trends",
                "Investors showing mixed sentiment"
            ]
        }

    except Exception as e:
        return {
            "trend": "Error",
            "change": "0%",
            "recommendation": "N/A",
            "start_price": 0,
            "end_price": 0,
            "news": [str(e)]
        }


# 🔹 Extra metrics (for portfolio UI)
def get_metrics(data):
    try:
        latest = data.iloc[-1]

        return {
            "Open": round(float(latest["Open"]), 2),
            "High": round(float(latest["High"]), 2),
            "Low": round(float(latest["Low"]), 2),
            "Close": round(float(latest["Close"]), 2),
            "Volume": int(latest["Volume"])
        }

    except:
        return {}
