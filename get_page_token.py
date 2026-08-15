import urllib.request
import urllib.parse
import json
import os

base_dir = r"C:\Users\Admin\.gemini\antigravity\scratch\windear-landing"

app_id = "1375049340788214"
app_secret = "7d07a285be9023c6d6bd13ca49fabc23"
short_token = "EAATimZAZBBnfYBSOFWzNuP9sFLR2d5GxR25Y9W92XtbBoapJIZBz6CI0xcyLroJbYtGnSs9TjKhgOlSabOQRVZBTZBii42KvXz0GvZAAdhOPA8WFJ3ZCiZBHOrDlPwiLJ5r8HjrzPBn8atErRnStQjmwqU7EK5CHqdLeADgxKrMYP7XqDcs5QB7RrNnO9itRz9aEkuYwOoBauXvvMwZAwhE4CHGcNptZA16nFovBJinXaNZAx0tGaqdVdxRSHrXpEFPcHnAfxZA7A0afDtnpJ1nIZBB6OVwZDZD"

try:
    # 1. Exchange short-lived token to long-lived token
    url1 = f"https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id={app_id}&client_secret={app_secret}&fb_exchange_token={short_token}"
    req1 = urllib.request.urlopen(url1)
    res1 = json.loads(req1.read().decode())
    long_token = res1.get("access_token")

    # 2. Get User ID
    url2 = f"https://graph.facebook.com/v18.0/me?access_token={long_token}"
    req2 = urllib.request.urlopen(url2)
    res2 = json.loads(req2.read().decode())
    user_id = res2.get("id")

    # 3. Get Permanent Page Access Token
    url3 = f"https://graph.facebook.com/v18.0/{user_id}/accounts?access_token={long_token}"
    req3 = urllib.request.urlopen(url3)
    res3 = json.loads(req3.read().decode())
    pages = res3.get("data", [])

    if pages:
        page_id = pages[0]["id"]
        page_token = pages[0]["access_token"]
        page_name = pages[0]["name"]

        # Write to .env
        env_content = f"OPENAI_API_KEY=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\nFB_APP_ID={app_id}\nFB_APP_SECRET={app_secret}\nFB_PAGE_ID={page_id}\nFB_PAGE_ACCESS_TOKEN={page_token}\nDRY_RUN=false\n"
        
        env_path1 = os.path.join(base_dir, ".env")
        env_path2 = os.path.join(base_dir, "my-skills", "tao-creative-fb", ".env")
        os.makedirs(os.path.dirname(env_path2), exist_ok=True)
        
        with open(env_path1, "w", encoding="utf-8") as f:
            f.write(env_content)
        with open(env_path2, "w", encoding="utf-8") as f:
            f.write(env_content)

        # Update post_test.py
        post_test_code = f"""import requests
import json

page_id = "{page_id}"
page_token = "{page_token}"

caption = \"\"\"[TỪ VẤT VẢ DUYỆT BÀI SANG NGỦ MỘT GIẤC DẬY PAGE ĐÃ TỰ ĐĂNG BÀI 🤖✨]

Bạn có bao giờ cảm thấy mệt mỏi vì ngày nào cũng phải ngồi vò đầu bứt tóc nghĩ ý tưởng, làm ảnh rồi đăng Facebook?

Hôm nay, Windear chính thức ứng dụng AI Agent tự động sản xuất trọn bộ Content (ẢNH + CAPTION) mỗi ngày!

🎧 HỌC TIẾNG ANH CÙNG WINDEAR:
🚀 Phương pháp Luyện tai 4 bước: Xẻ nhỏ từng audio khó nhất giúp chữa dứt điểm chứng nghe trôi tuột chữ.
📚 Chỉ 5 phút/ngày: Nẩy số phản xạ 2.0x tự nhiên.
🎁 Trải nghiệm ngay Web App Miễn Phí tại: https://web.windear.online

Chúc mọi người một ngày làm việc siêu năng lượng! 🚀✨

#Windear #LuyenTai4Buoc #NgheTroiChut #AIFirst\"\"\"

image_url = "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1024&q=80"

url = f"https://graph.facebook.com/v18.0/{{page_id}}/photos"
payload = {{
    "url": image_url,
    "caption": caption,
    "access_token": page_token
}}

try:
    response = requests.post(url, data=payload, timeout=30)
    res = response.json()
    print("Facebook Post Result:", json.dumps(res, indent=2, ensure_ascii=False))
except Exception as e:
    print("Error posting to Facebook:", e)
"""
        post_test_path = os.path.join(base_dir, "post_test.py")
        with open(post_test_path, "w", encoding="utf-8") as f:
            f.write(post_test_code)

        print(f"SUCCESSFULLY UPDATED TOKEN FOR PAGE '{page_name}' ({page_id})!")
    else:
        print("No pages found.")

except Exception as e:
    print("Error:", e)
