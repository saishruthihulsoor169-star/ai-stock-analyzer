import yfinance as yf


def get_stock_data(symbol):
    try:
        data = yf.download(symbol, period="6mo", interval="1d")

        if data.empty:
            return None

        data.reset_index(inplace=True)
        return data

    except Exception as e:
        print("Error:", e)
        return None


def analyze_stock(data):
    try:
        close_prices = data["Close"].values  # ✅ FIXED

        start_price = float(close_prices[0])
        end_price = float(close_prices[-1])

        change = ((end_price - start_price) / start_price) * 100

        # 🔹 Trend logic
        if change > 2:
            trend = "Strong Uptrend 📈"
            recommendation = "BUY 🟢"
            sentiment = "Positive"
        elif change > 0:
            trend = "Mild Uptrend 📊"
            recommendation = "HOLD 🟡"
            sentiment = "Slightly Positive"
        elif change > -2:
            trend = "Sideways / Weak 📉"
            recommendation = "HOLD 🟡"
            sentiment = "Neutral"
        else:
            trend = "Strong Downtrend 📉"
            recommendation = "SELL 🔴"
            sentiment = "Negative"

        explanation = f"""
Stock moved from ₹{round(start_price,2)} → ₹{round(end_price,2)}  
Change: {round(change,2)}%

Trend: {trend}  
Market Sentiment: {sentiment}  

AI Suggestion: {recommendation}
"""

        return {
            "trend": trend,
            "change": f"{round(change,2)}%",
            "recommendation": recommendation,
            "sentiment": sentiment,
            "explanation": explanation,
        }

    except Exception as e:
        return {
            "trend": "Error",
            "change": "0%",
            "recommendation": "N/A",
            "sentiment": "Unknown",
            "explanation": str(e),
        }
