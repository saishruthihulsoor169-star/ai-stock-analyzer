import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ai_report(stock, change):

    prompt = f"""
    Analyze stock {stock}.

    Price change: {change}%

    Give:
    - Trend (UP/DOWN)
    - Sentiment (Positive/Negative/Neutral)
    - Recommendation (Buy/Sell/Hold)
    - Confidence %
    - Short explanation
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception:
        # 🔥 FALLBACK (IMPORTANT)
        if change > 1:
            return f"""
Trend: UP 📈  
Sentiment: Positive 😊  
Recommendation: Buy  
Confidence: 70%  
Reason: Strong upward momentum detected.
"""
        elif change < -1:
            return f"""
Trend: DOWN 📉  
Sentiment: Negative 😟  
Recommendation: Sell  
Confidence: 70%  
Reason: Continuous decline in price.
"""
        else:
            return f"""
Trend: Sideways ➡️  
Sentiment: Neutral 😐  
Recommendation: Hold  
Confidence: 60%  
Reason: No strong movement.
"""
