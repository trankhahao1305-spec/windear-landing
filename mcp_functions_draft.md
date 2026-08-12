# Danh Sách MCP Functions Cho Website Windear

Dựa trên cấu trúc dự án `windear-landing` (bao gồm hệ thống CRM SQLite `brain.db`, Landing Page `index.html`, Admin Panel `/admin` và bộ gửi email `email_sender.py`), dưới đây là 3 MCP function hữu ích nhất được chọn để xây dựng công cụ điều khiển cho AI Agent qua Telegram:

---

## 1. `get_today_orders` (Báo Cáo Đơn Hàng Hôm Nay)
- **Input params**: `date` (string, optional - định dạng YYYY-MM-DD, mặc định là ngày hôm nay)
- **Output dự kiến**: Tổng số đơn hàng, tổng doanh thu (VND), danh sách chi tiết các đơn (Tên khách hàng, sản phẩm, số tiền, trạng thái thanh toán).
- **Tình huống dùng hàng ngày**: Sáng mở mắt ra hoặc cuối ngày nhắn Telegram để xem nhanh doanh số và lượng đơn phát sinh trong ngày mà không cần mở máy tính.
- **Độ ưu tiên**: ⭐⭐⭐⭐⭐ (5/5)
- **Ví dụ câu nhắn Telegram sẽ trigger**: 
  - *"Mễ Mễ ơi, hôm nay có bao nhiêu đơn hàng rồi em?"*
  - *"Báo cáo doanh thu ngày hôm nay cho chủ nhân nhé."*

---

## 2. `update_landing_hero` (Đổi Tiêu Đề Landing Page Trực Tiếp)
- **Input params**: `new_headline` (string, required - nội dung tiêu đề mới)
- **Output dự kiến**: Trạng thái cập nhật thành công, thời gian áp dụng, đường link kiểm tra trực tiếp trên VPS.
- **Tình huống dùng hàng ngày**: Nảy ra chương trình khuyến mãi/Flash Sale cuối tuần, nhắn Telegram cho Agent để cập nhật ngay tiêu đề website mà không cần gõ code hay SSH vào VPS.
- **Độ ưu tiên**: ⭐⭐⭐⭐⭐ (5/5)
- **Ví dụ câu nhắn Telegram sẽ trigger**:
  - *"Mễ Mễ ơi, đổi tiêu đề landing page thành: 'Flash Sale Cuối Tuần — Giảm 50% Học Phí!'"*
  - *"Cập nhật cho chủ nhân tiêu đề chính trang web thành: 'Bật Mí Phương Pháp Luyện Nghe Tiếng Anh 5 Phút Mỗi Ngày'*."

---

## 3. `send_customer_email` (Gửi Email Chăm Sóc/Xác Nhận Khách Hàng)
- **Input params**: 
  - `to_email` (string, required - email người nhận)
  - `subject` (string, required - tiêu đề email)
  - `content` (string, required - nội dung email)
- **Output dự kiến**: Mã phản hồi gửi email thành công, ID email, thời gian gửi.
- **Tình huống dùng hàng ngày**: Khách nhắn tin tư vấn qua Telegram hoặc vừa đăng ký waitlist, nhắn cho Agent để gửi email chào mừng/báo giá cho khách ngay lập tức.
- **Độ ưu tiên**: ⭐⭐⭐⭐☆ (4/5)
- **Ví dụ câu nhắn Telegram sẽ trigger**:
  - *"Mễ Mễ ơi, gửi email cho anh Huy (huy@gmail.com) nội dung cảm ơn anh đã đăng ký tư vấn khóa học nhé."*
  - *"Gửi email xác nhận kèm tài liệu cho khách khachhang@gmail.com giúp chủ nhân."*
