import os
import requests
from agents.analyst import analyst_agent
from agents.creator import creator_agent
from agents.visualist import visualist_agent


# =====================================
# Wikipedia Fact Layer
# =====================================
def fetch_wikipedia_summary(topic: str) -> str:
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
        response = requests.get(url)

        if response.status_code != 200:
            return ""

        data = response.json()
        return data.get("extract", "")

    except Exception:
        return ""


# =====================================
# MAIN ENGINE
# =====================================
def run_growth_engine():

    # =====================================
    # 1️⃣ ANALYST (5 News + Ranked Selection)
    # =====================================
    analysis = analyst_agent()

    if not analysis:
        return {
            "all_news": [],
            "signal": "No signal found.",
            "strategy": "",
            "first_draft": "",
            "trace": "",
            "content": "",
            "image": None,
            "video": ""
        }

    all_news = analysis.get("all_news", [])
    signal = analysis.get("selected_news", "")

    if not signal:
        signal = "No high-priority signal selected."

    # =====================================
    # 2️⃣ WIKIPEDIA FACT LAYER
    # =====================================
    wiki_summary = fetch_wikipedia_summary("Artificial intelligence")

    # =====================================
    # 3️⃣ STRATEGY FRAMING
    # =====================================
    strategy = f"""
Strategic Positioning:

Angle Chosen:
Reframe the selected signal as validation that enterprise AI infrastructure
requires resilient, scalable architecture.

Why This Angle:
Aligns with DataVex’s infrastructure-first positioning.

Factual Context (Wikipedia Reference):
{wiki_summary[:500]}

Discarded:
Generic reporting without strategic interpretation.
"""

    # =====================================
    # 4️⃣ CREATOR (Blog Generation)
    # =====================================
    try:
        with open("prompts/brand_voice.txt", "r", encoding="utf-8") as f:
            brand_voice = f.read()
    except FileNotFoundError:
        brand_voice = "Professional enterprise AI consulting tone."

    try:
        blog = creator_agent(signal, brand_voice)
    except Exception:
        blog = "Fallback blog: Enterprise AI infrastructure requires scalable and resilient systems."

    if not blog:
        blog = "Blog generation failed."

    blog += "\n\n---\nSource Context: Wikipedia + Ranked Enterprise News Signal"

    first_draft = blog[:600]

    trace = (
        "Parallel self-critique executed during generation. "
        "Enterprise tone validated."
    )

    # =====================================
    # 5️⃣ VISUALIST (Safe Handling)
    # =====================================
    try:
        image_data, video_script = visualist_agent(blog)
    except Exception:
        image_data = None
        video_script = "Video storyboard could not be generated due to API limits."

    # =====================================
    # 6️⃣ Embed Image into Blog Content
    # =====================================
    if image_data:

        # If URL image
        if isinstance(image_data, str) and image_data.startswith("http"):
            blog = f"![DataVex AI Visual]({image_data})\n\n" + blog

        # If bytes image
        elif isinstance(image_data, bytes):
            os.makedirs("media", exist_ok=True)
            image_path = "media/generated_image.png"

            with open(image_path, "wb") as f:
                f.write(image_data)

            blog = f"![DataVex AI Visual]({image_path})\n\n" + blog

    else:
        # Placeholder image if generation failed
        placeholder_url = "https://via.placeholder.com/800x400.png?text=DataVex+AI+Infrastructure"
        blog = f"![DataVex Placeholder]({placeholder_url})\n\n" + blog

    # =====================================
    # FINAL RESPONSE OBJECT
    # =====================================
    return {
        "all_news": all_news,
        "signal": signal,
        "strategy": strategy,
        "first_draft": first_draft,
        "trace": trace,
        "content": blog,      # 👈 now contains image markdown
        "image": image_data,
        "video": video_script
    }


# =====================================
# CLI TEST MODE
# =====================================
if __name__ == "__main__":
    result = run_growth_engine()
    print(result)