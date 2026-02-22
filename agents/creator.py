from google import genai
import os

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def creator_agent(signal, strategy):
    """
    Generates structured enterprise-grade blog content
    for DataVex based on selected news signal and strategy.
    """

    prompt = f"""
You are a senior enterprise technology strategist writing for DataVex AI.

Your task:
Transform the provided news signal and strategic framing into a
high-authority, executive-level thought leadership blog.

---------------------------------------
News Signal:
{signal}

Strategic Framing:
{strategy}
---------------------------------------

STRICT REQUIREMENTS:

1. Create a compelling enterprise-level headline.
2. Add a short contextual subheading referencing the news.
3. Provide strategic analysis (not summary).
4. Include 2–3 technical deep-dive sections:
   - Infrastructure implications
   - Cost / scalability challenges
   - Security / orchestration layer
5. Clearly position DataVex as the strategic solution.
6. Mention relevant enterprise technologies where appropriate:
   (Kubernetes, containerization, FastAPI, hybrid cloud,
    AI scalability, infrastructure resilience, zero-trust security)
7. Include a strong executive conclusion.
8. End with a Source Citation section referencing the signal.

Tone Guidelines:
- Executive-level
- Analytical
- Infrastructure-first
- Confident
- No emojis
- No hype marketing language
- No casual tone

Length: 800–1200 words minimum.
Structure with clear section headings.
"""

    try:
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=prompt
        )

        blog = response.text

        if not blog or len(blog.strip()) < 200:
            raise ValueError("Generated blog too short.")

        return blog

    except Exception as e:
        # Graceful fallback (enterprise tone)
        return f"""
The Strategic Imperative of Enterprise AI Infrastructure

As enterprises scale artificial intelligence workloads, infrastructure
resilience, cost control, and architectural flexibility become non-negotiable.

DataVex specializes in architecting hybrid, scalable, and secure AI
infrastructure solutions that ensure measurable business impact.

(Source generation temporarily limited. Fallback enterprise summary displayed.)
Error: {str(e)}
"""