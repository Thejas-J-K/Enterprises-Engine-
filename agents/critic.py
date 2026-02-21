def critic_agent(content, brand_voice, client):
    prompt = f"""
    You are the DataVex Brand Guardian. 
    Review this draft: {content}

    Check against DataVex Standards:
    - Does it mention our end-to-end technological expertise?
    - Is the tone 'Carrier-grade' and professional? (Remove flowery adjectives like 'tapestry' or 'journey').
    - Does it highlight measurable impact?

    Provide harsh feedback to the writer if it sounds like a generic brochure.
    """

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3.1-8b"
    )

    return response.choices[0].message.content