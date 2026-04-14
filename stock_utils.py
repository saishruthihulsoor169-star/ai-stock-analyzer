import yfinance as yf
import matplotlib.pyplot as plt
from textblob import TextBlob
import time

def analyze_stock(stock_name):
    try:
        stock = yf.Ticker(stock_name)

        # Avoid rate limit
        time.sleep(2)

        data = stock.history(period="3mo")

        if data.empty:
            return None

        latest = data['Close'].iloc[-1]
        prev = data['Close'].iloc[-2]

        change_percent = ((latest - prev) / prev) * 100

        trend = "UP 📈" if latest > data['Close'].mean() else "DOWN 📉"

        news = stock.news
        headlines = [n.get('content', {}).get('title', '') for n in news[:5]]

        sentiment_score = 0
        for h in headlines:
            if h:
                sentiment_score += TextBlob(h).sentiment.polarity

        sentiment_score = sentiment_score / len(headlines) if headlines else 0

        if sentiment_score > 0:
            sentiment_label = "Positive 😊"
        elif sentiment_score < 0:
            sentiment_label = "Negative 😟"
        else:
            sentiment_label = "Neutral 😐"

        # Chart
        plt.figure(figsize=(8, 4))
        plt.plot(data['Close'])
        plt.title(stock_name)
        plt.savefig("chart.png")
        plt.close()

        return {
            "trend": trend,
            "change": round(change_percent, 2),
            "headlines": headlines,
            "sentiment": sentiment_label,
            "sentiment_score": round(sentiment_score, 2)
        }

    except Exception as e:
        return {"error": str(e)}
