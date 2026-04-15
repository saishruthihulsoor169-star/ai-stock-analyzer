def generate_ai_report(stock, change):

    if change > 2:
        sentiment = "Positive 😊"
        recommendation = "BUY"
    elif change < -2:
        sentiment = "Negative 😟"
        recommendation = "SELL"
    else:
        sentiment = "Neutral 😐"
        recommendation = "HOLD"

    confidence = min(abs(change) * 5, 100)

    report = f"""
### 📊 {stock} Analysis

**Trend:** {'UP 📈' if change > 0 else 'DOWN 📉'}  
**Change:** {change}%  
**Sentiment:** {sentiment}  
**Recommendation:** {recommendation}  
**Confidence:** {round(confidence,2)}%

---
"""

    return report
