import os
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras

# Importing your custom agents
from agents.scout import scout_agent
from agents.brain import brain_agent
from agents.writer import writer_agent
from agents.strategist import strategist_agent
from agents.critic import critic_agent
from agents.designer import designer_agent  # <--- New Agent

# Load environment variables (API Keys)
load_dotenv()

# Initialize the Cerebras Client
client = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))

def run_growth_engine(keyword):
    """
    The Orchestrator: Manages the flow between 6 different AI agents.
    """
    
    # 1. SCOUT: Search Google News for a specific signal
    print(f"🚀 Scout searching for: {keyword}...")
    signal = scout_agent(keyword)
    
    # 2. BRAIN: Check if news is relevant to DataVex AI
    print("🧠 Brain analyzing relevance...")
    brain_decision = brain_agent(signal, client)
    
    # Check if the Brain Agent gave the green light
    if "APPROVED" in brain_decision.upper():
        print("✅ Signal Approved. Starting Growth Workflow...")

        # Load the DataVex Brand Rules
        try:
            with open("prompts/brand_voice.txt", "r") as f:
                brand_voice = f.read()
        except FileNotFoundError:
            brand_voice = "Technical, professional, and authoritative."

        # 3. STRATEGIST: Create the 'Attack Angle' and Strategy Brief
        print("🎯 Strategist defining the angle...")
        strategy_brief = strategist_agent(signal, client)

        # 4. WRITER: Create the first draft of LinkedIn/Twitter/Blog content
        print("✍️ Writer creating first draft...")
        first_draft = writer_agent(signal, brand_voice, client)

        # 5. CRITIC: Review the draft against Brand Voice and Technical Accuracy
        print("🛡️ Critic reviewing the content...")
        critique = critic_agent(first_draft, brand_voice, client)
        
        # 6. WRITER (V2): Rewrite using Cerebras (Inference speed is key here)
        print("✨ Polishing final content...")
        final_content_response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"You are the DataVex Editor. Rules: {brand_voice}. Feedback: {critique}"},
                {"role": "user", "content": f"Original: {first_draft}. Rewrite this to be 100% brand-aligned."}
            ],
            model="llama3.1-8b"
        )
        final_content = final_content_response.choices[0].message.content

        # 7. DESIGNER: Generate the Visual Asset (DALL-E)
        # We pass the final content so the image matches the text perfectly
        print("🎨 Designer creating visual assets...")
        image_data = designer_agent(final_content, client)

        # Return the full package to app.py
        return {
            "signal": signal,
            "brain": brain_decision,
            "strategy": strategy_brief,
            "first_draft": first_draft,
            "trace": f"CRITIC FEEDBACK: {critique}",
            "content": final_content,
            "image": image_data  # Contains 'url' and 'prompt_used'
        }

    else:
        # If news is not relevant to DataVex, stop the process
        print("❌ Signal Rejected by Brain Agent.")
        return {
            "signal": signal,
            "brain": brain_decision,
            "content": "Signal Rejected: This news does not align with DataVex core services."
        }