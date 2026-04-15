def generate_ai_report(stock, change):

    if change > 2:
        return f"""
Trend: UP 📈  
Sentiment: Positive 😊  
Recommendation: BUY  
Confidence: 70%  
Reason: Strong upward movement in price.
"""

    elif change < -2:
        return f"""
Trend: DOWN 📉  
Sentiment: Negative 😟  
Recommendation: SELL  
Confidence: 70%  
Reason: Continuous decline in stock.
"""

    else:
        return f"""
Trend: Sideways ➡️  
Sentiment: Neutral 😐  
Recommendation: HOLD  
Confidence: 60%  
Reason: No strong trend observed.
"""
