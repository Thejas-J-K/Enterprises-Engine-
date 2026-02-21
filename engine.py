from agents.scout import scout_agent
from agents.brain import brain_agent
from agents.writer import writer_agent
from dotenv import load_dotenv
import os
from cerebras.cloud.sdk import Cerebras

load_dotenv()
client = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))

def run_growth_engine(keyword):

    signal = scout_agent(keyword)
    print("SCOUT FOUND:", signal)

    brain_decision = brain_agent(signal)
    print("BRAIN ANALYSIS:", brain_decision)

    if "APPROVED" in brain_decision.upper():
        with open("prompts/brand_voice.txt", "r") as f:
            brand_voice = f.read()

        content = writer_agent(signal, brand_voice, client)

        return {
            "signal": signal,
            "brain": brain_decision,
            "content": content
        }

    else:
        return {
            "signal": signal,
            "brain": brain_decision,
            "content": "Signal Rejected by Brain Agent."
        }


if __name__ == "__main__":
    result = run_growth_engine("AI security breach")
    print(result)