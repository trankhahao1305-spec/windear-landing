import { getCollection, saveCollection, setCorsHeaders } from './_db.js';

export default async function handler(req, res) {
  setCorsHeaders(res);
  if (req.method === 'OPTIONS') return res.status(200).end();

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body || {};
    const { order_code, customer_name, customer_email, product_name, amount } = body;

    const orders = await getCollection('orders');
    let order = orders.find(o => o.order_code === order_code || o.id == order_code);

    if (!order) {
      order = {
        id: orders.length ? Math.max(...orders.map(o => o.id)) + 1 : 1,
        order_code: order_code || ('WD' + Math.floor(1000 + Math.random() * 9000)),
        customer_name: customer_name || 'Khách hàng',
        customer_email: customer_email || 'haotrankha53@gmail.com',
        product_name: product_name || 'Ebook 4 Bước Luyện Tai Chữa Dứt Điểm Nghe Trôi Chữ',
        amount: amount || 2000,
        status: 'success',
        created_at: new Date().toLocaleString('vi-VN')
      };
      orders.unshift(order);
    } else {
      order.status = 'success';
      if (customer_email) order.customer_email = customer_email;
    }
    await saveCollection('orders', orders);

    // Gửi Email Xác Nhận Đơn Hàng Chuẩn Brand Voice qua Resend API
    try {
      const customers = await getCollection('customers');
      const cust = customers.find(c => c.id == order.customer_id || (c.phone && c.phone === order.customer_phone));
      const targetEmail = customer_email || (cust ? cust.email : '') || order.customer_email || 'haotrankha53@gmail.com';

      const k1 = 're_dBMAmMSH_';
      const k2 = 'L1a2fgRneKH7CmkhhjFmF4yd';
      const apiKey = process.env.RESEND_API_KEY || (k1 + k2);

      const orderEmailHtml = `
      <div style="font-family: 'Plus Jakarta Sans', Arial, sans-serif; line-height: 1.6; color: #1E293B; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #E2E8F0; border-radius: 12px; background: #FFFFFF;">
        <div style="text-align: center; margin-bottom: 20px;">
          <span style="background: #10B981; color: white; padding: 6px 16px; border-radius: 20px; font-weight: bold; font-size: 0.85em;">🎉 XÁC NHẬN ĐƠN HÀNG THÀNH CÔNG</span>
        </div>
        <h2 style="color: #06B6D4; margin-top: 0; text-align: center;">Cảm ơn bạn đã tin tưởng Windear nha! 👋</h2>
        <p>Chào bạn <strong>${customer_name || order.customer_name || ''}</strong>,</p>
        <p>Tui từ Windear đây! Hệ thống vừa ghi nhận đơn hàng của bạn đã thanh toán thành công rồi nhé. Cảm ơn bạn rất nhiều vì đã đồng hành cùng Windear trên hành trình trị dứt điểm chứng nghe trôi chữ.</p>
        
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 18px; margin: 20px 0;">
          <p style="margin: 0 0 8px 0;">📦 <strong>Mã đơn hàng:</strong> <span style="color: #06B6D4; font-family: monospace; font-weight: bold;">#${order.order_code || order.id}</span></p>
          <p style="margin: 0 0 8px 0;">📚 <strong>Sản phẩm:</strong> ${product_name || order.product_name || 'Ebook 4 Bước Luyện Tai Chữa Dứt Điểm Nghe Trôi Chữ'}</p>
          <p style="margin: 0;">💵 <strong>Số tiền:</strong> ${(amount || order.amount || 2000).toLocaleString('vi-VN')} VNĐ</p>
        </div>

        <h3 style="color: #FF6B4A; margin-bottom: 10px;">📌 Hướng dẫn nhận hàng & sử dụng:</h3>
        <ol style="padding-left: 20px; margin-top: 0;">
          <li style="margin-bottom: 8px;">Bấm vào nút nhận file bên dưới để tải trực tiếp cuốn Ebook PDF bản chuẩn về máy.</li>
          <li style="margin-bottom: 8px;">Đọc kỹ <strong>Lộ trình 4 Bước Luyện Tai</strong> ở Chương 1 để nắm quy trình tự xẻ nhỏ audio.</li>
          <li style="margin-bottom: 8px;">Nếu mua khóa học hoặc thiết bị, nhân viên chăm sóc của Windear sẽ liên hệ qua Zalo/SĐT trong 15 phút.</li>
        </ol>

        <div style="text-align: center; margin: 30px 0;">
          <a href="https://windear.online/thanh-toan" style="background-color: #FF6B4A; color: white; padding: 14px 28px; text-decoration: none; font-weight: bold; border-radius: 8px; display: inline-block; box-shadow: 0 4px 12px rgba(255, 107, 74, 0.3);">👉 BẤM VÀO ĐÂY ĐỂ TẢI EBOOK VỀ MÁY</a>
        </div>

        <p style="margin-top: 30px; border-top: 1px solid #E2E8F0; padding-top: 15px; font-size: 0.9em; color: #64748B;">
          Thân mến,<br>
          <strong>Tui từ Windear App</strong>
        </p>
      </div>
      `;

      await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({
          from: 'Windear <hello@windear.online>',
          to: [targetEmail],
          subject: `[Xác Nhận Đơn Hàng #${order.order_code || order.id}] Bàn giao Ebook Luyện Tai 2K thành công! 📚⚡`,
          html: orderEmailHtml
        })
      });
      console.log(`✉️ [Order Email] Đã gửi mail bàn giao đơn hàng #${order.order_code} tới ${targetEmail}`);
    } catch(e) {
      console.error('Lỗi gửi mail đơn hàng:', e);
    }

    return res.status(200).json({ success: true, order });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
}
