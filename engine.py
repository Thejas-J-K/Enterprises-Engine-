import os
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras

# 1. Load your API keys
load_dotenv()
client = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))

def analyze_and_write(news_signal):
    # STEP 2: The "Brain" Agent - Fact Check & Strategy
    # We use llama3.1-8b because it is lightning fast on Cerebras
    brain_prompt = f"""
    You are the DataVex Intelligence Brain. 
    1. Verify if this news is logically sound: {news_signal}
    2. If it is high-value for a data company, write a bold LinkedIn post.
    3. Use the DataVex voice: Technical, No-nonsense, and Bold.
    """
    
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": brain_prompt}],
        model="llama3.1-8b", # Or llama-3.3-70b for more complex reasoning
    )
    
    return response.choices[0].message.content

# Test it
test_news = "Major competitor AI-Corp just leaked 50k user records due to poor database encryption."
print(analyze_and_write(test_news))