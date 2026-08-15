import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

page_id = os.getenv("FB_PAGE_ID", "1329502136902421")
page_token = os.getenv("FB_PAGE_ACCESS_TOKEN")

caption = """[TỪ VẤT VẢ DUYỆT BÀI SANG NGỦ MỘT GIẤC DẬY PAGE ĐÃ TỰ ĐĂNG BÀI 🤖✨]

Bạn có bao giờ cảm thấy mệt mỏi vì ngày nào cũng phải ngồi vò đầu bứt tóc nghĩ ý tưởng, làm ảnh rồi đăng Facebook?

Hôm nay, Windear chính thức ứng dụng AI Agent tự động sản xuất trọn bộ Content (ẢNH + CAPTION) mỗi ngày!

🎧 HỌC TIẾNG ANH CÙNG WINDEAR:
🚀 Phương pháp Luyện tai 4 bước: Xẻ nhỏ từng audio khó nhất giúp chữa dứt điểm chứng nghe trôi tuột chữ.
📚 Chỉ 5 phút/ngày: Nẩy số phản xạ 2.0x tự nhiên.
🎁 Trải nghiệm ngay Web App Miễn Phí tại: https://web.windear.online

Chúc mọi người một ngày làm việc siêu năng lượng! 🚀✨

#Windear #LuyenTai4Buoc #NgheTroiChut #AIFirst"""

image_url = "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1024&q=80"

url = f"https://graph.facebook.com/v18.0/{page_id}/photos"
payload = {
    "url": image_url,
    "caption": caption,
    "access_token": page_token
}

try:
    response = requests.post(url, data=payload, timeout=30)
    res = response.json()
    print("Facebook Post Result:", json.dumps(res, indent=2, ensure_ascii=False))
except Exception as e:
    print("Error posting to Facebook:", e)
