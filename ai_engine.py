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

    Keep it clean and professional.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI Error: {e}"
