import yfinance as yf
import matplotlib.pyplot as plt

def analyze_stock(stock_name):
    stock = yf.Ticker(stock_name)
    data = stock.history(period="3mo")

    latest = data['Close'].iloc[-1]
    avg = data['Close'].mean()

    trend = "UP 📈" if latest > avg else "DOWN 📉"

    news = stock.news
    headlines = [n.get('content', {}).get('title', '') for n in news[:5]]

    # Save chart
    plt.figure(figsize=(8, 4))
    plt.plot(data['Close'])
    plt.title("Stock Price Trend")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.savefig("chart.png")
    plt.close()

    return data, trend, headlines