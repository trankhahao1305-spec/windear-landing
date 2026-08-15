---
name: tao-creative-fb
description: Sản xuất trọn bộ Content hoàn chỉnh (gồm CẢ ẢNH VÀ VĂN BẢN) cho Facebook Page Windear. Dùng khi người dùng bảo "tạo content cho ngày mai", "gen bài Page", "content free", "tạo creative ads", "gen ads cho sản phẩm X", "cần 3 bộ creative".
---

# SKILL: Sản Xuất Content & Creative Ads Facebook (2 Mode)

## 1. Mục Đích
Tự động tạo trọn bộ bài đăng Facebook (ẢNH 1024x1024 + CAPTION CHUẨN BRAND VOICE WINDEAR) cho cả nội dung hàng ngày (Organic Content) lẫn nội dung quảng cáo chiến dịch (Creative Ads).

---

## 2. Quy Trình 2 Mode

### MODE 1 — CONTENT FREE (Tự động đăng Fanpage mỗi ngày)
- **Kích hoạt khi**: *"tạo content cho ngày mai"*, *"gen bài Page"*, *"content free"*, *"content organic"*.
- **Các bước**:
  1. **Tạo 3 ý tưởng**: Xuất 3 ý tưởng tiêu đề + góc nhìn ngắn cho người dùng chọn.
  2. **Sinh Full Content**:
     - Gọi `scripts/gen_image.py` tạo 1 ảnh đẹp 1024x1024 bằng OpenAI Image API.
     - Gọi `scripts/gen_caption.py` tạo 1 Caption hoàn chỉnh (80-150 từ, Hook + Body + Soft CTA).
  3. **Xem trước (Preview)**: Hiển thị cả Ảnh + Caption cho người dùng kiểm tra.
  4. **Đăng bài**: Gọi `scripts/post_facebook.py` đăng cả Ảnh + Caption lên Fanpage khi người dùng xác nhận "OK".

---

### MODE 2 — CREATIVE ADS (Sản xuất 3 bộ Quảng cáo chiến dịch)
- **Kích hoạt khi**: *"tạo creative ads"*, *"gen ads"*, *"cần 3 bộ creative"*.
- **Các bước**:
  1. Sinh **3 BỘ CREATIVE** hoàn chỉnh (Mỗi bộ = 1 Ảnh Ads + 1 Ad Copy ghép đôi):
     - **Bộ 1 (Pain Point)**: Nỗi đau "nghe trôi tuột chữ".
     - **Bộ 2 (Solution)**: Phương pháp "Luyện tai 4 bước 5 phút/ngày".
     - **Bộ 3 (Offer)**: Ưu đãi Ebook 2k & App Miễn Phí.
  2. Xuất kết quả ghép đôi sẵn sàng copy-paste vào Facebook Ads Manager (KHÔNG tự động đăng).
