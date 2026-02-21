def strategist_agent(signal, client):
    prompt = f"""
    You are Growth Strategist for DataVex.

    From this signal:
    {signal}

    Create the strongest positioning angle.
    Should we:
    - Educate?
    - Warn?
    - Compete?
    - Thought leadership?

    Give final strategic angle.
    """

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3.1-8b"
    )

    return response.choices[0].message.content