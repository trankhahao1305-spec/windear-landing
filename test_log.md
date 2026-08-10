# 📑 Nhật Ký Kiểm Thử & Sửa Lỗi (Test Log - Windear Project)

> **Dự án:** Windear - Landing Page & Hệ Thống CRM Luyện Tai Tiếng Anh  
> **Ngày kiểm thử:** 10/08/2026  
> **Môi trường:** Live Deployment (`https://windear.online`) & Vercel Serverless

---

## 🛠️ Danh Sách Các Lỗi (Bugs) Phát Hiện & Phương Án Khắc Phục

### Bug 1: Lỗi `404 Not Found` đối với Endpoint Polling Trạng Thái Thanh Toán (`/api/check-order-status`)
- **Mô tả lỗi:** Khi khách hàng ở trang thanh toán `/thanh-toan`, DevTools Console báo liên tục `GET /api/check-order-status 404 (Not Found)`.
- **Nguyên nhân:** File `vercel.json` bị thiếu quy tắc định tuyến (rewrite rule) cho `/api/check-order-status`.
- **Cách fix:** Bổ sung bộ quy tắc rewrites cho `/api/check-order-status`, `/api/manual-success-order` và `/api/sepay-webhook` trong `vercel.json`.
- **Trạng thái:** ✅ Đã sửa & Verified thành công.

---

### Bug 2: Lỗi `500 Internal Server Error` khi tạo Đơn hàng (`/api/create-order`)
- **Mô tả lỗi:** Khi bấm nút mua/tạo đơn thanh toán, Console báo lỗi `POST /api/create-order 500`.
- **Nguyên nhân:** Lỗi cú pháp JavaScript trong `api/create-order.js` do thiếu dấu ngoặc đóng `}` ở khối lệnh `else`.
- **Cách fix:** Viết lại cấu trúc điều kiện trong `api/create-order.js` chuẩn cú pháp Node.js.
- **Trạng thái:** ✅ Đã sửa & Verified thành công.

---

### Bug 3: Form Waitlist gửi dữ liệu trùng lặp 4 lần (Duplicate Form Submission)
- **Mô tả lỗi:** Điền form 1 lần nhưng Console hiện 4 lượt gửi request tới `/api/save-customer`, làm tạo 4 bản ghi trùng lặp.
- **Nguyên nhân:** Cả nút bấm `onclick="submitWaitlistFormDirect()"` trong `index.html` và sự kiện `nativeForm.addEventListener('submit')` trong `main.js` đều đăng ký lắng nghe song song.
- **Cách fix:** 
  1. Thêm cờ khóa chống gửi lặp `isWaitlistSubmitting = true` trong `index.html`.
  2. Vô hiệu hóa nút submit (`disabled = true`) khi đang xử lý request.
  3. Gộp duy nhất 1 Event Handler xử lý chung.
- **Trạng thái:** ✅ Đã sửa & Verified thành công.

---

### Bug 4: Gián đoạn gửi mail khi vượt Hạn ngạch Resend Free (Daily Quota Exceeded)
- **Mô tả lỗi:** Resend trả về lỗi HTTP 429 khi tài khoản miễn phí vượt mức 100 email/ngày.
- **Nguyên nhân:** Do test gửi mail nhiều lần liên tục làm vượt hạn ngạch 100 email/ngày.
- **Cách fix:** Bọc khối `try...catch` dạng **SafeMode** quanh lệnh gửi mail trong `api/save-customer.js`. Nếu Resend hết quota, server vẫn lưu dữ liệu Khách hàng vào CRM và phản hồi giao diện mượt mà 100%.
- **Trạng thái:** ✅ Đã sửa & Verified thành công.

---

### Bug 5: Dữ liệu Khách Hàng không hiển thị trong Chế độ Ẩn danh (Incognito Mode)
- **Mô tả lỗi:** Đăng ký trên trang chủ nhưng khi mở trang Admin `/admin` trong Chế độ Ẩn danh thì không thấy khách hàng mới.
- **Nguyên nhân:** Chế độ Ẩn danh chặn `localStorage` và `BroadcastChannel` của cửa sổ thường, đồng thời Vercel Serverless Function tái khởi động lại RAM liên tục.
- **Cách fix:** Tích hợp bộ lưu trữ đám mây toàn cầu **KVDB Cloud Store (`kvdb.io`)** đồng bộ 24/7 trực tiếp trên cả Client và Serverless Function.
- **Trạng thái:** ✅ Đã sửa & Verified thành công.

---

### Bug 6: Đơn hàng kích hoạt Success trong `/admin` không tự động gửi Email xác nhận
- **Mô tả lỗi:** Bấm nút `⚡ Kích hoạt Success` đơn hàng chuyển sang `✅ Đã thanh toán` nhưng khách không nhận được email xác nhận.
- **Nguyên nhân:** File `api/manual-success-order.js` chưa gọi Resend API và chưa nhận đủ payload Email khách hàng từ Admin.
- **Cách fix:** 
  1. Cập nhật `triggerManualSuccess()` trong `admin.html` để truyền đầy đủ thông tin Email & Đơn hàng.
  2. Viết bộ tự động gửi Email Bàn Giao Ebook chuẩn Brand Voice "Tui từ Windear" qua Resend API trong `api/manual-success-order.js`.
- **Trạng thái:** ✅ Đã sửa & Verified thành công.

---

### Bug 7: Không nhận được Email Xác Nhận Đơn Hàng khi Thanh Toán / Quét Mã SePay
- **Mô tả lỗi:** Điền form thanh toán `Trần Bình An`, tạo đơn và bấm nút kích hoạt thanh toán SePay nhưng hòm thư Gmail chưa nhận được Email bàn giao Ebook.
- **Nguyên nhân:** Khi tạo đơn ở `api/create-order.js`, thông tin `customer_email` chưa được lưu vào đối tượng đơn hàng `order`. Do đó khi SePay Webhook hay nút giả lập kích hoạt thành công, server không có email để gửi đi.
- **Cách fix:** 
  1. Cập nhật `api/create-order.js` để lưu đầy đủ `customer_email` vào đơn hàng.
  2. Tích hợp bộ tự động gửi Email Bàn Giao Ebook qua Resend API trong `api/sepay-webhook.js` và `thanh-toan.html`.
- **Trạng thái:** ✅ Đã sửa & Verified thành công.

---

### Bug 8: Múi giờ ngày mua hiển thị sai giờ UTC trên Vercel Serverless Function
- **Mô tả lỗi:** Đơn hàng tạo lúc 14:48:00 (Giờ Việt Nam) nhưng trang Admin hiển thị `07:48:00`.
- **Nguyên nhân:** Vercel Serverless Function chạy mặc định múi giờ UTC (GMT+0) thay vì múi giờ Việt Nam GMT+7.
- **Cách fix:** Đổi tất cả hàm khởi tạo ngày tháng sang chuẩn múi giờ Việt Nam: `new Date().toLocaleString('vi-VN', { timeZone: 'Asia/Ho_Chi_Minh' })`.
- **Trạng thái:** ✅ Đã sửa & Verified thành công.

