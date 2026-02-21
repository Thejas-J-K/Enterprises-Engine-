def writer_agent(signal, brand_voice, client):
    prompt = f"""
    Using this brand voice:
    {brand_voice}
    
    Create:
    1. LinkedIn Post
    2. Twitter Thread
    3. Short Blog
    
    Based on this signal:
    {signal}
    """

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3.1-8b"
    )

    return response.choices[0].message.content