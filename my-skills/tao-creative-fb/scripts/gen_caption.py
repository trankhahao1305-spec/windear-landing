import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_caption(topic, mode="organic"):
    """
    Generate caption following Windear Brand Voice using OpenAI GPT.
    """
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY is missing in .env")
        return "Caption fallback: Windear Luyện Tai 4 Bước"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    system_prompt = """Bạn là chuyên gia viết content cho thương hiệu Windear (Ebook & App Luyện Tai 4 Bước).
Tông giọng: Chân thành, hóm hỉnh, thực chiến, gọi 'bạn' xưng 'tui' (hoặc 'em - anh Khả Hào').
Từ ngữ đặc trưng bắt buộc dùng: 'nghe trôi tuột chữ', 'xẻ nhỏ audio', 'luyện tai 4 bước', '5 phút/ngày'.
Cấu trúc 3 phần: HOOK (nỗi đau) + BODY (lợi ích 4 bước) + CTA.
Độ dài: 80 - 150 từ. Kèm 3-4 hashtag."""

    user_prompt = f"Viết bài Facebook theo mode '{mode}' cho chủ đề/sản phẩm: {topic}"

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=30)
        res_data = response.json()
        if response.status_code == 200:
            caption = res_data["choices"][0]["message"]["content"]
            print("--- GENERATED CAPTION ---")
            print(caption)
            return caption
        else:
            print(f"GPT Error: {res_data}")
            return None
    except Exception as e:
        print(f"Exception during caption generation: {e}")
        return None

if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "Ebook 4 bước Luyện Tai Windear 2k"
    mode = sys.argv[2] if len(sys.argv) > 2 else "organic"
    generate_caption(topic, mode)
