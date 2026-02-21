def strategist_agent(signal, client):
    prompt = f"""
    You are the DataVex Growth Strategist. We focus on 'Research-backed Innovation.'
    
    SIGNAL: {signal}

    Choose the strongest positioning angle for DataVex:
    - THE PROPTECH ANGLE: Use if news involves real estate or automation.
    - THE ZERO-TRUST ANGLE: Use if news involves security or cloud infrastructure.
    - THE ROI ANGLE: Focus on reducing operational costs and improving efficiency.
    
    Provide a 'Strategy Brief' explaining why this angle helps DataVex grow.
    """
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3.1-8b"
    )

    return response.choices[0].message.content