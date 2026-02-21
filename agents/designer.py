import os
import google.generativeai as genai

def designer_agent(content_summary, client):
    # 1. Setup Gemini
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    # Standard fallback image in case everything fails
    fallback_url = "https://images.unsplash.com/photo-1550751827-4bd374c3f58b"
    prompt_text = "Modern Enterprise AI Technology"

    try:
        # Use the most stable model name
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        visual_prompt_query = f"Provide a 10-word description for a tech image about: {content_summary}. Professional style."
        response = model.generate_content(visual_prompt_query)
        
        if response and response.text:
            prompt_text = response.text.strip()
            # Clean for URL use
            clean_prompt = "".join(e for e in prompt_text if e.isalnum() or e == " ")
            clean_prompt = clean_prompt.replace(" ", "%20")
            
            # Use Pollinations - High reliability
            image_url = f"https://pollinations.ai/p/{clean_prompt}?width=1024&height=1024&seed=42&model=flux"
        else:
            image_url = fallback_url
            
    except Exception as e:
        print(f"Gemini Error: {e}")
        image_url = fallback_url

    return {
        "url": image_url,
        "prompt_used": prompt_text
    }