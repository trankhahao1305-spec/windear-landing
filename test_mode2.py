import os
import requests
import json

output_dir = r"C:\Users\Admin\.gemini\antigravity\scratch\windear-landing\output"
os.makedirs(output_dir, exist_ok=True)

# High quality curated ad visuals for Windear
images_data = [
    {
        "img_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=1024&q=80",
        "file_img": os.path.join(output_dir, "ads_set1_painpoint.png"),
        "file_txt": os.path.join(output_dir, "ads_set1_painpoint.txt"),
        "name": "Bộ 1 - Pain Point",
        "content": """[BẠN CÓ ĐANG BỊ CHỨNG "BIẾT TỪ VỰNG NHƯNG NGHE TRÔI TUỘT CHỮ"? 🎧❌]

Nhìn từ vựng trên giấy thì hiểu 100%, nhưng hễ bật video/phim Hollywood lên là chữ cứ trôi tuột qua tai không đọng lại gì?

Vấn đề không nằm ở trí nhớ của bạn. Vấn đề là tai bạn chưa từng được "bắt bài" các cụm nối âm & nuốt âm của người bản xứ!

📚 Cẩm Nang Ebook 4 Bước Luyện Tai Windear sẽ xẻ nhỏ từng audio khó nhất giúp bạn nẩy số phản xạ tự nhiên.
💸 Mức giá "tượng trưng": Chỉ 2.000 VNĐ (bằng một ly trà đá!).

👉 Nhấn "Tìm hiểu thêm" để chữa dứt điểm chứng nghe trôi chữ ngay hôm nay!
#Windear #LuyenTai4Buoc #NgheTroiChut #Ebook2k"""
    },
    {
        "img_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1024&q=80",
        "file_img": os.path.join(output_dir, "ads_set2_solution.png"),
        "file_txt": os.path.join(output_dir, "ads_set2_solution.txt"),
        "name": "Bộ 2 - Solution",
        "content": """[DỪNG NGAY VIỆC NGỒI CHÉP CHÍNH TẢ 30 PHÚT MỖI NGÀY MỎI TAY! 🛑]

Rất nhiều bạn bơi trong các video dài ngợp thở, nghe đi nghe lại vẫn không hiểu vì người bản xứ nói quá nhanh. 

Đừng lãng phí thời gian tự bơi nữa. Phương pháp Luyện Tai 4 Bước Windear sẽ giúp bạn:
🚀 Step 1-2: Xẻ nhỏ từng audio khó & làm quen nốt biến âm.
🚀 Step 3-4: Luyện lủng lỗ tai từ khó, nẩy số phản xạ 2.0x.
⏱️ Chỉ cần 5 phút/ngày — không mỏi tay, không ngợp!

🎁 Dùng thử Web App Luyện tai MIỄN PHÍ 100% ngay hôm nay.

👉 Nhấn "Tìm hiểu thêm" để trải nghiệm ngay!
#Windear #LuyenTai4Buoc #AppLuyenTai"""
    },
    {
        "img_url": "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=1024&q=80",
        "file_img": os.path.join(output_dir, "ads_set3_offer.png"),
        "file_txt": os.path.join(output_dir, "ads_set3_offer.txt"),
        "name": "Bộ 3 - Offer",
        "content": """[KHÓA COACHING 1-1 LUYỆN TAI 7 NGÀY — TẶNG TAI NGHE MONITOR 350K! 🎁✨]

Bạn muốn có người đồng hành sửa trực tiếp tư thế nghe và chỉnh từng nốt nuốt âm khó nhất qua Zoom?

🏆 Khóa Coaching 1-1 Windear 7 Ngày:
• Học 1-1 qua Zoom trực tiếp.
• Nẩy số phản xạ nghe bản xứ chỉ sau 1 tuần.
• Học phí hạt dẻ: Chỉ 199.000 VNĐ.
🔥 QUÀ TẶNG ĐẶC BIỆT: Tặng ngay 01 Tai nghe Monitor chuyên dụng (trị giá 350.000đ) cho 10 bạn đăng ký sớm nhất hôm nay!

👉 Nhấn "Đăng ký ngay" để nhận quà tặng độc quyền!
#Windear #Coaching11 #TaiNgheWindear"""
    }
]

print("=== ĐANG TẠO TRỌN BỘ 3 BỘ CREATIVE ADS THẬT VÀO THƯ MỤC OUTPUT ===")

for item in images_data:
    print(f"\n--- Đang tạo {item['name']} ---")
    try:
        # Download image
        res = requests.get(item["img_url"], timeout=30)
        with open(item["file_img"], "wb") as f:
            f.write(res.content)
        print(f"✅ Đã tạo file ảnh: {item['file_img']}")
    except Exception as e:
        print(f"Lỗi tải ảnh {item['file_img']}: {e}")

    # Write text file
    with open(item["file_txt"], "w", encoding="utf-8") as f:
        f.write(item["content"])
    print(f"✅ Đã tạo file Ad Copy: {item['file_txt']}")

print("\n🎉 ĐÃ XUẤT THÀNH CÔNG 3 FILE ẢNH VÀ 3 FILE AD COPY VÀO 'output'!")
