def critic_agent(content, brand_voice, client):
    prompt = f"""
    You are DataVex Brand Guardian.

    Brand Voice:
    {brand_voice}

    Review this content:
    {content}

    1. Does it match brand voice?
    2. Is it strong and authoritative?
    3. Improve it if weak.
    4. Give Brand Alignment Score (0-100).
    """

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3.1-8b"
    )

    return response.choices[0].message.content