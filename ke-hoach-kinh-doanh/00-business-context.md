# Business Context — Windear English (Trần Khả Hào)

## 1. Sản phẩm / dịch vụ chính
- **Tên sản phẩm:** Cẩm Nang Luyện Tai 4 Bước (Chữa dứt điểm chứng "Nghe trôi chữ") + Hệ sinh thái Windear.
- **Dạng:** Digital Info Product (Ebook PDF / Cẩm nang thực hành) kết hợp dịch vụ Coaching 1-1 và Tai nghe kiểm âm.
- **Đang ở giai đoạn:** Đã hoàn thiện sản phẩm số, tích hợp cổng thanh toán tự động và đã bán/test thành công đơn hàng thực tế trên VPS. Đang chuẩn bị scale phễu traffic.
- **Giá hiện tại:** 2.000 VNĐ (chế độ Launch Test thực chiến) / Giá niêm yết thương mại: 297.000 VNĐ.
- **Link sản phẩm:** `https://web.windear.online/luyen-tai-4-buoc.html` (hoặc `https://windear.online/luyen-tai-4-buoc.html`)

## 2. Khách hàng đang có & Chân dung mục tiêu
- **Đã bán cho ai:** 
  1. Người đi làm / sinh viên mất gốc tiếng Anh: Học ngữ pháp nhiều năm nhưng khi nghe người bản xứ nói nhanh, nuốt âm thì bị "trôi tuột chữ", không kịp nẩy số phản xạ.
  2. Người luyện thi IELTS/TOEIC: Kẹt band điểm Listening ở mức 5.0 - 6.0 vì thói quen vừa nghe vừa dịch sang tiếng Việt trong đầu.
  3. Người bận rộn: Cần phương pháp xẻ nhỏ audio nghe hiệu quả chỉ 10 - 15 phút mỗi ngày.
- **Họ tìm đến qua kênh nào:** Facebook Fanpage (qua các bài viết giải mã phát âm/nuốt âm do Agent tự động đăng), Group Telegram cộng đồng, Website trực tiếp.
- **Họ trả tiền vì điều gì:** Phương pháp "Luyện tai 4 bước" thực chiến, giải quyết trúng tim đen nỗi đau "nghe trôi chữ", có lộ trình cụ thể chứ không nói lý thuyết chung chung.

## 3. Tài sản đã có sau 19 ngày
- **Hệ thống Web & Backend trên VPS:** 
  - Website chạy trên VPS Linux với Python `server.py` & SQLite `brain.db`.
  - Cổng thanh toán SePay quét mã VietQR tự động khớp đơn và kích hoạt tức thì 24/7.
  - Hệ thống email tự động qua Resend API (bàn giao Ebook + chuỗi 3 email nurturing).
- **Hệ sinh thái Agent GoClaw:** 
  - Đội ngũ AI Agent trên Telegram: Lead Orchestrator (Mễ Mễ), Cây Bút (`viet-bai-fb`), Hoạ Sĩ (`tao-hinh-fb`).
  - Tích hợp Kanban tasks (`team_tasks`) điều phối công việc mượt mà.
- **Brand Voice:** Trẻ trung, thực chiến, đồng cảm, nói thẳng vào vấn đề ("banh lỗ tai ra nghe hoài vẫn trôi chữ"), xưng hô gần gũi "Tui - Bạn".

## 4. Mục tiêu kinh doanh 12 tháng tới
- **Mô hình kinh doanh muốn xây:** Hybrid Funnel:
  1. *Front-end:* Ebook / Mini-guide giá mềm (Lead Magnet & Tripwire: 2k - 99k) để gom tệp khách hàng có hành vi trả tiền.
  2. *Middle-end:* Khóa học video tự học / Template Flashcard Shadowing (299k - 599k).
  3. *Back-end / High-ticket:* Khóa Coaching 1-1 Luyện Tai 7 Ngày (1.990.000đ - 3.500.000đ) + Combo bán kèm Tai nghe kiểm âm.
- **Doanh thu mong muốn 12 tháng:** 300.000.000 VNĐ - 500.000.000 VNĐ (~30 - 40 triệu/tháng).
- **Vị trí trên thị trường VN trong 1 năm nữa:** Trở thành thương hiệu số 1 được nhắc đến khi người học tiếng Anh tìm kiếm giải pháp đặc trị chứng "Nghe trôi chữ" và phản xạ nghe nói không cần dịch.
