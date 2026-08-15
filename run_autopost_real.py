import requests
import json

page_token = "EAATimZAZBBnfYBSD0ZBWDFBxSsNRGIgKoquK6PyeEuDSY2xWnHiCHOZAmfztPDQ7EEBkpMNQ1Y7yYCRByipzPKFxxb48UkRUhoFkXFmAXkYUPtdLK93fxmLUJkmqRzHArancTZASzJouYSGfL039fXNkYiD0zZAxjy7VlRnykRYe35W3ZA3tby3kdAYRZC2aTwyjBoox9VLkuqa29YqRfZBdgEALZAplVrn5mmugU8NOAWtsAZD"

caption = """[TẠI SAO BẠN BIẾT HẾT TỪ VỰNG NHƯNG NGHE NGƯỜI BẢN XỨ NÓI VẪN TRÔI TUỘT CHỮ? 🎧❌]

Rất nhiều bạn học tiếng Anh gặp chung một nghịch lý: Nhìn transcript thì từ vựng nào cũng biết, ngữ pháp nào cũng thông. Nhưng hễ bật video lên nghe là chữ cứ trôi tuột qua tai không đọng lại gì!

Lý do không phải vì bạn kém, mà là vì: Người bản xứ không phát âm từng từ rời rạc như từ điển. Họ nối âm, lướt âm và nuốt âm với tốc độ 2.0x!

🚀 GIẢI PHÁP TỪ PHƯƠNG PHÁP LUYỆN TAI 4 BƯỚC WINDEAR:
• Step 1-2: Xẻ nhỏ từng audio khó, "bắt bài" các nốt nối âm & biến âm.
• Step 3-4: Luyện lủng lỗ tai với tốc độ tăng dần, nẩy số phản xạ tự nhiên.
⏱️ Chỉ cần 5 phút mỗi ngày — nhẹ nhàng, không ngợp!

🎁 Trải nghiệm Web App Luyện tai MIỄN PHÍ ngay tại: https://web.windear.online

#Windear #LuyenTai4Buoc #NgheTroiChut #HocTiengAnhMoiNgay"""

image_path = r"C:\Users\Admin\.gemini\antigravity\scratch\windear-landing\output\ads_set1_painpoint.png"

# Use me/photos endpoint with Page token
url = "https://graph.facebook.com/v18.0/me/photos"

payload = {
    "caption": caption,
    "access_token": page_token
}

print("=== ĐANG AUTO-POST QUA ENDPOINT ME/PHOTOS ===")

try:
    with open(image_path, "rb") as img_file:
        files = {"source": img_file}
        response = requests.post(url, data=payload, files=files, timeout=60)
    
    res = response.json()
    print("Facebook API Response:", json.dumps(res, indent=2, ensure_ascii=False))
    
    if "id" in res:
        print("\n🎉 AUTO-POST THÀNH CÔNG 100% LÊN FANPAGE FACEBOOK!")
        print(f"Photo ID: {res['id']}")
        print(f"Post ID: {res.get('post_id', res['id'])}")
except Exception as e:
    print("Error:", e)
