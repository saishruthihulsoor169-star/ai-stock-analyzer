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

        # 📈 % change
        change_percent = ((latest - prev) / prev) * 100

        # 📊 Moving averages (better trend detection)
        ma_short = data['Close'].tail(5).mean()
        ma_long = data['Close'].tail(20).mean()

        if ma_short > ma_long:
            trend = "UP 📈"
            trend_score = 1
        else:
            trend = "DOWN 📉"
            trend_score = -1

        # 📰 News
        news = stock.news
        headlines = [n.get('content', {}).get('title', '') for n in news[:5]]

        # 😊 Sentiment
        sentiment_score = 0
        for h in headlines:
            if h:
                sentiment_score += TextBlob(h).sentiment.polarity

        sentiment_score = sentiment_score / len(headlines) if headlines else 0

        if sentiment_score > 0:
            sentiment_label = "Positive 😊"
            sentiment_flag = 1
        elif sentiment_score < 0:
            sentiment_label = "Negative 😟"
            sentiment_flag = -1
        else:
            sentiment_label = "Neutral 😐"
            sentiment_flag = 0

        # 🔥 FINAL DECISION ENGINE (weighted)
        final_score = (0.7 * trend_score) + (0.3 * sentiment_flag)

        if final_score > 0:
            recommendation = "BUY 🟢"
        elif final_score < 0:
            recommendation = "SELL 🔴"
        else:
            recommendation = "HOLD ⚪"

        # 🎯 Confidence
        confidence = round(abs(final_score) * 100)

        # 📉 Chart
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
            "sentiment_score": round(sentiment_score, 2),
            "recommendation": recommendation,
            "confidence": confidence
        }

    except Exception as e:
        return {"error": str(e)}
