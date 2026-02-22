import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def analyst_agent():

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "q": "latest AI infrastructure news OR AI security breach OR enterprise AI failure",
        "gl": "us",
        "hl": "en"
    }

    response = requests.post(
        "https://google.serper.dev/news",
        headers=headers,
        json=payload
    )

    news = response.json()["news"][0]

    signal = f"{news['title']} - {news['snippet']}"

    return signal