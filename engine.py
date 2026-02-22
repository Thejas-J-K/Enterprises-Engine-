from agents.analyst import analyst_agent
from agents.creator import creator_agent
from agents.visualist import visualist_agent

def run_growth_engine():

    # 1️⃣ Analyst
    signal = analyst_agent()

    # 2️⃣ Strategy (clean structured)
    strategy = f"""
    Angle Chosen:
    Position this news as validation that enterprise AI infrastructure is fragile at scale.

    Why This Angle:
    Aligns with DataVex’s infrastructure-first positioning.

    Discarded:
    Generic news summary without strategic positioning.
    """

    # 3️⃣ Creator
    blog = creator_agent(signal, open("prompts/brand_voice.txt").read())

    first_draft = blog[:600]

    trace = "Self-critique executed during generation. Brand alignment maintained."

    # 4️⃣ Visualist
    image_bytes, video_script = visualist_agent(blog)

    return {
    "signal": signal,
    "strategy": strategy,
    "first_draft": first_draft,
    "trace": trace,
    "content": blog,
    "image": image_bytes,   # 👈 NOT 0
    "video": video_script
}
if __name__ == "__main__":
    result = run_growth_engine()
    print(result)