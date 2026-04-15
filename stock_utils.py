import yfinance as yf


# 🔹 Fetch stock data
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


# 🔹 Analyze stock
def analyze_stock(data):
    try:
        close_prices = data["Close"]

        # ✅ Convert properly to float
        start_price = float(close_prices.iloc[0])
        end_price = float(close_prices.iloc[-1])

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
            trend = "Mild Downtrend 📉"
            recommendation = "HOLD 🟡"
            sentiment = "Slightly Negative"
        else:
            trend = "Strong Downtrend 📉"
            recommendation = "SELL 🔴"
            sentiment = "Negative"

        # 🔹 AI-style explanation
        explanation = f"""
        The stock moved from {round(start_price,2)} to {round(end_price,2)} 
        showing a {round(change,2)}% change.
        
        Current trend indicates: {trend}.
        Market sentiment appears: {sentiment}.
        
        Based on momentum, the recommendation is: {recommendation}.
        """

        return {
            "trend": trend,
            "change": f"{round(change,2)}%",
            "recommendation": recommendation,
            "sentiment": sentiment,
            "explanation": explanation,
            "start_price": round(start_price, 2),
            "end_price": round(end_price, 2),
            "news": [
                "Market reacting to macroeconomic factors",
                "Stock influenced by sector performance",
                "Investor sentiment remains dynamic"
            ]
        }

    except Exception as e:
        return {
            "trend": "Error",
            "change": "0%",
            "recommendation": "N/A",
            "sentiment": "Unknown",
            "explanation": str(e),
            "start_price": 0,
            "end_price": 0,
            "news": [str(e)]
        }


# 🔹 Extra metrics (portfolio feel)
def get_metrics(data):
    try:
        latest = data.iloc[-1]

        return {
            "Open": float(latest["Open"]),
            "High": float(latest["High"]),
            "Low": float(latest["Low"]),
            "Close": float(latest["Close"]),
            "Volume": int(latest["Volume"])
        }

    except:
        return {}
