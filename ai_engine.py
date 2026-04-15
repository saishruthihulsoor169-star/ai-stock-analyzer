import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ai_report(stock, change):
    prompt = f"""
    Analyze stock {stock}.

    Change: {change}%

    Give output STRICTLY in this format:

    Trend: ...
    Sentiment: ...
    Recommendation: ...
    Confidence: ...%
    Explanation: (2 lines)
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content