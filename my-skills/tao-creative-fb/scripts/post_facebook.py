import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"

def post_to_facebook(image_url_or_path, caption):
    """
    Post image + caption to Facebook Fanpage Graph API /{page_id}/photos.
    """
    if DRY_RUN:
        print("=== DRY RUN MODE ACTIVE: NO REAL POSTING ===")
        print(f"Page ID: {FB_PAGE_ID}")
        print(f"Image: {image_url_or_path}")
        print(f"Caption: {caption[:100]}...")
        return {"id": "dry_run_photo_id_123456789"}

    if not FB_PAGE_ID or not FB_PAGE_ACCESS_TOKEN:
        print("Error: FB_PAGE_ID or FB_PAGE_ACCESS_TOKEN missing in .env")
        return None

    url = f"https://graph.facebook.com/v18.0/{FB_PAGE_ID}/photos"
    
    # Check if image is URL or local file path
    if image_url_or_path.startswith("http://") or image_url_or_path.startswith("https://"):
        payload = {
            "url": image_url_or_path,
            "caption": caption,
            "access_token": FB_PAGE_ACCESS_TOKEN
        }
        response = requests.post(url, data=payload)
    else:
        # Local file upload
        payload = {
            "caption": caption,
            "access_token": FB_PAGE_ACCESS_TOKEN
        }
        with open(image_url_or_path, "rb") as img_file:
            files = {"source": img_file}
            response = requests.post(url, data=payload, files=files)

    res_data = response.json()
    if response.status_code == 200 and "id" in res_data:
        photo_id = res_data["id"]
        print(f"SUCCESSFULLY POSTED TO FACEBOOK PAGE! Photo ID: {photo_id}")
        return res_data
    else:
        print(f"Facebook Graph API Error: {res_data}")
        return None

if __name__ == "__main__":
    img = sys.argv[1] if len(sys.argv) > 1 else "generated_image.png"
    cap = sys.argv[2] if len(sys.argv) > 2 else "Bài đăng tự động từ Windear Content Bot! 🚀 #Windear"
    post_to_facebook(img, cap)
