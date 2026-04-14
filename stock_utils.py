import yfinance as yf
import matplotlib.pyplot as plt
from textblob import TextBlob


def analyze_stock(stock_name):
    try:
        # ---------------- FETCH DATA ----------------
        stock = yf.Ticker(stock_name)
        data = stock.history(period="3mo")

        # 🚨 Safety check
        if data.empty:
            return {"error": "No data found for this stock"}

        # ---------------- BASIC CALCULATIONS ----------------
        latest = data['Close'].iloc[-1]
        prev = data['Close'].iloc[-2] if len(data) > 1 else latest
        avg = data['Close'].mean()

        # 📈 % Change
        change_percent = ((latest - prev) / prev) * 100 if prev != 0 else 0

        # 📊 Trend
        trend = "UP 📈" if latest > avg else "DOWN 📉"

        # ---------------- NEWS + SENTIMENT ----------------
        news = stock.news if hasattr(stock, "news") else []

        headlines = []
        for n in news[:5]:
            try:
                title = n.get('content', {}).get('title', '')
                if title:
                    headlines.append(title)
            except:
                continue

        # 😊 Sentiment Analysis
        sentiment_score = 0

        for h in headlines:
            sentiment_score += TextBlob(h).sentiment.polarity

        if len(headlines) > 0:
            sentiment_score = sentiment_score / len(headlines)
        else:
            sentiment_score = 0

        if sentiment_score > 0:
            sentiment_label = "Positive 😊"
        elif sentiment_score < 0:
            sentiment_label = "Negative 😟"
        else:
            sentiment_label = "Neutral 😐"

        # ---------------- CHART ----------------
        plt.figure(figsize=(8, 4))
        plt.plot(data['Close'])
        plt.title(stock_name)
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.grid(True)
        plt.savefig("chart.png")
        plt.close()

        # ---------------- RETURN CLEAN DATA ----------------
        return {
            "trend": trend,
            "change": round(change_percent, 2),
            "headlines": headlines,
            "sentiment": sentiment_label,
            "sentiment_score": round(sentiment_score, 2)
        }

    except Exception as e:
        return {"error": str(e)}
