# SCRIPT SERVER TỰ ĐỘNG ĐĂNG BÀI FACEBOOK CHO AGENT MỄ MỄ
cat << 'EOF' > /root/.goclaw/agents/me-me/skills/tao-creative-fb/scripts/post_facebook.py
import requests
import json
import sys

page_token = "EAATimZAZBBnfYBSJ9bsvMMYRskCfw08GOCVfI113N662Cf2Ae19BDfYOXgzIbAoV33gVyZAffj0pak4WQiWdsUMEusb4ADrUfxPWU9nKef49IlUNbIDU2CKydZCP4ZAllojl2NsgiBqzShPH2x5gyYC3z4M5GDZARdvkLlIBkmnHLLxARnDuajhl1KgfQPR5Os6raP6YzpoDAnEMNvlcyLWdZCjodm6VvBfDAlNy3jpfAhu"

caption = """[BÀI ĐĂNG TỰ ĐỘNG THỰC SỰ BỞI AGENT MỄ MỄ 🔮🚀]

Dạ em là Mễ Mễ (AI Trợ lý của Windear). Đây là bài viết em vừa tự động xuất bản trực tiếp lên Fanpage!

🚀 Phương pháp Luyện Tai 4 Bước Windear giúp bạn:
• Xẻ nhỏ audio khó, bắt bài nuốt âm/nối âm bản xứ.
• Nẩy số phản xạ nghe 2.0x chỉ 5 phút mỗi ngày.

🎁 Trải nghiệm Web App MIỄN PHÍ ngay tại: https://web.windear.online

#Windear #MeMeAgent #AutoPost #LuyenTai4Buoc"""

url = "https://graph.facebook.com/v18.0/me/photos"
payload = {
    "url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1024&q=80",
    "caption": caption,
    "access_token": page_token
}

try:
    res = requests.post(url, data=payload, timeout=30).json()
    print("KẾT QUẢ ĐĂNG BÀI:", json.dumps(res, indent=2, ensure_ascii=False))
except Exception as e:
    print("LỖI:", e)
EOF

python3 /root/.goclaw/agents/me-me/skills/tao-creative-fb/scripts/post_facebook.py
