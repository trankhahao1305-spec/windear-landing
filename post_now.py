import requests
import json

page_id = "1329502136902421"
page_token = "EAATimZAZBBnfYBSEZCkdtJjuO1ZA2WkIaYNWWTta6hV3x2Hd2Ytq8RgIAdETgW9ro6jQlsWUkkcqYifyulsHYARLOkIOFw0fZBoCcXShMWhO0ltIij1QbZBQl3xemGZBTo8Uvhz1HH2V2kmtSTsWLxdzfTfz6gqA1mS6xnzoP4TTssejTWlVZAYrmyxSOg6eZA0ntaVYHNzKoWHTBi7QfVcHFcDVsUIIz6fsMglXvq1EZD"

message = """[TỪ VẤT VẢ DUYỆT BÀI SANG NGỦ MỘT GIẤC DẬY PAGE ĐÃ TỰ ĐĂNG BÀI 🤖✨]

Bạn có bao giờ cảm thấy mệt mỏi vì ngày nào cũng phải ngồi vò đầu bứt tóc nghĩ ý tưởng rồi đăng Facebook?

Hôm nay, Windear chính thức ứng dụng AI Agent tự động sản xuất trọn bộ Content (ẢNH + CAPTION) mỗi ngày!

🎧 HỌC TIẾNG ANH CÙNG WINDEAR:
🚀 Phương pháp Luyện tai 4 bước: Xẻ nhỏ từng audio khó nhất giúp chữa dứt điểm chứng nghe trôi tuột chữ.
📚 Chỉ 5 phút/ngày: Nẩy số phản xạ 2.0x tự nhiên.
🎁 Trải nghiệm ngay Web App Miễn Phí tại: https://web.windear.online

#Windear #LuyenTai4Buoc #NgheTroiChut #AIFirst"""

# Post text feed post
url = f"https://graph.facebook.com/v18.0/{page_id}/feed"
payload = {
    "message": message,
    "access_token": page_token
}

try:
    response = requests.post(url, data=payload, timeout=30)
    res = response.json()
    print("Facebook Post Feed Result:", json.dumps(res, indent=2, ensure_ascii=False))
except Exception as e:
    print("Error posting to Facebook:", e)
