def brain_agent(signal, client):
    prompt = f"""
    You are DataVex Intelligence Brain.

    Analyze this signal:
    {signal}

    1. Is this real and logically valid?
    2. Is it useful for a data infrastructure company?
    3. Give:
       - Decision: APPROVED or REJECTED
       - Information Arbitrage Score (0-100)
       - Strategic Relevance Score (0-100)
    """

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3.1-8b"
    )

    return response.choices[0].message.content