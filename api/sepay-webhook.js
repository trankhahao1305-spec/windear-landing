import { getCollection, saveCollection, setCorsHeaders } from './_db.js';

export default async function handler(req, res) {
  setCorsHeaders(res);
  if (req.method === 'OPTIONS') return res.status(200).end();

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body || {};
    console.log('🔔 [SePay Webhook Vercel] Nhận dữ liệu:', JSON.stringify(body));

    const content = (body.content || body.description || '').toUpperCase();
    const orders = await getCollection('orders');

    let matchedOrder = orders.find(o => o.status === 'pending' && o.order_code && content.includes(o.order_code.toUpperCase()));

    if (matchedOrder) {
      matchedOrder.status = 'success';
      await saveCollection('orders', orders);
      console.log(`✅ [Webhook SePay] Kích hoạt thành công đơn hàng ${matchedOrder.order_code}`);
      return res.status(200).json({ success: true, order: matchedOrder });
    }

    // Fallback: active latest pending order
    const latestPending = orders.find(o => o.status === 'pending');
    if (latestPending) {
      latestPending.status = 'success';
      await saveCollection('orders', orders);
      console.log(`✅ [Webhook SePay] Kích hoạt đơn pending gần nhất ${latestPending.order_code}`);
      return res.status(200).json({ success: true, order: latestPending });
    }

    return res.status(200).json({ success: true, message: 'Processed without pending match' });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
}
