from agents.scout import scout_agent
from agents.brain import brain_agent
from agents.writer import writer_agent
from agents.strategist import strategist_agent
from agents.critic import critic_agent
from dotenv import load_dotenv
import os
from cerebras.cloud.sdk import Cerebras


load_dotenv()
client = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))

def run_growth_engine(keyword):
    # 1. SCOUT: Find the raw data
    signal = scout_agent(keyword)
    
    # 2. BRAIN: Filter for DataVex relevance
    brain_decision = brain_agent(signal, client)
    
    if "APPROVED" in brain_decision.upper():
        with open("prompts/brand_voice.txt", "r") as f:
            brand_voice = f.read()

        # 3. STRATEGIST: Decide the "Attack Angle" (Requirement: Strategy Brief)
        strategy_brief = strategist_agent(signal, client)

        # 4. WRITER: Create First Draft
        first_draft = writer_agent(signal, brand_voice, client)

        # 5. CRITIC: The Critique Loop (Requirement: The Trace)
        # The Critic reviews the Writer's work against the Brand Voice
        critique = critic_agent(first_draft, brand_voice, client)
        
        # 6. WRITER (V2): Final Polish based on Critic's feedback
        final_content = client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"You are the DataVex Writer. Original: {first_draft}. Feedback: {critique}"},
                {"role": "user", "content": "Rewrite the content to be 100% brand aligned based on the feedback."}
            ],
            model="llama3.1-8b"
        ).choices[0].message.content

        return {
            "signal": signal,
            "brain": brain_decision,
            "strategy": strategy_brief,
            "trace": f"CRITIC FEEDBACK: {critique}", # Shows judges the 'Thinking'
            "content": final_content
        }

    else:
        return {
            "signal": signal,
            "brain": brain_decision,
            "content": "Signal Rejected by Brain Agent."
        }