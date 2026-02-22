import base64
import os
from google import genai

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def visualist_agent(blog_content):

    prompt = (
        "Ultra realistic professional AI infrastructure illustration, "
        "modern data center, cloud computing, enterprise dashboards, "
        "cinematic lighting, 4K resolution"
    )

    try:
        response = client.models.generate_images(
            model="imagen-4.0-fast-generate-001",
            prompt=prompt,
            config={"size": "1024x1024"}
        )

        image_base64 = response.generated_images[0].image.image_bytes
        image_bytes = base64.b64decode(image_base64)

    except Exception as e:
        print("Image generation error:", e)
        image_bytes = None

    video_script = (
        "Scene 1: Futuristic AI city.\n"
        "Scene 2: Cloud data center.\n"
        "Scene 3: Enterprise dashboards.\n"
        "Scene 4: DataVex logo fade in."
    )

    return image_bytes, video_script