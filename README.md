# 🚀 Windear Landing Page & Hệ Thống CRM Luyện Tai Tiếng Anh

Windear là nền tảng Landing Page & Hệ Thống Quản Trị CRM tích hợp tự động hóa thanh toán ngân hàng (SePay VietQR) và chuỗi Email Marketing tự động (Resend API) dành cho sản phẩm giáo dục Tiếng Anh.

---

## 🛠️ Công Nghệ Sử Dụng

- **Frontend:** Vanilla HTML5, Modern CSS (Glassmorphic Dark UI), Client-side JavaScript.
- **Backend Serverless:** Vercel Serverless Functions (`api/`).
- **Database & State:** Upstash Redis / KVDB Cloud Store & Browser LocalStorage.
- **Email Automation:** Resend API (Transactional & Nurturing Email Sequence).
- **Payment Gateway:** SePay VietQR (Ngân Hàng MBBank).

---

## 💻 Hướng Dẫn Triển Khai (Deployment Guide)

### 1. Triển khai lên Vercel (Khuyên Dùng)

1. Clone repository về máy:
   ```bash
   git clone https://github.com/trankhahao1305-spec/windear-landing.git
   cd windear-landing
   ```

2. Cấu hình biến môi trường (Environment Variables) trên Vercel Project Settings:
   - `RESEND_API_KEY`: API Key từ Resend.com
   - `UPSTASH_REDIS_REST_URL`: (Tùy chọn) URL Upstash Redis
   - `UPSTASH_REDIS_REST_TOKEN`: (Tùy chọn) Token Upstash Redis

3. Push code lên GitHub branch `main`:
   ```bash
   git add .
   git commit -m "Deploy Windear project"
   git push origin main
   ```
   *Vercel sẽ tự động build và deploy lên tên miền chính `https://windear.online`.*

---

## 🔗 Các Trang Quan Trọng

- **Trang chủ Waitlist:** `https://windear.online`
- **Trang thanh toán Ebook:** `https://windear.online/thanh-toan`
- **Trang CRM Quản trị Admin:** `https://windear.online/admin`
