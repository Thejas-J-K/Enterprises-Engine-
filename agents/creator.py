from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def creator_agent(signal, strategy):

    prompt = f"""
    Write a high-authority blog for DataVex.

    Signal:
    {signal}

    Strategy:
    {strategy}

    Maintain professional enterprise tone.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    blog = response.text

    return blog