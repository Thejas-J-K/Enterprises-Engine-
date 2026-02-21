import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def scout_agent(keyword):

    url = "https://google.serper.dev/news"

    payload = {
        "q": keyword,
        "gl": "us",
        "hl": "en"
    }

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        return "Error fetching news."

    data = response.json()

    if "news" not in data or len(data["news"]) == 0:
        return "No relevant news found."

    top_news = data["news"][0]

    title = top_news.get("title", "")
    snippet = top_news.get("snippet", "")
    link = top_news.get("link", "")

    signal = f"""
    Title: {title}
    Summary: {snippet}
    Source: {link}
    """

    return signal