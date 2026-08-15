import os
import sys
import requests
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_image(prompt_text, output_filename="generated_image.png"):
    """
    Generate an image using OpenAI DALL-E API and save it locally.
    """
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY is missing in .env file.")
        return None

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "dall-e-3",
        "prompt": prompt_text,
        "n": 1,
        "size": "1024x1024",
        "quality": "standard"
    }

    try:
        response = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=payload, timeout=60)
        res_data = response.json()
        
        if response.status_code == 200 and "data" in res_data:
            image_url = res_data["data"][0]["url"]
            print(f"Image generated successfully: {image_url}")
            
            # Download image to local file
            img_res = requests.get(image_url)
            if img_res.status_code == 200:
                with open(output_filename, "wb") as f:
                    f.write(img_res.content)
                print(f"Saved image to {output_filename}")
                return image_url
        else:
            print(f"OpenAI Image Error: {res_data}")
            return None
    except Exception as e:
        print(f"Exception during image generation: {e}")
        return None

if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "A modern 3D illustration of a student listening to English audio on headphones with a smile, vibrant clean background"
    generate_image(prompt)
