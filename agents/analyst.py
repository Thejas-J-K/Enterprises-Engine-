import requests
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SERPER_API_KEY = os.getenv("SERPER_API_KEY")


def analyst_agent():
    """
    1. Generate dynamic enterprise-relevant search query
    2. Fetch 5 trending news articles
    3. Rank by enterprise impact + DataVex relevance
    4. Return structured output with citation
    """

    # =====================================
    # 🔹 Step 1: Generate Dynamic Query
    # =====================================
    query_prompt = """
    Generate ONE trending enterprise-level search query 
    related to AI, cloud computing, cybersecurity, or infrastructure.
    Keep it short (3-5 words).
    No explanation. Only query.
    """

    try:
        query_response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=query_prompt
        )
        query = query_response.text.strip()
    except Exception:
        query = "enterprise AI infrastructure"

    # =====================================
    # 🔹 Step 2: Fetch 5 News from Serper
    # =====================================
    url = "https://google.serper.dev/news"

    payload = {
        "q": query,
        "num": 5,
        "tbs": "qdr:12h"
        
    }

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        return None

    news_data = response.json()
    raw_news = news_data.get("news", [])

    if not raw_news:
        return None

    # Structure news properly
    news_list = []

    for item in raw_news:
        news_list.append({
            "title": item.get("title"),
            "source": item.get("source"),
            "url": item.get("link"),
            "published_at": item.get("date")
        })

    # =====================================
    # 🔹 Step 3: Rank News with Gemini
    # =====================================
    formatted_news = "\n".join([
        f"{i+1}. {item['title']} ({item['source']})"
        for i, item in enumerate(news_list)
    ])

    ranking_prompt = f"""
    From the following 5 news headlines, select the ONE 
    most strategically important for an enterprise AI company like DataVex.

    Criteria:
    - Market impact
    - Enterprise infrastructure relevance
    - AI scalability implications

    Headlines:
    {formatted_news}

    Return strictly in this format:

    Title: <exact headline>
    Reasoning: <short reasoning>
    """

    try:
        ranked_response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=ranking_prompt
        )
        ranking_text = ranked_response.text.strip()
    except Exception:
        # Fallback to first article if Gemini fails
        selected_article = news_list[0]
        return {
            "all_news": news_list,
            "selected_news": {
                "title": selected_article.get("title"),
                "reasoning": "Fallback selection due to ranking failure.",
                "source": selected_article.get("source"),
                "url": selected_article.get("url"),
                "published_at": selected_article.get("published_at")
            }
        }

    # =====================================
    # 🔹 Step 4: Extract Title + Reasoning
    # =====================================
    selected_title = ""
    reasoning = ""

    for line in ranking_text.split("\n"):
        if line.lower().startswith("title:"):
            selected_title = line.replace("Title:", "").strip()
        if line.lower().startswith("reasoning:"):
            reasoning = line.replace("Reasoning:", "").strip()

    # Match selected headline with actual news item
    selected_article = next(
        (item for item in news_list if selected_title in item["title"]),
        news_list[0]  # fallback if not matched
    )

    # =====================================
    # FINAL STRUCTURED RETURN
    # =====================================
    return {
        "all_news": news_list,
        "selected_news": {
            "title": selected_article.get("title"),
            "reasoning": reasoning,
            "source": selected_article.get("source"),
            "url": selected_article.get("url"),
            "published_at": selected_article.get("published_at")
        }
    }
from datetime import datetime

def calculate_score(article):
    score = 0

    title = article.get("title", "")
    date_str = article.get("date", "")

    # Recency Boost
    try:
        article_date = datetime.strptime(date_str, "%b %d, %Y")
        seconds_old = (datetime.now() - article_date).total_seconds()

        if seconds_old < 3600:  # within 1 hour
            score += 10
        elif seconds_old < 7200:
            score += 5
        elif seconds_old < 86400:
            score += 2
    except:
        pass

    # Slight boost for longer enterprise headlines
    if len(title.split()) > 8:
        score += 2

    return score