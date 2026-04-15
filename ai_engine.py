import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_ai_report(stock, change):
    prompt = f"""
    Analyze stock {stock}.

    Change: {change}%

    STRICT FORMAT:

    Trend: UP/DOWN
    Sentiment: Positive/Neutral/Negative
    Recommendation: BUY/SELL/HOLD
    Confidence: number%
    Explanation: 2 lines only
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
