import os
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras

load_dotenv()
client = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))

def brain_agent(signal):
    prompt = f"""
    You are DataVex Intelligence Brain.
    
    Analyze this signal:
    {signal}
    
    1. Is this news logically valid?
    2. Is it useful for a data infrastructure company?
    3. Give decision: APPROVED or REJECTED
    """

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3.1-8b"
    )

    return response.choices[0].message.content