import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ai_report(stock, change):

    prompt = f"""
    Analyze stock {stock}.
    Price change: {change}%

    Give:
    - Trend
    - Sentiment
    - Recommendation
    - Confidence %
    - Short explanation
    """

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content

    except:
        if change > 1:
            return "Trend: UP 📈 | Sentiment: Positive 😊 | Recommendation: Buy | Confidence: 70%"
        elif change < -1:
            return "Trend: DOWN 📉 | Sentiment: Negative 😟 | Recommendation: Sell | Confidence: 70%"
        else:
            return "Trend: Neutral ➡️ | Recommendation: Hold"
