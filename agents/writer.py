def writer_agent(signal, brand_voice, client):
    prompt = f"""
    Using this Brand Voice: {brand_voice}
    
    You are a Senior Content Engineer at DataVex. 
    Tone: Authoritative, Technical, and No-nonsense.
    Keywords to use: 'Scalable', 'Full-stack', 'Enterprise-grade', 'Predictive Analytics'.

    Create:
    1. LINKEDIN: Professional insight for global CXOs.
    2. TWITTER: 4-post thread focusing on technical depth.
    3. SHORT BLOG: A deep dive into how DataVex solves the challenge in the signal.

    SIGNAL: {signal}
    """

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3.1-8b"
    )

    return response.choices[0].message.content