def brain_agent(signal, client):
    prompt = f"""
    You are the DataVex Intelligence Brain. 
    Our mission: Pioneering the intersection of AI, Cloud, and Digital Transformation.

    Analyze this signal: {signal}

    1. RELEVANCE: Does this impact PropTech, FinTech, or Enterprise Cloud (AWS/GCP/Azure)?
    2. TRUTH: Is this a mission-critical technical update or generic gossip?
    3. STRATEGIC VALUE: Can we link this to our flagship solutions like AI-Powered PropTech or Automated Financial Analysis?

    OUTPUT:
    - Decision: [APPROVED or REJECTED]
    - Information Arbitrage: How can DataVex add value to this news?
    - Alignment Score: (0-100)
    """
    # ... rest of your Cerebras code ...
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3.1-8b"
    )

    return response.choices[0].message.content